import sys
import websocket
import threading
import time
import json
from helpers import initialiseexchange_object, market_order, limit_order, all_keywords_present
from secrets import TREE_NEWS_API_KEY

exchange = initialise_exchange_object()

Variables to change
##########################################################
orders = [
    ["BNBUSDT", "buy", 10],
]

Keywords to search for
keywords = ["Introducing", "Token Sale", "Binance", "Launchpad"]
place_market_order = True
slippage_protection = 2
##########################################################

headlines_processed = []


class WS():
    def init(self, ws_url, callback):
        self.ws_url = ws_url
        self.callback = callback
        self.WSCONNECTION = None
        threading.Thread(target=self.create_ws, daemon=True).start()

    def on_message(self, , msg):
        msg = json.loads(msg)
        if 'user' not in msg.keys():
            self.callback(msg)
        else:
            print(msg)

    def on_error(self, a, b):
        print(a, b)

    def on_close(self, a, b, c):
        print('Websocket closed - ' + self.ws_url)

    def on_open(self, e):
        print('Websocket opened - ' + self.ws_url)
        if 'treeofalpha' in self.ws_url:
            self.WSCONNECTION.send(f'login {TREE_NEWS_API_KEY}')

    def create_ws(self):
        while True:
            try:
                websocket.enableTrace(False)
                self.WSCONNECTION = websocket.WebSocketApp(self.ws_url, on_message=self.on_message,
                                                           on_error=self.on_error, on_close=self.on_close)
                self.WSCONNECTION.on_open = self.on_open
                self.WSCONNECTION.run_forever(skip_utf8_validation=True, ping_interval=10, ping_timeout=8)
            except Exception as e:
                print("Websocket connection Error  : {0}, restarting...".format(e))
            time.sleep(5)


def callback(msg):
    msg_timestamp = time.time()
    msg_source = msg.get('source')

    print(msg)

    if msg_source == 'Binance EN':
        msg_headline = msg.get('title')
        if msg_headline not in headlines_processed:
            print(f"Headline: {msg_headline}, Timestamp: {time.time()}")
            print(f"----------------------------------------")
            headlines_processed.append(msg_headline)

            # If this is a new article and all the keywords are in the headline, process it
            if all_keywords_present(msg_headline, keywords):
                print("Relevant News Article Found")

                if place_market_order:
                    for order in orders:
                        threading.Thread(target=market_order,
                                         args=(exchange, order, msg_timestamp)).start()
                else:
                    for order in orders:
                        threading.Thread(target=limit_order,
                                         args=(exchange, order, slippage_protection, msg_timestamp)).start()

                sys.exit()

ws = WS("wss://news.treeofalpha.com/ws", callback)
while True:
    time.sleep(1)
