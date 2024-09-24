# Import necessary libraries
from datetime import datetime, timedelta
import pandas as pd
import backtrader as bt
import numpy as np
from arch import arch_model
from scipy.stats import norm
import matplotlib.pyplot as plt

# Black-Scholes formula
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Monte Carlo simulation for future prices
def monte_carlo(S, sigma, r, T, num_simulations):
    dt = 1 / 252  # Daily steps
    num_steps = int(T / dt)
    simulations = np.zeros((num_simulations, num_steps + 1))
    simulations[:, 0] = S
    for t in range(1, num_steps + 1):
        Z = np.random.normal(size=num_simulations)
        simulations[:, t] = simulations[:, t - 1] * np.exp(
            (r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z
        )
    return simulations[:, -1]

# GARCH-based volatility prediction
def predict_volatility(data):
    if len(data) < 2:
        return 0.0  # Handle insufficient data
    returns = data.pct_change().dropna() * 100
    if len(returns) < 2:
        return 0.0  # Handle insufficient return data
    model = arch_model(returns, vol='Garch', p=1, q=1)
    fit = model.fit(disp="off")
    return fit.forecast(horizon=1).variance.iloc[-1] ** 0.5

# Calculate CVaR
def calculate_cvar(returns, confidence_level=0.05):
    if len(returns) == 0:
        return np.nan
    sorted_returns = np.sort(returns)
    index = int(confidence_level * len(sorted_returns))
    return sorted_returns[:index].mean()  # CVaR is the average of losses below VaR

# Calculate Sharpe Ratio
def calculate_sharpe_ratio(returns, risk_free_rate=0.03):
    if len(returns) == 0:
        return np.nan
    excess_returns = np.array(returns) - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns) if np.std(excess_returns) != 0 else np.nan

# Define Backtrader Strategy
class SimpleStrategy(bt.Strategy):
    params = (
        ('r', 0.03),
        ('stop_loss', 0.04),
        ('take_profit', 0.1),
        ('num_simulations', 1000),
        ('initial_position_size', 1000),
    )

    def __init__(self):
        self.historical_data = []
        self.entry_price = None

    def next(self):
        current_price = self.datas[0].close[0]
        self.historical_data.append(current_price)

        if len(self.historical_data) < 30:
            return  # Wait for enough data
        
        # Predict volatility
        volatility_forecast = predict_volatility(pd.Series(self.historical_data))

        if self.entry_price is None:
            self.entry_price = current_price
            self.buy(size=self.params.initial_position_size)

        elif current_price > self.entry_price * (1 + self.params.take_profit):
            self.sell(size=self.params.initial_position_size)
            self.entry_price = None

        elif current_price < self.entry_price * (1 - self.params.stop_loss):
            self.sell(size=self.params.initial_position_size)
            self.entry_price = None

    def stop(self):
        print("Strategy completed.")

# Initialize cerebro
cerebro = bt.Cerebro()

# Load data
data = bt.feeds.GenericCSVData(
    dataname='your_data.csv',  # Replace with your data file
    fromdate=datetime(2015, 1, 1),
    todate=datetime(2024, 9, 19),
    dtformat=('%Y-%m-%d'),
    timeframe=bt.TimeFrame.Days,
    compression=1,
    openinterest=-1
)
cerebro.adddata(data)

# Set initial cash
initial_cash = 100000
cerebro.broker.set_cash(initial_cash)

# Add strategy
cerebro.addstrategy(SimpleStrategy)

# Run the backtest
results = cerebro.run()
