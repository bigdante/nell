import os
from os.path import abspath, dirname, join, exists
from collections import defaultdict
import json
import codecs
import csv
from bson import ObjectId
from tqdm import tqdm

# MONGO_HOST = os.environ.get('MONGO_HOST', '166.111.7.173')
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 30019)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'kegger_bigsci')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'datiantian123!@#')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'bigsci')

PROJ_DIR = join(abspath(dirname(__file__)), '.')
LINK_DIR = join(PROJ_DIR, 'link')
CLIENT_DIR = join(PROJ_DIR, 'client')
DATA_DIR = join(PROJ_DIR, 'data')
RAW_DATA_DIR = join(DATA_DIR, 'raw_data')
FUZZY_DIR = join(DATA_DIR, 'fuzzy')
CANDIDATE_DIR = join(PROJ_DIR, 'candidates')
os.makedirs(DATA_DIR, exist_ok=True)
OUT_DIR = join(PROJ_DIR, 'out')
EVAL_DIR = join(PROJ_DIR, 'evaluate')
os.makedirs(OUT_DIR, exist_ok=True)

# directory for datasets
EXPAND_DIR = join(DATA_DIR, 'expand')

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

json_dict = defaultdict(list)
e = JSONEncoder()

def get_all_jsons():
    json_dict.clear()
    for path, dir_list, file_list in os.walk(PROJ_DIR):
        for file in file_list:
            if file.endswith('.json'):
                json_dict[file].append(join(path, file))

get_all_jsons()

def read_json(filename, dir=None) -> json:
    get_all_jsons()
    if not filename.endswith('.json'):
        filename = filename + '.json'
    files = json_dict.get(filename)
    if files is None or len(files) == 0:
        raise RuntimeError("\nread_json_error: [{}] does not exist.".format(filename))
    elif len(files) > 1:
        message = "\n"
        for file in files:
            if dir and file.endswith(join(dir, filename)):
                return json.load(codecs.open(file, 'r', 'utf-8'))
            message = message + file + "\n"
        raise RuntimeError(message + "read_json_error: duplicated [{}].".format(filename))
    else:
        return json.load(codecs.open(files[0], 'r', 'utf-8'))


def write_json(data, path, filename, overwrite=False, indent=None, jsonify=False):
    if not overwrite and filename in json_dict:
        for file in json_dict[filename]:
            if file == join(path, filename):
                print("\nwrite_json_error: not allowed overwrite on [{}]".format(filename))
                print("Do you want to overwrite on the file? (y/n)\n")
                overwrite = input()
                if overwrite != 'y' and overwrite != 'Y':
                    raise RuntimeError("The user terminate the write process.")
    if jsonify:
        data = json.loads(e.encode(data))
    json.dump(data, codecs.open(join(path, filename), 'w', 'utf-8'), ensure_ascii=False, indent=indent)
    get_all_jsons()


def read_csv(path):
    f = codecs.open(path, 'r', 'utf-8')
    csv_reader = csv.reader(f)
    for row in csv_reader:
        yield row
