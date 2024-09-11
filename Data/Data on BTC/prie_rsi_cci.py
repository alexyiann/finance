# Plot the data with circled points
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='Actual Price')

# Circle oversold points
for index, row in oversold_points.iterrows():
    plt.plot(index, row['Close'], 'o', markersize=8, color='red', label='Oversold' if index == oversold_points.index[0] else "")

# Circle overbought points
for index, row in overbought_points.iterrows():
    plt.plot(index, row['Close'], 'o', markersize=8, color='green', label='Overbought' if index == overbought_points.index[0] else "")

plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('BTC-USD Price with Circled Points')
plt.legend()
plt.show()
