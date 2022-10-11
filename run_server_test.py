from flask import Flask, abort, request
from datetime import datetime

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
        query_name = message['query_name']
        index = message['index'] if "index" in message.keys() else "page"
    else:
        return " 'it's not a POST operation! \n"
    print("search for",query_name)
    # results = call_es(query_name,index=index)
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
    else:
        return " 'it's not a POST operation! \n"
    start_item = size*(page-1)
    end_item = size*page
    total = WikidataEntity.objects().all().count()
    pages = math.ceil(total / size)

    for index, entity in enumerate(WikidataEntity.objects[start_item:end_item]):
        entity_list.append({"id":str(entity.id),"text":entity.text})
    print("entity search done, consume time {:.2f}s".format(time.time()-start)) 
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
        result.append(precess_db_data(triple))
    print("entity-detail search done, consume time {:.2f}s".format(time.time()-start)) 
    return output_process(result)




if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    # CMD("python3 run.py")
    app.run(host="0.0.0.0", port=8841, debug=True)
