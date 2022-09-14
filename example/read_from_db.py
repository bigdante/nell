from client import mongo_ssh
from settings import ObjectId
import datetime

# client = mongo_ssh()
# records = client.nell_demo_records


def read_examples_from_db():
    data = []
    for record in records.find().sort('_id', -1).limit(50):
        record['last_updated'] = sorted([evidence['ts'] for evidence in record['evidences']], reverse=True)[0]
        data.append(record)
    return data


def thumb_up_to_db(_id, action):
    doc = records.find_one({'_id', _id})
    if action == 'cancel':
        doc['thumb_up'] -= 1
    else:
        doc['thumb_up'] += 1
    records.update({'_id': ObjectId(_id)}, {'$set': {'thumb_up', doc['thumb_up']}})
    return True


def thumb_down_to_db(_id, action):
    doc = records.find_one({'_id', _id})
    if action == 'cancel':
        doc['thumb_up'] -= 1
    else:
        doc['thumb_up'] += 1
    records.update({'_id': ObjectId(_id)}, {'$set': {'thumb_down', doc['thumb_down']}})
    return True


def get_records_num():
    return records.find().count()


def get_running_days():
    init_doc = list(records.find().sort('_id', 1).limit(5))[0]
    ts = datetime.datetime.strptime(init_doc['evidences'][0]['ts'], '%Y-%m-%d %H:%M:%S.%f')
    lasting_time = (datetime.datetime.now() - ts).days
    return lasting_time
