ReadMe

Installing Dependencies

pip install -r requirements.txt
API Keys & Secrets

The secrets.py contains all the API Keys & Secrets.
secrets.py Format

BINANCE_API_KEY = ""
BINANCE_SECRET_KEY = ""

Instructions

Add your Binance API & Secret Keys to secrets.py.
Choose if you would like a browser window to open or not while running the script with the headless variable in the get_webdriver_instance method. If True a browser window does not open.
Modify the long_orders and short_orders using the format provided to your preferences.
Choose if you would like to place a market order using the place_marker_order variable. If False then a limit order will be used.
Choose slippage using the slippage variable. Do not enter a % sign. This is only used when placing limit orders.
