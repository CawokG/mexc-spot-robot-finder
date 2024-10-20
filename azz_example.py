"""
!!! ******** Поддержи канал на https://boosty.to/azzrael Спасибо ******** !!!
https://www.youtube.com/@AzzraelCode

https://pypi.org/project/websockets/
https://websockets.readthedocs.io/en/7.0/api.html
https://www.okx.com/docs-v5/en/#overview-websocket
"""
import asyncio
import base64
import hmac
import json
import logging
import os
from datetime import datetime
import websockets

# OKX API Websocket Logging  https://youtu.be/F7VNi_V0rMU
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# OKX KEYS  https://youtu.be/E4Y7SWBylBQ
# ENV VARS  https://youtu.be/E6lGUnUYGKU
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
API_PASSPHARSE = os.getenv('API_PASSPHARSE')

def sign(key : str, secret : str, passphrase : str):
    """
    Подпись для авторизации юзера в ранее подключенном вебсокете
    https://www.okx.com/docs-v5/en/#overview-websocket-login
    :return:
    """
    # время дб точным, е с точным локальным временем проблемы, то можно брать servertime от api
    # The request will expire 30 seconds after the timestamp. If your server time differs from the API server time,
    # we recommended using the REST API to query the API server time and then set the timestamp.
    ts = str(int(datetime.now().timestamp()))
    args = dict(apiKey=key, passphrase=passphrase, timestamp=ts)
    sign = ts + 'GET' + '/users/self/verify'
    mac = hmac.new(bytes(secret, encoding='utf8'), bytes(sign, encoding='utf-8'), digestmod='sha256')
    args['sign'] = base64.b64encode(mac.digest()).decode(encoding='utf-8')
    return args

async def send(ws, op : str, args : list):
    """
    Обертка для отправки сообщение в Вебсокет subscribe, unsubscribe, login, order ...
    ws = ресурс
    """
    subs = dict(op=op, args=args)
    await ws.send(json.dumps(subs))


async def azz_ws():
    """
    Основная фн для работы с Вебсокетом
    :return:
    """
    url = 'wss://ws.okx.com:8443/ws/v5/private'

    # ! Реконнекты
    # Этот способ отличается от способа описанного в пред видео https://youtu.be/F7VNi_V0rMU
    # он лучше тем что не использует рекурсию, и описан как рекомендуемый в документации
    # https://websockets.readthedocs.io/en/stable/faq/client.html#how-do-i-reconnect-when-the-connection-drops
    async for ws in websockets.connect(url):
        print("Connected " + datetime.now().isoformat())
        try:

            login_args : dict = sign(API_KEY, API_SECRET, API_PASSPHARSE)
            await send(ws, 'login', [login_args])

            # OKX API Websocket Connecting https://youtu.be/YCEMCVWiSH0
            async for msg_string in ws:
                try:

                    m = json.loads(msg_string)
                    ev = m.get('event')
                    data = m.get('data')

                    if ev == 'error':
                        print("Error ", msg_string)
                    elif ev in ['subscribe', 'unsubscribe']:
                        print("subscribe/unsubscribe ", msg_string)
                    elif ev == 'login':
                        print('Ur Logged in')
                        # ! Подписка только после Авторизации
                        # https://www.okx.com/docs-v5/en/#order-book-trading-trade-ws-order-channel
                        await send(ws, 'subscribe', [
                            dict(channel='orders', instType='SPOT'),
                            dict(channel='positions', instType='ANY'),
                        ])
                    elif data:
                        print(data)

                except Exception as e:
                    print(e)

            print("((( Connection Finished" + datetime.now().isoformat())

        except (websockets.ConnectionClosed, websockets.ConnectionClosedError) as e:
            print("((( ConnectionClosed " + datetime.now().isoformat())
            await asyncio.sleep(3)
            continue
        except asyncio.CancelledError as e:
            print("* Соединение остановлено вручную "+ datetime.now().isoformat())
            break


"""
Точка входа
"""
if __name__ == '__main__':
    print(f"Hola, AzzraelCode YouTube Subs!")
    asyncio.run(azz_ws())

