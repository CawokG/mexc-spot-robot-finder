import asyncio
import websockets
import datetime as dt
import json


class СounterIgnorer():


    def __init__(self, symbol, pushing_size = None, ignored_size = None):

        self.symbol = symbol
        self.pushing_size = pushing_size
        self.ignored_size = ignored_size
        self.upper_bound_ratio
        self.lower_bound_ratio

        self.preparation_stages = ['Behavior check', 
          'Get working zone boundaries',
          'Get ignored and pushing sizes',
          'Accumulate pushing size of tokens']
        self.working_stages = [
          'Push down with limit sell order of pushing size',
          'Place limit buy order of ignored size at upper bound of working range',
          'Wait for execution by bot',
          'Cancel pushing order',
          'Push up with limit buy order of pushing size',
          'Place limit sell order of ignored size at lower bound of working range',
          'Wait for execution by bot']

