#!/usr/bin/env python3
try:
    import api_wrapper
except ImportError:
    from . import api_wrapper
import json

#json_data = api_wrapper.save_geo_info()
with open('cities.json', 'r') as json_file:
    json_data = json.load(json_file)

# for continent in json_data['Continents']:
    # for it,shit in continent.items():
        # if it == 'Name':
            # print(it, shit)

europe = json_data['Continents'][2]

countries = {}

for country in europe['Countries']:
	countries[country['Name']]=country['Id']

with open('countries_list.json', 'w') as json_file:
	json.dump(countries, json_file)
