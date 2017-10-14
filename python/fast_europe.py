#!/usr/bin/env python3
import api_wrapper
import datetime
import json

with open('cities.json', 'r') as json_file:
    json_data = json.load(json_file)

europe = json_data['Continents'][2]
cities = {}

for country in europe['Countries']:
    for city in country['Cities']:
        cities[city['Name']] = dict(
                id=city['Id'],
                location=tuple(city['Location'].split(' '))
                )

        print("Input number of cities")
n = int(input())
print("Input cities")
tour = []
for i in range(n+1):
    s = input()
        tour.append(s)
print("Input number of days you want to spend in each city")
req = []
for i in range(n):
    a = input()
        req.append(a)
print("Input dates")
y1 = int(input())
m1 = int(input())
d1 = int(input())
y2 = int(input())
m2 = int(input())
d2 = int(input())
k2 = datetime.date(y2,m2,d2)
k1 = datetime.date(y1,m1,d1)
dk = k2-k1
d = dk.days
d1 = datetime.timedelta(1)
mat = []
for i in range(d+1):
    t0 = []
        for city1 in tour:
            t1 = []
                for city2 in tour:
                    if city1==city2:
                        t1.append({})
                    else:
                        #print(cities[city1],cities[city2])
                                q = str(k1.year) + "-" + str(k1.month) + "-" + str(k1.day)
                                c1 = cities[city1]["id"]+"-sky"
                                c2 = cities[city2]["id"]+"-sky"				
                                e = api_wrapper.query_and_find_cheapest(c1,c2,q)
                                if e is None:
                                    t1.append({})
                                else:
                                    t1.append(e)
                t0.append(t1)
        mat.append(t0)
        k1 = k1 + d1
print(n, d)
for i in range(n):
    print(req[i])
for l in range(d+1):
    for i in range(n+1):
        for j in range(n+1):
            if mat[l][i][j] is None:
                print(-1)
            else:
                print(mat[l][i][j]["price"])


