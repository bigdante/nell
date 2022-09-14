from flask import Flask, abort, request, jsonify
from datetime import datetime
from bson import ObjectId
from mongoengine.queryset.visitor import Q

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
    # if request.method == 'POST':
    # 	qurey_name = request.form.get('qurey_name')
    #     print(qurey_name)
    # else:
    # 	return " 'it's not a POST operation! "
    # '''
    #     TODO:
    #     this code will get the page we need using the qurey_name
    #     pageid = []

    # '''
    # assume that we get page_ids as followed
    page_ids = [
        "624d2c91c20df149ac58742b",
        "624d2c91c20df149ac58743f",
        "624d2c91c20df149ac587451",
        "624d2c92c20df149ac587480",
        "624d2c92c20df149ac5874c1",
        "624d2c92c20df149ac5874cd",
        "624d2c92c20df149ac5874f0"
    ]

    result_triples = {}
    page_sentence = {}
    for index, page_id in enumerate(page_ids):
        page = WikipediaPage.objects.get(id=ObjectId(page_id))
        # get sentences ids of this page
        sentences_ids = []
        for  paragrah in page.paragraphs:
            for sentence in paragrah.sentences:
                # print(index, " ",sentence.text)
                sentences_ids.append(sentence.id)
            # 代表一个段落后到换行
            sentences_ids.append("enter")
        page_sentence[page.id]=sentences_ids
    # print(page_sentence)
    for page_id, sentences_id in page_sentence.items():
        result_list = []
        for index, id in enumerate(sentences_id):
            if id == "enter":
                # 并且之前有返回才添加回车，实际上，正常情况下不会这么做，否则拼接的句子将会乱七八糟
                if result_list:
                    r = result_list[-1][0]['evidences'][0]['text']
                    if not r.endswith("\n"):
                        result_list[-1][0]['evidences'][0]['text'] += '\n'
                continue
            result = []
            for triple in TripleFact.objects(evidence=id):
                # print(triple.evidence.text)
                result.append(precess_db_data(triple))
            if result:
                result_list.append(result)
        if result_list:
            result_triples[str(page_id)]=result_list
        else:
            print("holly shit, no result in this page")

            # if result_triples and len(result_triples)>50:

    with open('result_triples.json', 'w') as f:
        # f.write(str(result_triples))
        json.dump(result_triples,f)

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


if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    # CMD("python3 run.py")
    app.run(host="0.0.0.0", port=8841, debug=True)
