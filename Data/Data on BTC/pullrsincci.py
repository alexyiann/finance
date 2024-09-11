# prompt: pull the cci data for the same range , combine the codes

import yfinance as yf
import pandas as pd

!pip install pandas
!pip install yfinance


# Define the ticker symbol
ticker = "BTC-USD"

# Define the date range (last 4 years)
end_date = pd.Timestamp.today()
start_date = end_date - pd.DateOffset(years=4)

# Download the data
data = yf.download(ticker, start=start_date, end=end_date)

# Print the data
print(data)


# Calculate RSI
def RSI(data, window):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate RSI with a window of 14
data['RSI'] = RSI(data, 14)

# Print the data with RSI
print(data)

# Calculate CCI
def CCI(data, window):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    sma = typical_price.rolling(window).mean()
    mad = (typical_price - sma).abs().rolling(window).mean()
    cci = (typical_price - sma) / (0.015 * mad)
    return cci

# Calculate CCI with a window of 20
data['CCI'] = CCI(data, 20)

# Print the data with CCI
print(data)
