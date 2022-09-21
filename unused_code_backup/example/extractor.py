import json
import requests

from os.path import join

relations = ['creator', 'capital', 'educated_at', 'different_from', 'conflict', 'competition_class', 'composer',
             'conflict', 'connecting_line', 'country', 'country_for_sport', 'country_of_citizenship', 'developer',
             'writing_language', 'work_location', 'residence', 'publisher', 'publication_date', 'position_held',
             'point_in_time', 'industry', 'inception', 'headquarters_location', 'father']

doc = [
    "The series was originally published in English by two major publishers, Bloomsbury in the United Kingdom and Scholastic Press in the United States. Please answer: The series",
    relations]

with requests.post('http://127.0.0.1:10036/extract', json=doc) as resp:
    answers = resp.json()

print(json.dumps(dict(zip(relations, answers)), indent=4, ensure_ascii=False))
