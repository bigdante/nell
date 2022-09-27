from flask import Flask, abort, request
from datetime import datetime

from mongoengine.queryset.visitor import Q
import json,time
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
        # return only 500 items
        if index >= 50:
            break
    print("latest search done, consume time {:.2f}s".format(time.time()-start)) 
    return output_process(result[:50])


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
    results = call_es(query_name,index=index)
    # result = get_page_entity(query_name)
    return output_process(results)


if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    # CMD("python3 run.py")
    app.run(host="0.0.0.0", port=8841, debug=True)
