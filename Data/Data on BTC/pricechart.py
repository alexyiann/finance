# prompt: add the price data on a regression line , exclude rsi and cci , point out equilibrium price and predict future equilibrium , show price values on y axis every 5,000$

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

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
