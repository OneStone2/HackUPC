#!/usr/bin/env python3

from requests import get
import json

import logging

URL = 'http://partners.api.skyscanner.net/apiservices'

CURRENCY='EUR'
LOCALE='US_en'
COUNTRY='ES'

with open('./api_key', 'r') as api_file:
    APIKEY = api_file.read()

HEADER = {'Accept' : 'application/json'}

def get_city_code(city):

    req = '/geo/v1.0?apiKey={apiKey}'

    values = dict(
        apiKey=APIKEY
        )

    req_format = req.format(**values)

    response = get(URL+req_format, headers=HEADER)

    json_data = json.loads(response.text)
    logging.debug(json_data)

    return json_data

def autosuggest(place_id):

    req = '/autosuggest/v1.0/{country}/{currency}/{locale}?id={place_id}&apiKey={apiKey}'

    values = dict(
            country=COUNTRY,
            currency=CURRENCY,
            locale=LOCALE,
            place_id=place_id,
            apiKey=APIKEY
            )

    req_format = req.format(**values)

    response = get(URL+req_format, headers=HEADER)

    json_data = json.loads(response.text)
    logging.debug(json_data)

    return json_data

def get_cheapest_ariport(originPlace, destinationPlace, outboundPartialDate):
    """
    :return: chapest flight from airport originPlace, to airport
    destinationPlace on date outboundPartialDate

    :rtype: dict = {price=price, quote=cheapest_quote}
    """

    req = '/browsequotes/v1.0/{country}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}'

    values = dict(
        country=COUNTRY,
        currency=CURRENCY,
        locale=LOCALE,
        originPlace=originPlace,
        destinationPlace=destinationPlace,
        outboundPartialDate=outboundPartialDate,
        inboundPartialDate='',  #One way flight only
        apiKey=APIKEY,
    )

    req_format = req.format(**values)

    response = get(URL+req_format, headers=HEADER)

    json_data = json.loads(response.text)
    logging.debug(json_data)

    cheapest_quote = None

    for quote in json_data['Quotes']:
        if cheapest_quote is None or quote['MinPrice'] < cheapest_quote['MinPrice']:
            cheapest_quote = quote

    return cheapest_quote

# api_wrapper.get_cheapest_ariport('ES','UK-sky','PARI-sky','2017-11-05')
