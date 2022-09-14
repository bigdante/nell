from client import mongo
import datetime
from random import randint

import time
import json

client = mongo()


def write_jsons_to_db(examples):
    records = client.nell_example
    for e in examples:
        for evidence in e['evidences']:
            evidence['ts'] = datetime.datetime.strptime(evidence['ts'], '%Y-%m-%d %H:%M:%S.%f')
        e['last_updated'] = sorted([evidence['ts'] for evidence in e['evidences']], reverse=True)[0]
        e['thumb_up'] = randint(0, 4)
        e['thumb_down'] = randint(0, 2)
        records.insert(e)


if __name__ == '__main__':
    for file in ['nell2_examples_extend.json', 'example.json']:
        data = json.load(open('nell2_examples_extend.json'))
        write_jsons_to_db(data)
