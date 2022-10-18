
from data_object import *
import numpy as np
import random
import datetime,time
import json
from bson import ObjectId
import uuid
from requests import post
from flask import jsonify
from mongoengine.queryset.visitor import Q
from tqdm import tqdm
import re

def get_params(request):
    '''
        get parameters
    '''
    params = {}
    if request.method == 'POST':
        message = eval(request.data)
        params["query_name"] = message['query_name'] if "query_name" in message.keys() else ""
        params["relation"] = message['relation'] if "relation" in message.keys() else ""
        params["page"] = message['page'] if "page" in message.keys() else 1
        params["size"] = message['size'] if "size" in message.keys() else 50
        params["refresh"] = message['refresh'] if "refresh" in message.keys() else False
        params["id"] = message['id'] if "id" in message.keys() else ""
        params["text"] = message['text'] if "text" in message.keys() else ""
    else:
        return " 'it's not a POST operation! \n"
    return params

def precess_db_data(db_document,need_span=True):
    '''
        formate the result for browser 
    '''
    output = {}
    output['new'] = random.randint(0,1)
    output['_id'] = str(db_document.id)
    output["head_linked_entity"] = "????"
    if need_span:
        indexs = np.asarray(db_document.headSpan)-BaseSentence.objects.get(id=db_document.evidence.id).charSpan[0]
        output['headSpan'] = indexs.tolist()
        output['head_entity'] = db_document.head
    else:
        # output['head_entity'] = re.sub(r"[^a-zA-Z.!?]+", r" ", db_document.head.lower())
        output['head_entity'] =db_document.head
    output['relation'] = db_document.relationLabel
    output['tail_entity'] = db_document.tail

    output['evidences'] = [{
        "text": db_document.evidenceText,
        "extractor": "GLM-2B/P-tuning",
        "confidence": random.random(),
        "filtered": True,
        "ts": str(datetime.date.today())
    }]


    return output


def call_es(text, index="page"):
    '''
        get the page or entity
    '''
    headers = {'Content-Type': 'application/json'}
    if index == 'page':
        url = 'http://166.111.7.106:9200/wikipedia_page/wikipedia_page/_search'
    elif index == 'entity':
        url = 'http://166.111.7.106:9200/wikipedia_entity/wikipedia_entity/_search'
    else:
        raise NotImplementedError()
    data = {
        "query": {"bool": {"should": [{"match": {"text": text}}]}}
    }
    with post(url=url, headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf8'),auth=("nekol", "kegGER123")) as resp:
        results = resp.json()
        s_r =  results['hits']['hits']
    if index == 'page':
        page_ids = [r['_id'] for r in s_r]
        result_triples = get_pages(page_ids)
    elif index == 'entity':
        entity_names = [r['_source']['text'] for r in s_r]
        entity_ids = [r['_id'] for r in s_r]
        result_triples=get_entity_net(entity_ids,entity_names)
    return result_triples


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def output_process(result):
    e = JSONEncoder()
    result = json.loads(e.encode(result))
    return jsonify(result)


def save_result_json(result_triples, path='./data/result_triples.json'):
    '''
        save the reuslt to json file
    '''
    with open(path, 'w') as f:
        json.dump(result_triples, f, indent=4)


def get_page_entity(query_name):
    result_all = {}
    result_all["page"] = call_es(query_name,"page")
    result_all["entity"] = call_es(query_name,"entity")
    save_result_json(result_all,"./data/page_entity.json")
    return result_all


def get_pages(page_ids):
    '''
        get the pages by page_ids
    '''
    start = time.time()
    # 记录最终的返回结果
    result_triples = {}
    # 记录page_id和对应的所有sentence的ID
    page_sentence = {}
    id_sentence = {}
    for index, page_id in enumerate(page_ids):
        page = WikipediaPage.objects.get(id=ObjectId(page_id))
        # get sentences ids of this page
        sentences_ids = []
        for paragrah in page.paragraphs:
            for sentence in paragrah.sentences:
                sentences_ids.append(sentence.id)
                id_sentence[sentence.id] = sentence.text
            # 代表一个段落后的换行，连续换行的话，就只保留一个
            if not sentences_ids[-1]=='enter':
                sentences_ids.append("enter")
        page_sentence[page.id] = sentences_ids

    for page_id, sentences_id in page_sentence.items():
        # 获取一个page所有sentence对应所有的三元组信息
        result_list = []
        for index, id in enumerate(sentences_id):
            # 遇到id=enter，代表需要回车
            if id == "enter":
                r = result_list[-1][0]['evidences'][0]['text']
                if not r.endswith("\n"):
                    result_list[-1][0]['evidences'][0]['text'] += '\n'
            else:
                result = []
                for triple in TripleFact.objects(evidence=id):
                    result.append(precess_db_data(triple))
                # 如果对应的id在triple表中能找到，则result不为空，加入result_list，否则将句子直接放入
                # 判断下是否文本内容就是个"\n""
                if not result:
                    if not id_sentence[id]=="\n":
                        result = [{
                            "_id": str(id),
                            "evidences": [{"text": id_sentence[id]}]
                        }]
                    else:
                        continue
                result_list.append(result)
                
        result_triples[str(page_id)] = result_list
    print("search page done....consume time:{:.2f}s".format(time.time()-start))
    return result_triples


def get_entity_net(entity_ids,entity_names):
    '''
        根据id，获得head和tail为关键词的所有的信息
         result = {
            word1:[{"head":x,"tail":b,"relationLabel":c},{},...],
            word2:[{},{},...]
        }
    '''
    start = time.time()
    result = {}
    for id,entity in tqdm(zip(entity_ids,entity_names)):
        nodes = [{"id":entity,"label":entity,"root":True}]
        edeges= []
        tables=[]
        # for triple in TripleFact.objects(Q(head=entity)):
        # for triple in TripleFact.objects(Q(head=entity) | Q(tail=entity)):
        for triple in TripleFact.objects(Q(headWikipediaEntity=ObjectId(id))):
            # if not triple.head.lower()==entity.lower():
            #     continue
            head = {
                    "id":triple.head,
                    "label":triple.head
            }
            tail = {
                    "id":triple.tail,
                    "label":triple.tail
            }
            relation = {
                    "source":triple.head,
                    "target":triple.tail,
                    "label":triple.relationLabel,
            }
            for_root = {
                    "source":entity,
                    "target":triple.head,
            }
            if head not in nodes:
                nodes.append(head)
            if tail not in nodes:
                nodes.append(tail)
            if relation not in edeges:
                edeges.append(relation)
            if for_root not in edeges and entity != for_root["target"]:
                edeges.append(for_root)
            
            r = precess_db_data(triple,need_span=False)
            hrt = r["head_entity"] + r["relation"] + r["tail_entity"]
            flag = 1
            for index, triple in enumerate(tables):
                t = triple["head_entity"] + triple["relation"] + triple["tail_entity"]
                if t == hrt:
                    flag = 0
                    tables[index]["evidences"].append(r["evidences"][0])
                    break
            if flag == 1 :
                tables.append(r)
            # tables.append(precess_db_data(triple,False))
        if nodes and edeges:    
            result[entity]={
                "nodes":nodes,
                "edges":edeges,
                "tables":tables
            }
    print("search entity done....consume time:{:.2f}s".format(time.time()-start))

    return result


def get_relation(query_id):
    '''
        通过relation获取到三元组的信息。
    '''
    result = []
    start = time.time()
    for index, triple in enumerate(TripleFact.objects(relation=query_id)):
        result.append(precess_db_data(triple,need_span=False))
        # 后期的优化
        if index > 1000:
            break
    save_result_json(result,"./data/relation.json")
    print("relation search done, consume time {:.2f}s".format(time.time()-start))
    return result
