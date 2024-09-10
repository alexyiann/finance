import time
import re
import threading
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from helpers import initialise_exchange_object, get_webdriver_instance
from helpers import market_order, limit_order

exchange = initialise_exchange_object()

Variables to change
##########################################################

driver = get_webdriver_instance(headless=True)

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

Navigate to the website
driver.get("https://news.treeofalpha.com/")
while True:
    news_elements = driver.find_elements(By.XPATH, '//div[@class="contentWrapper column gap-small"]')
    news_elements_found_timestamp = time.time()

    for news_element in news_elements:
        try:
            headline = news_element.find_element(By.XPATH, './/h2[@class="contentTitle"]').text

            if headline not in headlines_processed:
                print(f"Headline: {headline}, Timestamp: {time.time()}")
                print(f"----------------------------------------")
                headlines_processed.append(headline)

                # If this is a new article and the headline starts with "U.S.", check for numbers
                if headline.startswith("U.S."):
                    # Search for the first number in the headline
                    match = re.search(r'\d+.?\d*', headline)
                    if match:
                        inflation = float(match.group())
                        print(f"Inflation is: {inflation}")

                        if inflation <= 5.6:
                            if place_market_order:
                                for order in long_orders:
                                    threading.Thread(target=market_order,
                                                     args=(exchange, order, news_elements_found_timestamp)).start()
                            else:
                                for order in long_orders:
                                    threading.Thread(target=limit_order,
                                                     args=(
                                                     exchange, order, slippage, news_elements_found_timestamp, True))

                        elif inflation >= 5.8:
                            if place_market_order:
                                for order in short_orders:
                                    threading.Thread(target=market_order,
                                                     args=(exchange, order, news_elements_found_timestamp)).start()
                            else:
                                for order in short_orders:
                                    threading.Thread(target=limit_order,
                                                     args=(
                                                     exchange, order, slippage, news_elements_found_timestamp, False))
                    else:
                        print("No number found in the headline")
                        continue

        except NoSuchElementException:
            print("Inflation not found, skipping...")
            continue
        except StaleElementReferenceException:
            continue

    print("Waiting...")
    time.sleep(1)
