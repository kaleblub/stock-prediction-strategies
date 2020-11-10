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

'''CALCULATE THE TOP AND BOTTOM MOVING AVERAGES OF THE SSL CHANNEL'''
TopSSL = df.High.rolling(20, min_periods=10).mean()
BottomSSL = df.Low.rolling(20, min_periods=10).mean()





# # Check the total return of the data set
# total_return = 0.0
# BUYS = df.loc[df.loc[:, 'Buy'] > 0, 'Buy']
# SELLS = df.loc[df.loc[:, 'Sell'] > 0, 'Sell']
# BUY_SELL_CYCLE = len(SELLS)
# print("BUYS ARE:", BUYS, "SELLS ARE:", SELLS)
# for each in range(BUY_SELL_CYCLE):
# 	b = BUYS[each]
# 	s = SELLS[each]
# 	total_return -= b
# 	print("Bought at", b)
# 	print("Account balance is now:", total_return)
# 	total_return += s
# 	print("Sold at", s)
# 	print("Account balance is now:", total_return, "\n")
# print("Total =", total_return)




# Visually show the stock buy and sell signals
plt.figure(figsize=(12.5, 7))
plt.title('Buy and Sell Plot', fontsize = 18)
plt.plot(df['Close'], label='Close Price', color='blue', alpha=0.35)
plt.plot(TopSSL, label='Top SSL Moving Average', color='green', alpha=0.35)
plt.plot(BottomSSL, label='Bottom SSL Moving Average', color='red', alpha=0.35)
#plt.scatter(df.index, df['Buy'], color='green', marker='^', alpha=1)
#plt.scatter(df.index, df['Sell'], color='red', marker='v', alpha=1)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Close Price', fontsize = 18)
plt.show()