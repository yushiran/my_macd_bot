import yfinance as yf
import pandas as pd

def get_stock_history_prices(stock_name: str = 'TSLA', time_period: str = '1d', interval:str = '1m'):
    """
        Fetches historical stock prices for a given stock symbol, time period, and interval.
        Args:
            stock_name (str): The stock symbol to fetch data for. Default is 'TSLA'.
            time_period (str): The time period for which to fetch data. Default is '1d'.
                               Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
            interval (str): The interval at which to fetch data. Default is '1m'.
        Returns:
            pandas.Series: A series containing the closing prices of the stock for the specified period and interval.
    """

    # Fetch AAPL stock data with a 1-hour timeframe
    aapl = yf.Ticker(stock_name)
    try:
        stock_data = aapl.history(period=time_period, interval=interval)  # Adjust the period as needed
    except Exception as e:
        print(f"Error fetching data for {stock_name}: {e}")
        return None

    stock_prices = stock_data['Close']
    if interval in ['1m', '2m', '5m', '15m', '30m', '1h'] and time_period in ['1d']:
        stock_prices.index = stock_prices.index.strftime('%H:%M')
    elif interval in ['1m', '2m', '5m', '15m', '30m', '1h'] :
        stock_prices.index = stock_prices.index.strftime('%Y-%m-%d-%H:%M')
    elif interval in ['1d', '5d'] or time_period not in ['1d']:
        stock_prices.index = stock_prices.index.strftime('%Y-%m-%d')
    elif interval in ['1wk', '1mo', '3mo']:
        stock_prices.index = stock_prices.index.strftime('%Y-%m-%d')
    return stock_prices
    print(stock_prices)

def get_stock_history_data(stock_name: str = 'TSLA', time_period: str = '1d', interval:str = '1m'):
    """
        Fetches historical stock prices for a given stock symbol, time period, and interval.
        Args:
            stock_name (str): The stock symbol to fetch data for. Default is 'TSLA'.
            time_period (str): The time period for which to fetch data. Default is '1d'.
                               Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
            interval (str): The interval at which to fetch data. Default is '1m'.
        Returns:
            pandas.Series: A series containing the closing prices of the stock for the specified period and interval.
    """

    # Fetch AAPL stock data with a 1-hour timeframe
    aapl = yf.Ticker(stock_name)
    stock_data = aapl.history(period=time_period, interval=interval)  # Adjust the period as needed

    stock_prices = stock_data
    if stock_prices.empty:
        print("Empty DataFrame")
        return stock_prices
    if interval in ['1m', '2m', '5m', '15m', '30m', '1h'] and time_period in ['1d']:
        stock_prices.index = stock_prices.index.strftime('%H:%M')
    elif interval in ['1m', '2m', '5m', '15m', '30m', '1h'] :
        stock_prices.index = stock_prices.index.strftime('%Y-%m-%d-%H:%M')
    elif interval in ['1d', '5d'] or time_period not in ['1d']:
        stock_prices.index = stock_prices.index.strftime('%Y-%m-%d')
    elif interval in ['1wk', '1mo', '3mo']:
        stock_prices.index = stock_prices.index.strftime('%Y-%m-%d')
    return stock_prices