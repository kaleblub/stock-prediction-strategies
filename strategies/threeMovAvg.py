'''Description: This program uses the three moving average 
crossover strategy to determine when to buy and sell stock'''

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

# bynd = np.genfromtxt('BYND.csv', delimiter=",", names=["Date", "Close"])

'''CALCULATE THE THREE MOVING AVERAGES'''
# Calculate the short/fast exponential moving average
ShortEMA = df.Close.ewm(span=8, adjust=False).mean()
# Calculate the middle/medium exponential moving average
MiddleEMA = df.Close.ewm(span=34, adjust=False).mean()
# Calculate the long/slow exponential moving average
LongEMA = df.Close.ewm(span=89,adjust=False).mean()


# # Visually show the close price
# plt.figure(figsize=(12.5, 7))
# plt.title('Close Price', fontsize = 18)
# plt.plot(df['Close'], label='Close Price', color='blue')
# plt.plot(ShortEMA, label='Short/Fast EMA', color='green')
# plt.plot(MiddleEMA, label='Middle/Medium EMA', color='orange')
# plt.plot(LongEMA, label='Long/Slow EMA', color='red')
# plt.xlabel('Date', fontsize = 18)
# plt.ylabel('Close Price', fontsize = 18)
# plt.show()


# Add the exponential moving averages to the data set
df['Short'] = ShortEMA
df['Medium'] = MiddleEMA
df['Long'] = LongEMA

print(df)

# Create the function to buy and sell the stock
def buy_sell_function(data):
	buy_list = []
	sell_list = []
	flag_long = False
	flag_short = False

	for i in range(0, len(data)):
		if data['Medium'][i] < data['Long'][i] and data['Short'][i] < data['Medium'][i] and flag_long == False and flag_short == False:
			buy_list.append(data['Close'][i])
			sell_list.append(np.nan)
			flag_short = True
		elif flag_short == True and data['Short'][i] > data['Medium'][i]:
			sell_list.append(data['Close'][i])
			buy_list.append(np.nan)
			flag_short = False
		elif data['Medium'][i] > data['Long'][i] and data['Short'][i] > data['Medium'][i] and flag_long == False and flag_short == False:
			buy_list.append(data['Close'][i])
			sell_list.append(np.nan)
			flag_long = True
		elif flag_long == True and data['Short'][i] < data['Medium'][i]:
			sell_list.append(data['Close'][i])
			buy_list.append(np.nan)
			flag_long = False
		else:
			buy_list.append(np.nan)
			sell_list.append(np.nan)

	return(buy_list, sell_list)

# Add the buy and sell signals to the data set
df['Buy'] = buy_sell_function(df)[0]
df['Sell'] = buy_sell_function(df)[1]

# Check the total return of the data set
total_return = 0.0
BUYS = df.loc[df.loc[:, 'Buy'] > 0, 'Buy']
SELLS = df.loc[df.loc[:, 'Sell'] > 0, 'Sell']
BUY_SELL_CYCLE = len(SELLS)
print("BUYS ARE:", BUYS, "SELLS ARE:", SELLS)
for each in range(BUY_SELL_CYCLE):
	b = BUYS[each]
	s = SELLS[each]
	total_return -= b
	print("Bought at", b)
	print("Account balance is now:", total_return)
	total_return += s
	print("Sold at", s)
	print("Account balance is now:", total_return, "\n")
print("Total =", total_return)




# Visually show the stock buy and sell signals
plt.figure(figsize=(12.5, 7))
plt.title('Buy and Sell Plot', fontsize = 18)
plt.plot(df['Close'], label='Close Price', color='blue', alpha=0.35)
plt.plot(ShortEMA, label='Short/Fast EMA', color='green', alpha=0.35)
plt.plot(MiddleEMA, label='Middle/Medium EMA', color='orange', alpha=0.35)
plt.plot(LongEMA, label='Long/Slow EMA', color='red', alpha=0.35)
plt.scatter(df.index, df['Buy'], color='green', marker='^', alpha=1)
plt.scatter(df.index, df['Sell'], color='red', marker='v', alpha=1)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Close Price', fontsize = 18)
plt.show()