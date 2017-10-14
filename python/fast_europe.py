#!/usr/bin/env python3
import api_wrapper
import datetime
import json
import multiprocessing
from subprocess import run, PIPE

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
d0 = datetime.timedelta(1)
mat = []
total = (d+1)*(n+1)*(n+1)
cur=0
with multiprocessing.Pool(6) as p:
    for i in range(d+1):
        t0 = []
        for city1 in tour:
            t1 = []
            for city2 in tour:
                print(round(1000*cur/total)/10,"%")
                cur = cur + 1
                if city1==city2:
                    t1.append(None)
                else:
                    q = '{:04}-{:02}-{:02}'.format(k1.year, k1.month, k1.day)
                    #q = str(k1.year) + "-" + str(k1.month) + "-" + str(k1.day)
                    c1 = cities[city1]["id"]+"-sky"
                    c2 = cities[city2]["id"]+"-sky"				
                    e = p.apply_async(api_wrapper.query_and_find_cheapest,[c1,c2,q])
                    try:
                        f = e.get(timeout=1)
                    except multiprocessing.context.TimeoutError:
                        f = None
                    if f is None:
                        t1.append(None)
                    else:
                        t1.append(f)
            t0.append(t1)
        mat.append(t0)
        k1 = k1 + d0
inp=str(n)+" "+str(d)
for i in range(n):
    inp=inp+" "+str(req[i])
for l in range(d+1):
    for i in range(n+1):
        for j in range(n+1):
            if mat[l][i][j] is None:
                nn = -1
            else:
                nn = mat[l][i][j]["price"]
            inp=inp+" "+str(nn)
print(inp)
process = run(
    ["./bin/flight_planner.o"],stdout=PIPE, input=inp.encode()
)
out = process.stdout.decode()

json_data = json.loads(out)
print(json_data)
