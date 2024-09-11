# prompt: now combine the code , so when i run the code i get both charts at the same time 

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

!pip install pandas
!pip install yfinance


# Define the ticker symbol
ticker = "BTC-USD"

# Define the date range (last 4 years)
end_date = pd.Timestamp.today()
start_date = end_date - pd.DateOffset(years=4)

# Download the data
data = yf.download(ticker, start=start_date, end=end_date)

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

# Calculate CCI
def CCI(data, window):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    sma = typical_price.rolling(window).mean()
    mad = (typical_price - sma).abs().rolling(window).mean()
    cci = (typical_price - sma) / (0.015 * mad)
    return cci

# Calculate CCI with a window of 20
data['CCI'] = CCI(data, 20)

# Select relevant columns
data_for_regression = data[['Close']]

# Prepare data for regression
X = np.arange(len(data_for_regression)).reshape(-1, 1)
y = data_for_regression['Close'].values.reshape(-1, 1)

# Fit linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict values
y_pred = model.predict(X)

# Find equilibrium price
equilibrium_price = y_pred[-1][0]

# Predict future equilibrium (assuming a constant trend)
future_equilibrium = y_pred[-1][0] + (y_pred[-1][0] - y_pred[-2][0])

# Plot the data and regression line
plt.figure(figsize=(12, 6))
plt.plot(data_for_regression.index, data_for_regression['Close'], label='Actual Price')
plt.plot(data_for_regression.index, y_pred, color='red', label='Regression Line')

# Set y-axis ticks every 5000
plt.yticks(np.arange(data_for_regression['Close'].min() // 5000 * 5000, 
                      data_for_regression['Close'].max() // 5000 * 5000 + 5000, 
                      5000))

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('BTC-USD Price with Regression Line')

# Add equilibrium price annotation
plt.axhline(y=equilibrium_price, color='green', linestyle='--', label='Current Equilibrium Price')
plt.text(data_for_regression.index[-1], equilibrium_price, f'{equilibrium_price:.2f}', 
         color='green', ha='left', va='bottom')

# Add predicted future equilibrium annotation
plt.text(data_for_regression.index[-1], future_equilibrium, f'Predicted Future Equilibrium: {future_equilibrium:.2f}', 
         color='blue', ha='left', va='top')

# Show legend
plt.legend()
plt.show()

# Plot RSI and CCI
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['RSI'], label='RSI')
plt.plot(data.index, data['CCI'] / 100, label='CCI (scaled)')  # Scale CCI for better visualization
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('RSI and CCI')
plt.legend()
plt.show()


# Find points where RSI and CCI are both oversold
oversold_points = data[(data['RSI'] < 25) & (data['CCI'] < -150)]

# Find points where RSI and CCI are both overbought
overbought_points = data[(data['RSI'] > 75) & (data['CCI'] > 150)]

# Print the results
print("Oversold points:")
print(oversold_points)

print("\nOverbought points:")
print(overbought_points)

# Plot the data with circled points
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['RSI'], label='RSI')
plt.plot(data.index, data['CCI'] / 100, label='CCI (scaled)')  # Scale CCI for better visualization

# Circle oversold points
for index, row in oversold_points.iterrows():
  plt.plot(index, row['RSI'], 'o', markersize=8, color='red')

# Circle overbought points
for index, row in overbought_points.iterrows():
  plt.plot(index, row['RSI'], 'o', markersize=8, color='green')

plt.xlabel('Date')
plt.ylabel('Value')
plt.title('RSI and CCI with Circled Points')
plt.legend()
plt.show()
