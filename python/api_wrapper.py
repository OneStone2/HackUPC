#!/usr/bin/env python3

from requests import get
import json

URL = 'http://partners.api.skyscanner.net/apiservices'

with open('./api_key', 'r') as api_file:
    APIKEY = api_file.read()

HEADER = {'Accept' : 'application/json'}

def get_cheapest_ariport(country, originPlace, destinationPlace, outboundPartialDate):
    """
    :return: chapest flight from airport originPlace, to airport
    destinationPlace on date outboundPartialDate
    :rtype: dict = {price=price, QuoteId=quoteId}
    """

    req = '/browsequotes/v1.0/{country}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}'

    values = dict(
        country=country,
        currency='EUR',
        locale='en_US',
        originPlace=originPlace,
        destinationPlace=destinationPlace,
        outboundPartialDate=outboundPartialDate,
        inboundPartialDate='',  #One way flight only
        apiKey=APIKEY,
    )

    req_format = req.format(**values)

    response = get(URL+req_format, headers=HEADER)

    json_data = json.loads(response.text)

    min_price = -1
    quoteId = None

    for quote in json_data['Quotes']:
        if quote['MinPrice'] < min_price or min_price==-1:
            min_price = quote['MinPrice']
            quoteId = quote['QuoteId']

    return dict(
        price=min_price,
        quoteId=quoteId
    )

