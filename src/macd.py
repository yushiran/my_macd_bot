import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURRENT_DIR, '..'))
from src.stock_msg import get_stock_history_prices
import time
 
def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
    """
    计算MACD指标
    :param prices: 股票价格的时间序列
    :param short_window: 短期EMA窗口
    :param long_window: 长期EMA窗口
    :param signal_window: 信号线窗口
    :return: MACD线, 信号线, 柱状图
    """
    # 计算短期和长期EMA
    short_ema = prices.ewm(span=short_window, adjust=False).mean()
    long_ema = prices.ewm(span=long_window, adjust=False).mean()
    
    # 计算MACD线
    macd_line = short_ema - long_ema
    
    # 计算信号线
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    
    # 计算柱状图
    macd_histogram = macd_line - signal_line
    
    return macd_line, signal_line, macd_histogram
 

def update_macd(stock_name: str = 'TSLA', time_period: str = '1d', interval:str = '1m'):
    stock_prices = get_stock_history_prices(stock_name, time_period, interval)
    # Calculate MACD
    macd, signal, macd_histogram = calculate_macd(stock_prices)
    # Plot stock prices and MACD
    # plt.figure(figsize=(14, 7))
    
    # # Plot stock prices
    # plt.subplot(2, 1, 1)
    # plt.plot(stock_prices, label='Stock Prices')
    # plt.title(f'{stock_name} Stock Prices')
    # plt.xlabel('Date')
    # plt.xticks(rotation=45)
    # plt.ylabel('Price')
    # plt.legend()
    
    # # Plot MACD
    # plt.subplot(2, 1, 2)
    # plt.plot(macd, label='MACD Line', color='blue')
    # plt.plot(signal, label='Signal Line', color='red')
    # bar_colors = ['green' if val >= 0 else 'red' for val in macd_histogram]
    # plt.bar(macd_histogram.index, macd_histogram, label='MACD Histogram', color=bar_colors)
    # plt.title('MACD')
    # plt.xlabel('Date')
    # plt.xticks(rotation=45)
    # plt.ylabel('Value')
    # plt.legend()
    
    # plt.tight_layout()
    # plt.show()

    return macd, signal, macd_histogram

if __name__ == '__main__':
    update_macd()