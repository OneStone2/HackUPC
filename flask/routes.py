from flask import Flask, render_template, request

import datetime

from fast_europe import fast_europe, api_wrapper

app  = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/welcome')
def welcome():
    pass
    return "WELCOME kind stranger :)"
    return render_template('input_number.html')

@app.route('/compute', methods=['POST'])
def compute():
    data_inici = request.form['startdate']
    data_final = request.form['enddate']
    country = request.form['country']
    city0 = request.form['startcity']
    city1 = request.form['C1']
    days1 = request.form['NC1']
    city2 = request.form.get('C2', None)
    days2 = request.form.get('NC2', None)
    city3 = request.form.get('C3', None)
    days3 = request.form.get('NC3', None)
    city4 = request.form.get('C4', None)
    days4 = request.form.get('NC4', None)
    api_wrapper.set_country(country)
    if city2 !="" and days2 =="":
        return render_template('error.html', error_code=6)
    if city3 !="" and days3 =="":
        return render_template('error.html', error_code=6)
    if city4 !="" and days4 =="":
        return render_template('error.html', error_code=6)
    if city2 =="" and days2 !="":
        return render_template('error.html', error_code=7)
    if city3 =="" and days3 !="":
        return render_template('error.html', error_code=7)
    if city4 =="" and days4 !="":
        return render_template('error.html', error_code=7)
    # intervals_parsed = []

    # for interval in intervals.split(';'):
        # intervals_parsed.append(tuple(interval.split(',')))
    intervals_parsed = [days1]
    aeroports_parsed = [city0,city1]
    
    if city2 !="":
        intervals_parsed.append(days2)
        aeroports_parsed.append(city2)
    if city3 !="":
        intervals_parsed.append(days3)
        aeroports_parsed.append(city3)
    if city4 !="":
        intervals_parsed.append(days4)
        aeroports_parsed.append(city4)
    print(intervals_parsed,aeroports_parsed)
    inici, final = [], []



    for data in data_inici.split('-'):
        inici.append(int(data))

    for data in data_final.split('-'):
        final.append(int(data))

    data_inici_parsed = datetime.date(*inici)
    data_final_parsed = datetime.date(*final)

    result = fast_europe.calculate(aeroports_parsed, intervals_parsed, data_inici_parsed, data_final_parsed)

    if "error" in result:
        return render_template('error.html', error_code=result["error"])

    for vol in result['vols']:
        vol['link'] = api_wrapper.get_link(vol['orig'], vol['dest'], vol['dia'])
        vol['price'] = '{:.2f}'.format(vol['price'])

    return render_template('results.html', vols=result['vols'], price='{:.2f}'.format(result['cost']))

if __name__ == '__main__':
    app.run(debug=True)
