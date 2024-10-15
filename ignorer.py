import asyncio
import websockets
import datetime as dt
import json

stages = ['Behavior check', 
          'Get working zone',
          'Get ignored size',
          'Accumulate working size',
          'Push down',
          'Place ignored size',
          '']

# class ignorer():

