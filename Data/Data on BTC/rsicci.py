# prompt: circle the points where CCI and RSI are both oversold and overbought , when RSI is above 75 and CCI above 150 , and when RSI is below 25 and CCI -150 

import matplotlib.pyplot as plt
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
