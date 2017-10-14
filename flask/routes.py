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
	print("debug")
    data_inici = request.form['startdate']
    data_final = request.form['enddate']
    country = request.form['country']
    city0 = request.form['startcity']
    city1 = request.form['C1']
    days1 = request.form['NC1']
    city2 = request.form['C2']
    days2 = request.form['NC2']
    city3 = request.form['C3']
    days3 = request.form['NC3']
    city4 = request.form['C4']
    days4 = request.form['NC4']
	print("DEBUG")
    # intervals_parsed = []

    # for interval in intervals.split(';'):
        # intervals_parsed.append(tuple(interval.split(',')))
    intervals_parsed = [days1,days2,days3,days4]

    aeroports_parsed = [city0,city1,city2,city3,city4]

    inici, final = [], []



    for data in data_inici.split('-'):
        inici.append(int(data))

    for data in data_final.split('-'):
        final.append(int(data))

    data_inici_parsed = datetime.date(*inici)
    data_final_parsed = datetime.date(*final)

    # return '{} {}'.format(
            # data_inici_parsed,
            # data_final_parsed,
            # )

    result = fast_europe.calculate(aeroports_parsed, intervals_parsed, data_inici_parsed, data_final_parsed)

    if "error" in result:
         return render_template('error.html', error_code=result["error"])

    for vol in result['vols']:
        vol['link'] = api_wrapper.get_link(vol['orig'], vol['dest'], vol['dia'])
        vol['price'] = '{:.2f}'.format(vol['price'])

    return render_template('results.html', vols=result['vols'], price='{:.2f}'.format(result['cost']))

if __name__ == '__main__':
    app.run(debug=True)
