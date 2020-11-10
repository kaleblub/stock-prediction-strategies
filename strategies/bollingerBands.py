#Import the libraries
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
plt.style.use('fivethirtyeight')

# Store the csv data into a variable
df = pd.read_csv('../data/BTC-USD.csv') # BYND.csv, BTC-USD.csv

# Set the index to the Dates
df = df.set_index(pd.DatetimeIndex(df['Date'].values))

# Show the data
print(df)

# Calculate the simple moving average, standard deviation, upper band and lower band
# Get the time period (20 day)
period = 21
# Calculate the Simple Moving Average (SMA)
df['SMA'] = df['Close'].rolling(window=period).mean()
# Get the standard deviation
df['STD'] = df['Close'].rolling(window=period).std()
# Calculate the upper Bollinger band
df['Upper'] = df['SMA'] + (df['STD'] * 2)
# Calculate the lower Bollinger band
df['Lower'] = df['SMA'] - (df['STD'] * 2)

# Create a list of columns to keep
column_list = ['Close', 'SMA', 'Upper', 'Lower']
# plot the data
df[column_list].plot(figsize=(12.2, 6.4))
plt.title('Bollinger Band')
plt.ylabel('USD Price ($)')
plt.show()

# Plot and shade the area between the two Bollinger bands
# Get the figure and the figure size
fig = plt.figure(figsize=(12.2, 6.4))
# Add the subplot
ax = fig.add_subplot(1,1,1)
# Get the index values of the data frame
x_axis = df.index
# Plot and shade the area between the upper band and the lower band grey
ax.fill_between(x_axis, df['Upper'], df['Lower'], color = 'grey')
# Plot the closing price and the moving average
ax.plot(x_axis, df['Close'], color = 'gold', lw = 3, label = 'Close Price')
ax.plot(x_axis, df['SMA'], color = 'blue', lw = 3, label = 'Simple Moving Average')
# Set the title and show the image
ax.set_title('Bollinger Band')
ax.set_xlabel('Date')
ax.set_ylabel('USD Price ($)')
plt.xticks(rotation = 45)
ax.legend()
plt.show()

# Create a new data frame
new_df = df[period-1:]
# Show the new data
new_df

# Create a function to get the buy and sell signals
def get_signal(data):
	buy_signal = []
	sell_signal = []

	for i in range(len(data['Close'])):
		if data['Close'][i] > data['Upper'][i]: #Then you should sell
			buy_signal.append(np.nan)
			sell_signal.append(data['Close'][i])
		elif data['Close'][i] < data['Lower'][i]: #Then you should buy
			buy_signal.append(data['Close'][i]) 
			sell_signal.append(np.nan)
		else:
			buy_signal.append(np.nan)
			sell_signal.append(np.nan)

	return (buy_signal, sell_signal)

# Create two new columns
new_df['Buy'] = get_signal(new_df)[0]
new_df['Sell'] = get_signal(new_df)[1]

# Plot all of the data
# Get the figure and the figure size
fig = plt.figure(figsize=(12.2, 6.4))
# Add the subplot
ax = fig.add_subplot(1,1,1)
# Get the index values of the data frame
x_axis = new_df.index
# Plot and shade the area between the upper band and the lower band grey
ax.fill_between(x_axis, new_df['Upper'], new_df['Lower'], color = 'grey')
# Plot the closing price and the moving average
ax.plot(x_axis, new_df['Close'], color = 'gold', lw = 3, label = 'Close Price', alpha = 0.5)
ax.plot(x_axis, new_df['SMA'], color = 'blue', lw = 3, label = 'Simple Moving Average', alpha = 0.5)
ax.scatter(x_axis, new_df['Buy'], color = 'green', lw = 3, label = 'Buy', marker = '^', alpha = 1)
ax.scatter(x_axis, new_df['Sell'], color = 'red', lw = 3, label = 'Sell', marker = 'v', alpha = 1)
# Set the title and show the image
ax.set_title('Bollinger Band')
ax.set_xlabel('Date')
ax.set_ylabel('USD Price ($)')
plt.xticks(rotation = 45)
ax.legend()
plt.show()







