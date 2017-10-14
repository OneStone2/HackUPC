#!/usr/bin/env python3

import requests
import json

import logging

URL = 'http://partners.api.skyscanner.net/apiservices'

CURRENCY='EUR'
LOCALE='US_en'
COUNTRY='ES'

APIKEY = 'ha731738434387524676454915828415'

HEADER = {'Accept' : 'application/json'}

def live_flight(originPlace, destinationPlace, outboundDate, adults=1, children=0, infants=0):
    pass


def save_geo_info():

    req = '/geo/v1.0?apiKey={apiKey}'

    values = dict(
        apiKey=APIKEY
        )

    req_format = req.format(**values)

    response = requests.get(URL+req_format, headers=HEADER)

    if response.status_code != 200:
        print('request returned code:', response.status_code)
        return None

    # json_data = json.loads(response.text)
    # logging.debug(json_data)
    
    # return json.loads(response.text)
    with open('cities.json', 'w') as myfile:
       myfile.write(response.text)

    # return json_data

def get_link(originPlace, destinationPlace, outboundPartialDate):
    """
    :return: chapest flight from airport originPlace, to airport
    destinationPlace on date outboundPartialDate

    :rtype: dict = {price=price, quote=cheapest_quote}
    """

    req = '/referral/v1.0/{country}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={shortApiKey}'

    values = dict(
        country=COUNTRY,
        currency=CURRENCY,
        locale=LOCALE,
        originPlace=originPlace,
        destinationPlace=destinationPlace,
        outboundPartialDate=outboundPartialDate,
        inboundPartialDate='',  #One way flight only
        shortApiKey=APIKEY[:16],
    )
    

    req_format = req.format(**values)
    

    response = requests.get(URL+req_format, headers=HEADER)

    return response.url

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

    response = requests.get(URL+req_format, headers=HEADER)

    json_data = json.loads(response.text)
    logging.debug(json_data)

    return json_data

def get_carrier(carriers, carrierId):
    for carrier in carriers:
        if carrier['CarrierId'] == carrierId:
            return carrier['Name']
    return None

def get_place(places, placeId):
    for place in places:
        if place['PlaceId'] == placeId:
            return place['Name']
    return None

def query_flight(originPlace, destinationPlace, outboundPartialDate):
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
    print(URL+req_format)
    response = requests.get(URL+req_format, headers=HEADER)
    if response.status_code != 200:
        print('request returned code:', response.status_code)
        return None

    return json.loads(response.text)

def query_and_find_cheapest(originPlace, destinationPlace, outboundPartialDate):
    json_data = query_flight(originPlace, destinationPlace, outboundPartialDate)
    return find_cheapest(json_data)

def find_cheapest(json_data):
    cheapest_quote = None
    
    if json_data is None:
        return None
    
    for quote in json_data['Quotes']:
        if (cheapest_quote is None or quote['MinPrice'] < cheapest_quote['MinPrice']) and (quote['OutboundLeg']['CarrierIds']):
            cheapest_quote = quote
    
    if cheapest_quote is None:
        return None
        
    carriers = json_data['Carriers']
    places = json_data['Places']
	
    carrier = get_carrier(carriers, cheapest_quote['OutboundLeg']['CarrierIds'][0])
    destination = get_place(places, cheapest_quote['OutboundLeg']['DestinationId'])
    origin = get_place(places, cheapest_quote['OutboundLeg']['OriginId'])

    return dict(
        price=cheapest_quote['MinPrice'],
        departure=cheapest_quote['OutboundLeg']['DepartureDate'],
        carrier=carrier,
        origin=origin,
        destination=destination,
    )

def set_country(country):
    with open('countries_list.json', 'r') as countries:
       json_data = json.load(countries)
       global COUNTRY
       COUNTRY = json_data[country]
