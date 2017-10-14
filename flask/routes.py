from flask import Flask, render_template, request

import datetime

from fast_europe import fast_europe

app  = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/welcome')
def welcome():
    pass
    return "WELCOME kind stranger :)"
    return render_template('input_number.html')

@app.route('/compute', methods=['POST'])
def compute():
    data_inici = request.form['data_inici']
    data_final = request.form['data_final']
    intervals = request.form['intervals']
    aeroports = request.form['aeroports']

    # intervals_parsed = []

    # for interval in intervals.split(';'):
        # intervals_parsed.append(tuple(interval.split(',')))
    intervals_parsed = intervals.split(',')

    aeroports_parsed = aeroports.split(',')

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

    return '{}'.format(fast_europe.calculate(aeroports_parsed, intervals_parsed, data_inici_parsed, data_final_parsed))

    return '''\
inici: {} <br>
final: {} <br>
intervals: {} <br>
aeroports: {} <br>
'''.format(
        data_inici,
        data_final,
        intervals_parsed,
        aeroports_parsed)



if __name__ == '__main__':
    app.run(debug=True)
