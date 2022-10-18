from flask import Flask, abort, request
from datetime import datetime
import random
from mongoengine.queryset.visitor import Q
import json,time,math
from requests import post
from tqdm import tqdm
from flask_cors import cross_origin, CORS
from data_object import *
from tool.utils import *
import uuid

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)


# 记录relation和id的对应
relation2id = {}
for r in BaseRelation.objects():
    if r.text not in relation2id.keys():
        relation2id[r.text] = r.id
# 记录总的条数，防止每次计算
total = WikidataEntity.objects.count()
@app.route('/latest', methods=['GET'])
def latest():
    '''
        return the latest triples extracted
    '''
    result = []
    # for index, triple in enumerate(TripleFact.objects()):
    start = time.time()
    for index, triple in enumerate(TripleFact.objects[:100]):
        result.append(precess_db_data(triple))
    # print("latest search done, consume time {:.2f}s".format(time.time()-start)) 
    return output_process(result)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # ent_num, rel_num = tuple(open('get_ent_rel_num.txt').readlines())
    # ent_num = int(ent_num.strip('\n'))
    # rel_num = int(rel_num.strip('\n'))
    return output_process(
        {"all_triples": random.randint(50, 100), "all_entities": random.randint(50, 100),
         "all_relations": random.randint(50, 100),
         'running_days': random.randint(50, 100)})


@app.route('/pps', methods=['GET', 'POST'])
def show_pps():
    if request.method == 'POST':
        message = eval(request.data)
        print(message)
        query_name = message['query_name'] if "query_name" in message.keys() else ""
        relation = message['relation'] if "relation" in message.keys() else ""
    else:
        return " 'it's not a POST operation! \n"
    print("search for",query_name)
    if relation:
        query_id = relation2id[query_name]
        results = get_relation(query_id)
    else:
        results = get_page_entity(query_name)
    return output_process(results)


@app.route('/entity', methods=['GET', 'POST'])
def show_entity():
    entity_list = []
    start = time.time()
    if request.method == 'POST':
        message = eval(request.data)
        page = message['page'] if "page" in message.keys() else 1
        size = message['size'] if "size" in message.keys() else 50
        refresh = message['refresh'] if "refresh" in message.keys() else False
    else:
        return " 'it's not a POST operation! \n"

    pages = math.ceil(total / size)
    # 刷新和分页
    if refresh:
        page = random.randint(0,pages)
    start_item = size*(page-1)
    end_item = size*page
    for index, entity in enumerate(WikidataEntity.objects[start_item:end_item]):
        entity_list.append({"id":str(entity.id),"text":entity.text})
    print("entity bar show done, consume time {:.2f}s".format(time.time()-start)) 
    result ={
        "data":entity_list,
        "pages":pages,
        "total":total
    }
    return result

@app.route('/entity_detail', methods=['GET','POST'])
def entity_detail():
    result = []
    start = time.time()
    if request.method == 'POST':
        message = eval(request.data)
        id = message['id']
    else:
        return " 'it's not a POST operation! \n"
    for index, triple in enumerate(TripleFact.objects(headWikidataEntity=ObjectId(id))):
        
        result.append(precess_db_data(triple,need_span=False))
    save_result_json(result,"./data/entity_deatil.json")
    print("entity-detail search done, consume time {:.2f}s".format(time.time()-start)) 
    return output_process(result)

@app.route('/entity_test', methods=['GET','POST'])
def entity_test():
    result = []
    start = time.time()
    if request.method == 'POST':
        message = eval(request.data)
        id = message['id']
    else:
        return " 'it's not a POST operation! \n"
    for index, triple in enumerate(TripleFact.objects(headWikidataEntity=ObjectId(id))):
        result.append(precess_db_data(triple,need_span=False))
    repeat = []
    repeat2 = []
    for r in result:
        t = r["head_entity"] + r["relation"] + r["tail_entity"]
        t2 = r["head_entity"] + r["relation"] + r["tail_entity"] + r["evidences"][0]["text"]
        if t not in repeat:
            repeat.append(t)
        else:
            if t2 not in repeat2:
                print("hhhhh,what i said")
                repeat2.append(t2)
            else:
                print("already, you stupid nut")
    save_result_json(repeat,"./data/test.json")
    print("entity-test search done, consume time {:.2f}s".format(time.time()-start)) 
    return output_process(result)


if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    # CMD("python3 run.py")
    app.run(host="0.0.0.0", port=8841, debug=True)
