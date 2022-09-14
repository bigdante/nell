from client import mongo
from settings import *
from datetime import datetime
from collections import OrderedDict

from random import sample

client = mongo()


def get_filtered():
    data = defaultdict(list)
    stats = defaultdict(int)
    records = client.nell_demo_records_filtered

    for doc in tqdm(records.find({})):
        stats[doc['relation']] += 1
        data[doc['relation']].append(doc)

    for relation, docs in data.items():
        json.dump([json.loads(e.encode(d)) for d in docs],
                  open(join(DATA_DIR, 'sampled_test', relation.replace(' ', '_') + '_negs.json'), 'w'), indent=4,
                  ensure_ascii=False)
    stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    _stats = OrderedDict()
    check_exists = json.load(open(join(DATA_DIR, 'fsl_checking.train.json')))
    for x in stats:
        if x[0].replace('_', ' ') in check_exists:
            continue
        _stats[x[0]] = x[1]
    json.dump(_stats, open(join(DATA_DIR, '20220330_filtered_stats.json'), 'w'), indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_filtered()
