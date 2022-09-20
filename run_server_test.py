from flask import Flask, abort, request, jsonify
from datetime import datetime
from bson import ObjectId
from mongoengine.queryset.visitor import Q
import json
from requests import post
from tqdm import tqdm
from settings import *
from flask_cors import cross_origin, CORS
from data_object import *
import random
import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)


@app.route('/latest', methods=['GET'])
def latest():
    result = []
    for index, triple in enumerate(TripleFact.objects()):
        result.append(precess_db_data(triple))
        # show only 50
        if index >= 500:
            break
    random.shuffle(result)
    return output_process(result[:50])


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # ent_num, rel_num = tuple(open('get_ent_rel_num.txt').readlines())
    # ent_num = int(ent_num.strip('\n'))
    # rel_num = int(rel_num.strip('\n'))
    return output_process(
        {"all_triples": random.randint(0, 100), "all_entities": random.randint(0, 100),
         "all_relations": random.randint(0, 100),
         'running_days': random.randint(0, 100)})


@app.route('/pps', methods=['GET', 'POST'])
def show_pps():
    # query
    if request.method == 'POST':
        query_name = request.form.get('query_name')
        query_name = eval(request.data)['query_name']
    else:
        return " 'it's not a POST operation! \n"

    # assume that we get page_ids as followed
    # page_ids = [
    #     "624d2c91c20df149ac58742b",
    #     "624d2c91c20df149ac58743f",
    #     "624d2c91c20df149ac587451",
    #     "624d2c92c20df149ac587480",
    #     "624d2c92c20df149ac5874c1",
    #     "624d2c92c20df149ac5874cd",
    #     "624d2c92c20df149ac5874f0"
    # ]
    # query_name = "Abraham Lincoln"
    s_r = call_es(query_name)
    page_ids = []
    for r in s_r:
        page_ids.append(r['_id'])
    # 记录最终的返回结果
    result_triples = {}
    # 记录page_id和对应的所有sentence的ID
    page_sentence = {}
    id_sentence = {}
    for index, page_id in enumerate(page_ids):
        page = WikipediaPage.objects.get(id=ObjectId(page_id))
        # get sentences ids of this page
        sentences_ids = []
        for  paragrah in page.paragraphs:
            for sentence in paragrah.sentences:
                # print(index, " ",sentence.text)
                sentences_ids.append(sentence.id)
                id_sentence[sentence.id] = sentence.text
            # 代表一个段落后的换行
            sentences_ids.append("enter")
        page_sentence[page.id]=sentences_ids
    # print(page_sentence)
    for page_id, sentences_id in page_sentence.items():
        result_list = []
        for index, id in enumerate(sentences_id):
            if id == "enter":
                if result_list:
                    if type(result_list[-1])== str:
                        r = result_list[-1]
                        if not r.endswith("\n"):
                            result_list[-1] += '\n'
                    else:
                        r = result_list[-1][0]['evidences'][0]['text']
                        if not r.endswith("\n"):
                            result_list[-1][0]['evidences'][0]['text'] += '\n'
                continue
            result = []
            for triple in TripleFact.objects(evidence=id):
                # print(triple.evidence.text)
                result.append(precess_db_data(triple))
            # 找到id对应的三元组将结果放进去，如果result为空，则说明没找到，那么就直接将句子返回
            if result:
                result_list.append(result)
            else:
                result_list.append(id_sentence[id])
        print(result_list)
        if result_list:
            result_triples[str(page_id)]=result_list
        else:
            print("holly shit, no result in this page")

            # if result_triples and len(result_triples)>50:

    with open('result_triples.json', 'w') as f:
        # f.write(str(result_triples))
        json.dump(result_triples,f,indent=4)

        '''
            result_triples 格式：
                {
                    page_id:[[sentence1],[sentence2]],第一个list是page里的所有句子，list里面的每个元素也都是list，因为每个句子可能有多个三元组，这个list的每个元素就是之前返回的list中的每个元素
                    page_id:[[sentence1],[sentence2]]
                }
                所以在做句子拼接成段落时候，遍历每个list，第一个句子要作为标题，之后如果遇到了enter就表示要换行，直接接个换行符即可。

        '''

    return output_process(result_triples)



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)




e = JSONEncoder()


def output_process(result):
    result = json.loads(e.encode(result))
    return jsonify(result)


def precess_db_data(db_document):
    output = {}
    output['_id'] = str(db_document.id)
    output['head_entity'] = db_document.head
    output["head_linked_entity"] = "????"
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
    with post(url=url, headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf8'),
              auth=("nekol", "kegGER123")) as resp:
        results = resp.json()
        return results['hits']['hits']

if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    # CMD("python3 run.py")
    app.run(host="0.0.0.0", port=8841, debug=True)
