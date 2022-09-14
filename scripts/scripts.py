from settings import *
import re

res = dict()

for file in tqdm(sorted(list(os.listdir('/home/liuxiao/data/fever/wiki-pages')))):
    for line in open('/home/liuxiao/data/fever/wiki-pages/'+file):
            doc = json.loads(line)
            if not doc['lines']:
                continue
            lines = re.split(r'\n[0-9]+', doc['lines'])
            res[doc['id']] = []
            for sent in lines:
                    sent = sent.split('\t')
                    res[doc['id']].append(sent[1])
num = 0

for filename in ['train', 'shared_task_dev']:
    out = open('/home/liuxiao/data/fever/{}_verifiable.jsonl'.format(filename), 'w')
    for line in tqdm(open('/home/liuxiao/data/fever/' + filename + '.jsonl')):
        doc = json.loads(line)
        skip = False
        if doc["verifiable"] == "VERIFIABLE":
            doc['sentences'] = []
            for evidence in doc['evidence']:
                doc['sentences'].append([])
                for e in evidence:
                    try:
                        doc['sentences'][-1].append(res[e[2]][e[3]])
                    except:
                        skip = True
                        break
                if skip:
                    break
            if skip:
                continue
            out.write(json.dumps(doc, ensure_ascii=False) + '\n')
            num += 1

    print(num)
