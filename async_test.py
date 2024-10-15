import asyncio
import websockets
import datetime as dt
import json


ws_url = "wss://wbs.mexc.com/ws"

async def ws_connection():
    
    async with websockets.connect(ws_url) as ws:
        print("Connected: " + dt.datetime.now().isoformat())

        symbol = "XODEXUSDT"
        subscribe = {
                "method": "SUBSCRIPTION",
                "params": [
                    f"spot@public.deals.v3.api@{symbol}"
                ]
        }
        await ws.send(json.dumps(subscribe))

        async for msg in ws:
            print(msg)
        
        # await ws.send()
    print("Disconnected: " + dt.datetime.now().isoformat())

# Name	Type	Description
# deals	array	dealsInfo
# > S	int	    tradeType 1:buy 2:sell
# > p	string	price
# > t	long	dealTime
# > v	string	quantity
# e	    string	eventType
# s	    string	symbol
# t	    long	eventTime
def parse_deals_msg(msg):
    msg = json.loads(msg)



if __name__ == "__main__":
    print("Hello")
    asyncio.run(ws_connection())
    # asyncio.get_event_loop().run_until_complete(listen_trades())

