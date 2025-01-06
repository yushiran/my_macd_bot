import robin_stocks
from robin_stocks import *
import robin_stocks.robinhood as r
import pyotp
from dotenv import load_dotenv
load_dotenv()
import os
import json
import threading
# Simple credential specifications - a better method is mentioned
# in the docs.
USERNAME = os.getenv("RH_USERNAME")
PASSWORD = os.getenv("RH_PASSWORD")
alphanumeric_code = os.getenv("alphanumeric_code")

from src import *
import src.macd as macd
import src.actions as actions
import src.impulse_macd as impulse_macd
import src.dig_oppo as dig_oppo
import src.stock_msg as stock_msg

def main():
    totp  = pyotp.TOTP(alphanumeric_code).now()
    print(totp)
    login = r.login(USERNAME, PASSWORD, mfa_code=totp)

    dig_oppo_list = dig_oppo.dig_oppoturnity()
    valid_stocks = []
    for stock in dig_oppo_list:
        stock_prices = stock_msg.get_stock_history_data(stock, '1d', '1m')
        if not stock_prices.empty:
            valid_stocks.append(stock)
    dig_oppo_list = valid_stocks
    print(dig_oppo_list)

    threading_list = []
    for symbol in dig_oppo_list:
        threading_list.append(threading.Thread(target=impulse_macd.impusle_main, args=(symbol,)))

    for thread in threading_list:
        thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        r.logout()
        print("Exiting...")

if __name__ == '__main__':
    main()