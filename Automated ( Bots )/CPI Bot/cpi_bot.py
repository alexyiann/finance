import sys
import websocket
import threading
import time
import json
import re
from helpers import initialiseexchange_object, market_order, limit_order
from secrets import TREE_NEWS_API_KEY

exchange = initialise_exchange_object()

Variables to change
##########################################################
long_orders = [
    ["BTCUSDT", "buy", 0.05],
    ["ETHUSDT", "buy", 0.2],
]

short_orders = [
    ["BTCUSDT", "sell", 0.025],
    ["ETHUSDT", "sell", 0.25],
]

place_market_order = True
slippage = 2
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
    # msg_source = msg.get('source')

    print(msg)

    # if msg_source == 'Binance EN': Would be nice to have
    msg_headline = msg.get('title')
    if msg_headline not in headlines_processed:
        print(f"Headline: {msg_headline}, Timestamp: {time.time()}")
        print(f"----------------------------------------")
        headlines_processed.append(msg_headline)

        # If this is a new article and the headline starts with "U.S.", check for numbers
        if msg_headline.startswith("U.S."):
            # Search for the first number in the headline
            match = re.search(r'\d+.?\d*', msg_headline)
            if match:
                inflation = float(match.group())
                print(f"Inflation is: {inflation}")

                if inflation <= 5.6:
                    if place_market_order:
                        for order in long_orders:
                            threading.Thread(target=market_order, args=(exchange, order, msg_timestamp)).start()
                    else:
                        for order in long_orders:
                            threading.Thread(target=limit_order,
                                             args=(exchange, order, slippage, msg_timestamp, True)).start()

                    sys.exit()

                elif inflation >= 5.8:
                    if place_market_order:
                        for order in short_orders:
                            threading.Thread(target=market_order,
                                             args=(exchange, order, msg_timestamp)).start()
                    else:
                        for order in short_orders:
                            threading.Thread(target=limit_order,
                                             args=(exchange, order, slippage, msg_timestamp, False)).start()

                    sys.exit()
            else:
                print("No number found in the headline")


ws = WS("wss://news.treeofalpha.com/ws", callback)
while True:
    time.sleep(1)
