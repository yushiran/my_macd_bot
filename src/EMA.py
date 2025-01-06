import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURRENT_DIR, '..'))
from src.stock_msg import get_stock_history_prices

def calculate_ema(stock_prices, period):
    ema_values = stock_prices.ewm(span=period, adjust=False).mean()
    return ema_values


if __name__ == '__main__':
    # Get historical stock prices for Tesla
    stock_prices = get_stock_history_prices('TSLA', '1d', '5m')
    
    # Calculate the EMA for the stock prices
    ema_values = calculate_ema(stock_prices, 200)

    print(ema_values)