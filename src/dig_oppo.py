import robin_stocks
from robin_stocks import *
import robin_stocks.robinhood as r
import os
import json
import time
import requests
from bs4 import BeautifulSoup    

def movers_top_url():
    return('https://api.robinhood.com/midlands/tags/tag/top-movers/')

def get_100_most_popular_url():
    return('https://api.robinhood.com/midlands/tags/tag/100-most-popular/')

def request_get(url, type):
    if type == 'regular':
        response = requests.get(url)
    elif type == 'soup':
        response = requests.get(url)
        response = BeautifulSoup(response.text, 'html.parser')
    return response

def dig_oppoturnity():
    url = get_100_most_popular_url()
    data = request_get(url, 'regular')
    data = data.json()
    most_popular_instruments_list = data.get('instruments', [])
    symbol_list = []
    for instrument_url in most_popular_instruments_list:
        instrument_data = request_get(instrument_url, 'regular').json()
        symbol = instrument_data.get('symbol')
        if symbol:
            symbol_list.append(symbol)
    return symbol_list