import time
import numpy as np
import pandas as pd
from mexc_api.spot import Spot
from mexc_api.common.enums import Side, OrderType, StreamInterval, Action
from mexc_api.common.exceptions import MexcAPIError



def format_timestamp(timestamp: int) -> str:
    return time.ctime(timestamp / 1000)


def get_server_time_delta(spot: Spot):
    current_time = time.time()
    server_time = spot.market.server_time() / 1000
    return server_time - current_time


def get_spot_symbols(spot: Spot):
    data = spot.market.exchange_info()
    return [symbol['symbol'] for symbol in data['symbols'] if symbol['status'] == '1']


# returns ratio size of spread to first ask
def get_symbol_spread_ratio(spot: Spot, symbol: str):
    order_book = spot.market.order_book(symbol, limit=1)
    first_bid = order_book['bids'][0][0]
    first_ask = order_book['asks'][0][0]
    return (first_bid - first_ask) / first_ask


def get_squeeze_price(spot: Spot, volume: float, bids_or_asks: list[list[float, float]]):
    bank = volume
    for order in bids_or_asks:
        bank -= order[0] * order[1]
        if bank < 0:
            return order[0]
    return bids_or_asks[-1][0]


def get_symbol_spread_ratio_by_volume(spot: Spot, symbol: str, volume: float, limit=100):
    order_book = spot.market.order_book(symbol, limit=limit)
    bid_price = get_squeeze_price(volume, order_book['bids'])
    ask_price = get_squeeze_price(volume, order_book['asks'])
    return (bid_price - ask_price) / ask_price


# def get_symbol_trades() -> list[]
