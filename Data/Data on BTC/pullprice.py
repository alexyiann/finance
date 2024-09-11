# prompt: pull btc price last 4 years

!pip install pandas
!pip install yfinance

import yfinance as yf
import pandas as pd

# Define the ticker symbol
ticker = "BTC-USD"

# Define the date range (last 4 years)
end_date = pd.Timestamp.today()
start_date = end_date - pd.DateOffset(years=4)

# Download the data
data = yf.download(ticker, start=start_date, end=end_date)

# Print the data
print(data)
