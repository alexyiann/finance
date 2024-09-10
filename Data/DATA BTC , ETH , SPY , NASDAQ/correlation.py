#PART A
# prompt: pull btc , eth , spy , nasdaq price the last 5 years using yfinance library and save each ticker data in a .csv file

!pip install yfinance

import yfinance as yf
import pandas as pd

# Define the tickers
tickers = ["BTC-USD", "ETH-USD", "SPY", "^IXIC"]

# Define the start and end dates
start_date = "2018-01-01"
end_date = "2023-01-01"

# Loop through the tickers and download data
for ticker in tickers:
  data = yf.download(ticker, start=start_date, end=end_date)

  # Save the data to a CSV file
  filename = f"{ticker}.csv"
  data.to_csv(filename)
  print(f"Data for {ticker} saved to {filename}")


#PART B

# prompt: use the following code and createa a matrix chart with the above ticker : from pandas.tools.plotting import scatter_matrix
# sm = scatter_matrix(Train, figsize=(10, 10))

import yfinance as yf
import pandas as pd
from pandas.plotting import scatter_matrix

!pip install yfinance


# Define the tickers
tickers = ['BTC-USD', 'ETH-USD', 'SPY', '^IXIC']

# Define the start and end dates
start_date = '2020-04-01'
end_date = '2023-04-01'

# Download the data for each ticker
data_frames = []
for ticker in tickers:
  data = yf.download(ticker, start=start_date, end=end_date)

  # Save the data to a CSV file
  data.to_csv(f'{ticker}.csv')
  data_frames.append(data['Close'])

# Combine dataframes into one
df = pd.concat(data_frames, axis=1)
df.columns = tickers

# Create the scatter matrix
sm = scatter_matrix(df, figsize=(10, 10))

#PART C
# prompt: # From the above tickers find the one with largest correlation and most negative correlation

import numpy as np
# Calculate the correlation matrix
corr_matrix = df.corr()

# Find the largest correlation excluding diagonal values
corr_matrix = corr_matrix.mask(np.equal(*np.indices(corr_matrix.shape)))
max_corr = corr_matrix.max().max()
max_corr_tickers = corr_matrix[corr_matrix == max_corr].stack().idxmax()

# Find the most negative correlation excluding diagonal values
min_corr = corr_matrix.min().min()
min_corr_tickers = corr_matrix[corr_matrix == min_corr].stack().idxmin()

print(f"Largest correlation: {max_corr} between {max_corr_tickers}")
print(f"Most negative correlation: {min_corr} between {min_corr_tickers}")


#PART D

# Example DataFrame creation (Replace this with your actual data loading process)
# df = pd.read_csv('your_data_file.csv')  # Load your data

# Ensure 'df' is a DataFrame and not a view
df = df.copy()

# Create lagged SPY data if needed
df['SPY_lag1'] = df['SPY'].shift(1)

# Drop rows with NaN values (from the shift operation or otherwise)
df = df.dropna()

# Rename columns to remove special characters
df = df.rename(columns={'BTC-USD': 'BTC_USD', 'ETH-USD': 'ETH_USD', '^IXIC': 'IXIC', 'SPY': 'SPY'})

# Calculate the correlation matrix
correlation_matrix = df[['BTC_USD', 'ETH_USD', 'SPY', 'IXIC']].corr()

# Print the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)


#PART E

import pandas as pd

# Example DataFrame creation (Replace this with your actual data loading process)
# df = pd.read_csv('your_data_file.csv')  # Load your data

# Ensure 'df' is a DataFrame and not a view
df = df.copy()

# Create lagged variables for each asset
df['BTC_USD_lag1'] = df['BTC_USD'].shift(1)
df['ETH_USD_lag1'] = df['ETH_USD'].shift(1)
df['SPY_lag1'] = df['SPY'].shift(1)
df['IXIC_lag1'] = df['IXIC'].shift(1)

# Drop rows with NaN values (from the shift operation or otherwise)
df = df.dropna()

# Rename columns to ensure consistent naming (already handled if not using special characters)
# df = df.rename(columns={'BTC-USD': 'BTC_USD', 'ETH-USD': 'ETH_USD', '^IXIC': 'IXIC', 'SPY': 'SPY'}) # If needed

# Calculate the correlation matrix including lagged variables
correlation_matrix = df[['BTC_USD', 'ETH_USD', 'SPY', 'IXIC',
                         'BTC_USD_lag1', 'ETH_USD_lag1', 'SPY_lag1', 'IXIC_lag1']].corr()

# Print the correlation matrix
print("Correlation Matrix including lagged variables:")
print(correlation_matrix)

#PART F

import pandas as pd
import statsmodels.formula.api as smf

# Example DataFrame creation (Replace this with your actual data loading process)
# df = pd.read_csv('your_data_file.csv')  # Load your data

# Ensure 'df' is a DataFrame and not a view
df = df.copy()

# Create lagged variables for each asset
df['BTC_USD_lag1'] = df['BTC_USD'].shift(1)
df['ETH_USD_lag1'] = df['ETH_USD'].shift(1)
df['SPY_lag1'] = df['SPY'].shift(1)
df['IXIC_lag1'] = df['IXIC'].shift(1)

# Drop rows with NaN values (from the shift operation or otherwise)
df = df.dropna()

# Define asset pairs to compare
asset_pairs = [
    ('BTC_USD', 'ETH_USD'),
    ('BTC_USD', 'SPY'),
    ('BTC_USD', 'IXIC'),
    ('ETH_USD', 'SPY'),
    ('ETH_USD', 'IXIC'),
    ('SPY', 'IXIC')
]

# Run regressions for each pair and print results
for asset1, asset2 in asset_pairs:
    # Construct the formula
    formula = f'{asset1} ~ {asset2} + {asset2}_lag1'

    # Fit the model
    model = smf.ols(formula=formula, data=df).fit()

    # Print the summary
    print(f"\nRegression results for {asset1} ~ {asset2} and {asset2}_lag1:")
    print(model.summary())

#PART G

import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

# Example DataFrame creation (Replace this with your actual data loading process)
# df = pd.read_csv('your_data_file.csv')  # Load your data

# Ensure 'df' is a DataFrame and not a view
df = df.copy()

# Create lagged variables for each asset
df['BTC_USD_lag1'] = df['BTC_USD'].shift(1)
df['ETH_USD_lag1'] = df['ETH_USD'].shift(1)
df['SPY_lag1'] = df['SPY'].shift(1)
df['IXIC_lag1'] = df['IXIC'].shift(1)

# Drop rows with NaN values (from the shift operation or otherwise)
df = df.dropna()

# Define asset pairs to compare
asset_pairs = [
    ('BTC_USD', 'ETH_USD'),
    ('BTC_USD', 'SPY'),
    ('BTC_USD', 'IXIC'),
    ('ETH_USD', 'SPY'),
    ('ETH_USD', 'IXIC'),
    ('SPY', 'IXIC')
]

# Assume Train and Test are predefined DataFrames for training and testing
# For demonstration, splitting the DataFrame into Train and Test (replace with your actual split)
train_size = int(0.8 * len(df))
Train = df.iloc[:train_size]
Test = df.iloc[train_size:]

# Define evaluation metrics functions
def adjustedMetric(data, model, model_k, yname):
    data['yhat'] = model.predict(data)
    SST = ((data[yname] - data[yname].mean())**2).sum()
    SSR = ((data['yhat'] - data[yname].mean())**2).sum()
    SSE = ((data[yname] - data['yhat'])**2).sum()
    r2 = SSR / SST
    adjustR2 = 1 - (1 - r2) * (data.shape[0] - 1) / (data.shape[0] - model_k - 1)
    RMSE = (SSE / (data.shape[0] - model_k - 1))**0.5
    return adjustR2, RMSE

def assessTable(test, train, model, model_k, yname):
    r2test, RMSEtest = adjustedMetric(test, model, model_k, yname)
    r2train, RMSEtrain = adjustedMetric(train, model, model_k, yname)
    assessment = pd.DataFrame(index=['R2', 'RMSE'], columns=['Train', 'Test'])
    assessment['Train'] = [r2train, RMSEtrain]
    assessment['Test'] = [r2test, RMSEtest]
    return assessment

# Run regressions for each pair, predict, and plot results
for asset1, asset2 in asset_pairs:
    # Construct the formula
    formula = f'{asset1} ~ {asset2} + {asset2}_lag1'

    # Fit the model
    lm = smf.ols(formula=formula, data=Train).fit()

    # Predict values for Train and Test
    Train['PredictedY'] = lm.predict(Train)
    Test['PredictedY'] = lm.predict(Test)

    # Plot actual vs predicted values for Train
    plt.figure(figsize=(10, 5))
    plt.scatter(Train[asset1], Train['PredictedY'], label='Train Data', alpha=0.6)
    plt.xlabel(f'Actual {asset1}')
    plt.ylabel('Predicted Values')
    plt.title(f'Actual vs Predicted Values for {asset1} using {asset2}')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot actual vs predicted values for Test
    plt.figure(figsize=(10, 5))
    plt.scatter(Test[asset1], Test['PredictedY'], label='Test Data', alpha=0.6)
    plt.xlabel(f'Actual {asset1}')
    plt.ylabel('Predicted Values')
    plt.title(f'Actual vs Predicted Values for {asset1} using {asset2}')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Get the assessment table for the model
    assessment = assessTable(Test, Train, lm, len(lm.params) - 1, asset1)
    print(f"\nAssessment Table for {asset1} ~ {asset2}:")
    print(assessment)
