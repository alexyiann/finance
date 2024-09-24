# Install required libraries
# prompt: pull all avaialble apple price data from 2015 up to now , name the file apple_price_data.csv

import yfinance as yf
from datetime import datetime

# Define the ticker symbol for Apple
ticker = "AAPL"

# Define the start and end dates for the data
start_date = "2015-01-01"
end_date = datetime.now().strftime("%Y-%m-%d")

# Download the historical data
data = yf.download(ticker, start=start_date, end=end_date)

# Save the data to a CSV file
data.to_csv("apple_price_data.csv")
