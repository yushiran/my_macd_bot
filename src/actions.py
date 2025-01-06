import robin_stocks
from robin_stocks import *
from datetime import datetime
import time
import robin_stocks.robinhood as r


def buy_stock_with_stop_loss(symbol='TSLA', money:float =1, stop_loss_radio:float=0.0025, take_profit_radio=0.005):
    # 购买股票
    # 获取当前股票市场价格
    current_price = float(r.stocks.get_latest_price(symbol)[0])
    print(f"Current market price for {symbol}: {current_price}")

    # 计算购买数量
    quantity = round(money / current_price, 2)

    # 计算止损和止盈价格
    stop_loss_price = round(current_price * (1 - stop_loss_radio), 2)
    take_profit_price = round(current_price * (1 + take_profit_radio), 2)

    buy_order =  r.order_buy_fractional_by_price(symbol=symbol,amountInDollars=money)
    
    if buy_order:
        print(f"Buy order placed: {buy_order}")    
        # 获取持有的股票数量
        positions_data = r.account.build_holdings()
        if symbol in positions_data:
            owned_quantity = float(positions_data[symbol]['quantity'])
            print(f"Owned quantity of {symbol}: {owned_quantity}")
        else:
            print(f"No holdings found for {symbol}")
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            current_price = float(r.stocks.get_latest_price(symbol)[0])
            if datetime.now().second % 60 == 0:
                print(f"Current time: {current_time}, {symbol} current price {current_price}, stop loss price {stop_loss_price}, take profit price {take_profit_price}")
                time.sleep(1)
            if current_price <= stop_loss_price:
                print(f"Stop loss triggered for {symbol}")
                r.order_sell_fractional_by_quantity(symbol, owned_quantity)
                break
            elif current_price >= take_profit_price:
                print(f"Take profit triggered for {symbol}")
                r.order_sell_fractional_by_quantity(symbol, owned_quantity)
                break
    else:
        print(f"Buy order failed for {symbol}")

    print("finish the buy_stock_with_stop_loss")



if __name__ == '__main__':
    buy_stock_with_stop_loss('TSLA', 1, 0.005, 0.01)