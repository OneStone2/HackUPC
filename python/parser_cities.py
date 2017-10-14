#!/usr/bin/env python3
import json

with open('cities.json', 'r') as json_file:
    json_data = json.load(json_file)

# for continent in json_data['Continents']:
    # for it,shit in continent.items():
        # if it == 'Name':
            # print(it, shit)

europe = json_data['Continents'][2]

cities = {}

for country in europe['Countries']:
    for city in country['Cities']:
        cities[city['Name']] = dict(
                id=city['Id'],
                location=tuple(city['Location'].split(' '))
                )

