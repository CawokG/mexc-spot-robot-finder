import time
import numpy as np
import pandas as pd
from mexc_api.spot import Spot
from mexc_api.websocket import SpotWebsocketStreamClient
from mexc_api.common.enums import Side, OrderType, StreamInterval, Action
from mexc_api.common.exceptions import MexcAPIError
import utils

KEY = ""
SECRET = ""

spot = Spot(KEY, SECRET)


# for symbol in spot.market.exchange_info(symbols=['BTCUSDT', 'ETHUSDT', 'MXUSDT'])['symbols']:
#     print(symbol['symbol'], symbol['status'])


def get_robot_timing(symbol: str, limit=100):
    trades = spot.market.trades(symbol, limit)
    df = pd.DataFrame(trades)
    df = df.groupby('quoteQty', as_index=False).sum()

symbols = utils.get_spot_symbols(spot)
books = spot.market.ticker_book_price()

# dataset = pd.merge(pd.DataFrame(symbols), pd.DataFrame(books), on='ID', how='outer')

# for trade in trades:
#     print(f"{trade['quoteQty']} at {time.ctime(trade['time'])}")

# order_book = spot.market.order_book("MXUSDT", limit=2)
# print(order_book)

# trading_symbols = get_spot_symbols()
# with open('mexc_spot_symbols.txt', 'w') as f:
#     f.writelines(f"{symbol}\n" for symbol in trading_symbols)

# print("Tradable symbols on MEXC spot:")
# for symbol in trading_symbols:
#     print(symbol)
