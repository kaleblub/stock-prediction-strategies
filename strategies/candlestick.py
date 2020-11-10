# Go to 1 hour chart
# Identify trend direction with SSL Channel (SSL is 2 SMAs, one of recent Highs, one of
# recent Lows)
# Go to the 5 minute chart
# Wait for price to return to the 50 EMA
# Wait for an entry signal (eg engulfing pattern)
# Enter trade with stop loss below/above recent high/low
# Take profit wherever suits you


# Trend Change Green line crosses above red line on 1 hour chart
# on 5 minute chart use 50 EMA and wait to cross under EMA with a 
# bullish engulfing (up candle is bigger than down candle)
# enter at the top of the bullish candle, set stop-loss below the berish candle and target
# above 
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

df = pd.read_csv('../data/BTC-USD.csv')

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

fig.show()