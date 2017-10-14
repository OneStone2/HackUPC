import json

with open('./cities.json', 'r') as json_file:
    json_data = json.loads(json_file.read())

for it,shit in json_data.items():
    print(it)
