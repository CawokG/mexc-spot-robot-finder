import asyncio
import websockets
import datetime as dt
import json


class СounterIgnorer():

    def __init__(self, symbol, pushing_size = None, ignored_size = None, upper_bound_ratio = None, lower_bound_ratio = None):

        self.symbol = symbol
        self.pushing_size = pushing_size
        self.ignored_size = ignored_size
        self.upper_bound_ratio = upper_bound_ratio
        self.lower_bound_ratio = lower_bound_ratio

        self.preparation_stages = [
            'Behavior check', 
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
        self.current_stage = -1  # -1 means not started yet

        self.stages_functions = {}

    def next_stage(self):
        self.current_stage = (self.current_stage + 1) % len(self.working_stages)

    def get_stage(self):
        return self.current_stage

    def get_symbol(self):
        return self.symbol

    def get_current_stage_name(self):
        return self.working_stages[self.current_stage]


