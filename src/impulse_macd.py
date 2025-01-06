import pandas as pd
import numpy as np
import os
from os import environ as env
from dotenv import load_dotenv
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURRENT_DIR, '..'))
from src.stock_msg import get_stock_history_prices,get_stock_history_data
import src.actions as actions
import time
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


# Define SMMA calculation
def calc_smma(src: pd.DataFrame, length: int) -> np.ndarray:
    smma = np.full_like(src, fill_value=np.nan)
    sma = pd.Series(src).rolling(window=length, min_periods=1).mean().to_numpy()
    for i in range(1, len(src)):
        smma[i] = (
            sma[i]
            if np.isnan(smma[i - 1])
            else (smma[i - 1] * (length - 1) + src[i]) / length
        )
    return smma

def calc_zlema(src: np.ndarray, length: int) -> np.ndarray:
    ema1 = pd.Series(src).ewm(span=length, adjust=False).mean()
    ema2 = pd.Series(ema1).ewm(span=length, adjust=False).mean()
    d = ema1 - ema2
    return ema1 + d

def impulse_macd_main(stock_name: str = 'TSLA', time_period: str = '1d', interval:str = '1m'):
    stock_prices = get_stock_history_data(stock_name, time_period, interval)

    # Define input parameters
    lengthMA = 34
    lengthSignal = 9

    # Calculate indicator values
    src = (stock_prices["High"] + stock_prices["Low"] + stock_prices["Close"]) / 3
    hi = calc_smma(stock_prices["High"].to_numpy(dtype=np.double), lengthMA)
    lo = calc_smma(stock_prices["Low"].to_numpy(dtype=np.double), lengthMA)
    mi = calc_zlema(src, lengthMA)

    md = np.full_like(mi, fill_value=np.nan)
    conditions = [mi > hi, mi < lo]
    choices = [mi - hi, mi - lo]
    md = np.select(conditions, choices, default=0)

    sb = pd.Series(md).rolling(window=lengthSignal, min_periods=1).mean().to_numpy()
    sh = md - sb

    ImpulseMACD = pd.Series(md, index=stock_prices.index)
    ImpulseHisto = pd.Series(sh, index=stock_prices.index)
    ImpulseMACDCDSignal = pd.Series(sb, index=stock_prices.index)

    # Plot stock prices and MACD
    # plt.figure(figsize=(14, 7))
    
    # # Plot stock prices
    # plt.subplot(2, 1, 1)
    # plt.plot(stock_prices.index, stock_prices["Close"], label='Stock Prices')
    # plt.title(f'{stock_name} Stock Prices')
    # plt.xlabel('Date')
    # plt.xticks(rotation=45)
    # plt.ylabel('Price')
    # plt.legend()
    
    # # Plot MACD
    # plt.subplot(2, 1, 2)
    # plt.plot(ImpulseMACD.index, ImpulseMACD, label='Impulse MACD', color='blue')
    # plt.plot(ImpulseMACDCDSignal.index, ImpulseMACDCDSignal, label='Signal Line', color='red')
    # bar_colors = ['green' if val >= 0 else 'red' for val in ImpulseHisto]
    # plt.bar(ImpulseHisto.index, ImpulseHisto, label='Histogram', color=bar_colors)
    # plt.title('Impulse MACD')
    # plt.xlabel('Date')
    # plt.xticks(rotation=45)
    # plt.ylabel('Value')
    # plt.legend()
    
    # plt.tight_layout()
    # save_path = f"{CURRENT_DIR}/../pic/{stock_name}"
    # if not os.path.exists(save_path):
    #     os.makedirs(save_path)
    # plt.savefig(f"{save_path}/{stock_name}_ImpulseMACD.png")
    # plt.show()
    return ImpulseMACD, ImpulseHisto, ImpulseMACDCDSignal

def check_signal(MACD: pd.Series,hist: pd.Series, signal: pd.Series):
    # breakpoint()
    if (hist.iloc[-1] > 0 and hist.iloc[-2] < 0) and signal.iloc[-1] > 0.75 *signal.max() and MACD.iloc[-1] > 0.75 * MACD.max():
        return True
    else:
        return False
    
def impusle_main(stock_name:str='TSLA'):
    while True:
        # print(f'{stock_name} Impulse MACD')
        ImpulseMACD, ImpulseHisto, ImpulseMACDCDSignal = impulse_macd_main(stock_name=stock_name, time_period='1d', interval='1m')
        
        if check_signal(ImpulseMACD,ImpulseHisto,ImpulseMACDCDSignal):
            print(f"Buy signal detected {time.strftime('%H:%M:%S', time.localtime())}")
            actions.buy_stock_with_stop_loss(stock_name, 1, 0.0025, 0.005)
            # break
        time.sleep(30)

if __name__ == '__main__':
    impulse_macd_main()