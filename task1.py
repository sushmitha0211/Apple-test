# Task 1

import json
import copy
import requests
import itertools


url = 'http://mysafeinfo.com/api/data?list=englishmonarchs&format=json'
response = requests.get(url)

monarch_list = json.loads(response.text)

res = itertools.groupby(monarch_list, key=lambda d: (d['cty'], d['hse']))
result = []

for k, v in res:
    entry = {'cty': k[0], 'hse': k[1]}
    entry['nm'] = [l['nm'] for l in v]
    result.append(entry.copy())

print(result)
