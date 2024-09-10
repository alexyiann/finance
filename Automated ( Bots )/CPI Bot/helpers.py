import ccxt
import time
from pprint import pprint
from selenium import webdriver
from secrets import BINANCE_API_KEY, BINANCE_SECRET_KEY


def get_webdriver_instance(headless):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if headless:
        options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(50)

    return driver


def initialise_exchange_object():
    # Initialize the  exchange object
    exchange = ccxt.binanceusdm({
        'apiKey': BINANCE_API_KEY,
        'secret': BINANCE_SECRET_KEY,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
            'adjustForTimeDifference': True,
        },
    })

    exchange.load_markets()
    balance = exchange.fetch_balance()
    positions = balance['info']['positions']
    exchange.verbose = True
    pprint(positions)

    return exchange


def market_order(exchange, order, relevant_elements_found_timestamp):
    try:
        exchange.create_market_order(order[0], order[1], order[2])

        print("Market Order in process...")
        print(f"Time Taken From Processing Till Placing Order: {time.time() - relevant_elements_found_timestamp}")
    except Exception as e:
        print(f"Error during order creation: {e}")


def limit_order(exchange, order, slippage, relevant_elements_found_timestamp, long):
    try:
        price = exchange.fetch_ticker(order[0])['last']
        if long:
            order_price = price * ((100 + slippage) / 100)
        else:
            order_price = price * ((100 - slippage) / 100)
        exchange.create_limit_order(order[0], order[1], order[2], order_price)

        print("Limit Order in process...")
        print(f"Time Taken From Processing Till Placing Order: {time.time() - relevant_elements_found_timestamp}")
    except Exception as e:
        print(f"Error during order creation: {e}")
