# Import necessary libraries
from datetime import datetime
import pandas as pd
import backtrader as bt
import numpy as np
import matplotlib.pyplot as plt

# Define a simple moving average crossover strategy
class SimpleMovingAverageStrategy(bt.Strategy):
    params = (
        ('short_window', 5),
        ('long_window', 20),
        ('initial_position_size', 1000),
    )

    def __init__(self):
        self.short_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_window)
        self.long_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_window)
        self.entry_price = None

    def next(self):
        if not self.position:  # Not in the market
            if self.short_sma > self.long_sma:  # Buy signal
                self.entry_price = self.data.close[0]
                self.buy(size=self.params.initial_position_size)
        else:  # In the market
            if self.short_sma < self.long_sma:  # Sell signal
                self.sell(size=self.params.initial_position_size)

    def stop(self):
        print(f'Final Portfolio Value: {self.broker.getvalue():.2f}')

# Initialize cerebro
cerebro = bt.Cerebro()

# Load data
data = bt.feeds.GenericCSVData(
    dataname='/path/to/your/data.csv',  # Change this to your data file
    fromdate=datetime(2015, 1, 1),
    todate=datetime(2024, 9, 19),
    dtformat=('%Y-%m-%d'),
    timeframe=bt.TimeFrame.Days,
    compression=1
)
cerebro.adddata(data)

# Set initial cash
initial_cash = 100000
cerebro.broker.set_cash(initial_cash)

# Add the strategy
cerebro.addstrategy(SimpleMovingAverageStrategy)

# Run the backtest
results = cerebro.run()

# Plot the results
cerebro.plot()
