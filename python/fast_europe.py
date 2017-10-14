#!/usr/bin/env python3
try:
    import api_wrapper
except ImportError:
    from . import api_wrapper
import datetime
import json
import multiprocessing
from subprocess import run, PIPE

def calculate(tour, req, k1, k2):
    z = datetime.date
    if k1>=k2:
        return {"error":1}
    if k1<=z.today():
        return {"error":2}
    if k2-k1>datetime.timedelta(31):
        return {"error":3}
    if len(tour)!=len(req)+1 or len(tour)>5 or len(tour)<2:
        return {"error":6}
    #json_data = api_wrapper.save_geo_info()
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
    k0=k1
    n = len(tour)-1
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
                    #print(round(1000*cur/total)/10,"%")
                    cur = cur + 1
                    if city1==city2:
                        t1.append(None)
                    else:
                        q = '{:04}-{:02}-{:02}'.format(k1.year, k1.month, k1.day)
                        #q = str(k1.year) + "-" + str(k1.month) + "-" + str(k1.day)
                        try:
                            c1 = cities[city1]["id"]+"-sky"
                            c2 = cities[city2]["id"]+"-sky"
                        except KeyError:
                            return {"error":4}	
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
    process = run(
        ["./bin/flight_planner.o"],stdout=PIPE, input=inp.encode()
    )
    out = process.stdout.decode()
    json_data = json.loads(out)

    if json_data["cost"]==-1:
        return {"error":5}
    else:
        for i in range(n+1):
            if i==0:
                json_data["vols"][i]["carrier"]=mat[json_data["vols"][i]["dia"]][0][json_data["vols"][i]["dest"]]["carrier"]
                json_data["vols"][i]["price"]=mat[json_data["vols"][i]["dia"]][0][json_data["vols"][i]["dest"]]["price"]
            else:
                json_data["vols"][i]["carrier"]=mat[json_data["vols"][i]["dia"]][json_data["vols"][i-1]["dest"]][json_data["vols"][i]["dest"]]["carrier"]
                json_data["vols"][i]["price"]=mat[json_data["vols"][i]["dia"]][json_data["vols"][i-1]["dest"]][json_data["vols"][i]["dest"]]["price"]
        for i in range(n+1):
            if i==0:
                json_data["vols"][i]["orig"]=tour[0]
            else:
                json_data["vols"][i]["orig"]=json_data["vols"][i-1]["dest"]
            json_data["vols"][i]["dest"]=tour[json_data["vols"][i]["dest"]]
            json_data["vols"][i]["dia"]=k0+datetime.timedelta(json_data["vols"][i]["dia"])
        return json_data

def main():
    print(calculate(["Barcelona","Madrid","Rome","Berlin","Vienna","London"],[1,2,3,4,5],datetime.date(2017,10,20),datetime.date(2017,11,8)))

if __name__ == "__main__": main()
