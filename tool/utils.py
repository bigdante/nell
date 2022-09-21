
from data_object import *
import numpy as np
import random
import datetime
import json
from bson import ObjectId
import uuid
from requests import post
from flask import jsonify


def precess_db_data(db_document):
    '''
        formate the result for browser 
    '''
    output = {}
    output['_id'] = str(db_document.id)
    output['head_entity'] = db_document.head
    output["head_linked_entity"] = "????"
    # s = BaseSentence.objects.get(id=db_document.evidence.id)
    indexs = np.asarray(db_document.headSpan)-BaseSentence.objects.get(id=db_document.evidence.id).charSpan[0]
    output['headSpan'] = indexs.tolist()
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
        get the page or entity related
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
        print("here asshole")
        result_triples = []
        pass
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

def get_pages(page_ids):
    '''
        get the pages by page_ids
    '''
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
            # 代表一个段落后的换行
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
                    result = [{
                        "_id": str(uuid.uuid4()),
                        "evidences": [{"text": "\n"}]
                    }]
            else:
                result = []
                for triple in TripleFact.objects(evidence=id):
                    result.append(precess_db_data(triple))
                # 如果对应的id在triple表中能找到，则result不为空，加入result_list，否则将句子直接放入
                if not result:
                    result = [{
                        "_id": str(uuid.uuid4()),
                        "evidences": [{"text": id_sentence[id]}]
                    }]
            result_list.append(result)
        result_triples[str(page_id)] = result_list
        save_result_json(result_triples)
    return result_triples