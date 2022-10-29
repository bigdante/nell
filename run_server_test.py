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

# # 记录relation和id的对应，后续还需要进行加速
# relation2id = {}
# for r in BaseRelation.objects():
#     if r.text not in relation2id.keys():
#         relation2id[r.text] = r.id
# 记录总的条数，防止每次计算
total = WikidataEntity.objects.count()
# total = 999
@app.route('/latest', methods=['GET'])
def latest():
    '''
        return the latest triples extracted
    '''
    result = []
    start = time.time()
    for index, triple in enumerate(TripleFact.objects[:100]):
        result.append(precess_db_data(triple,need_span=True))
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
    '''
        get the page and entity search results
    '''
    params = get_params(request)
    print("search for",params["query_name"])
    if params['relation']:
        '''
            if search for relation message
        '''
        # query_id = relation2id[params["query_name"]]
        results = get_relation(params["query_name"])
    else:
        results = get_page_entity(params["query_name"])
    return output_process(results)


@app.route('/entity', methods=['GET', 'POST'])
def show_entity():
    entity_list = []
    start = time.time()
    params = get_params(request)
    pages = math.ceil(total /params["size"])
    # 刷新和分页
    if params["refresh"]:
        params["page"] = random.randint(0,pages)
    start_item = params["size"]*(params["page"]-1)
    end_item = params["size"]*params["page"]
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
    params = get_params(request)
    for _, triple in enumerate(TripleFact.objects(headWikidataEntity=ObjectId(params["id"]))):
        r = precess_db_data(triple,need_span=True)
        r["head_unified"] = params["text"]
        hrt = r["head_entity"] + r["relation"] + r["tail_entity"]
        flag = 1
        for index, triple in enumerate(result):
            if hrt==triple["head_entity"] + triple["relation"] + triple["tail_entity"]:
                flag = 0
                result[index]["evidences"].append(r["evidences"][0])
                break
        if flag == 1 :
            result.append(r)
    save_result_json(result,"./data/entity_deatil.json")
    print("entity-detail {} search done, consume time {:.2f}s".format(params["text"],time.time()-start)) 
    return output_process(result)


@app.route('/thumb_up_down', methods=['GET','POST'])
def up_dowm():
    start = time.time()
    params = get_params(request)
    triple = TripleFact.objects(id=ObjectId(params["id"]))
    if params["type"] == "up":
        triple.thumb_up += 1
    elif params["type"] == "down":
        triple.thumb_down += 1
    result = triple.save()
    if result:
        print("record done, consume time {:.2f}s".format(time.time()-start)) 
        return {"success":True}
    else:
        print("record failed, consume time {:.2f}s".format(time.time()-start)) 
        return {"success":False}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8841, debug=True)
