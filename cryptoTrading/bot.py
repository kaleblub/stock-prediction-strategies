import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

#											ethusdt
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
HOUR_SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1h"

# 8, 13 ,21, 55 EMA = Exponential Moving Average = 




# Relative Strength Index = 100 - (100/1+RS)
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "BTC"
TRADE_QUANTITY = 0.05
# RS = AVG GAIN / AVG LOSS


closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET, tld='us')

def order(symbol, quantity, side, order_type=ORDER_TYPE_MARKET):
	try:
		print("sending order")
		order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
		print(order)
		return True
	except Exception as e:
		return False

	return True

def on_open(ws):
	print('opened connection')
	auth_data = {
		"action":"authenticate",
		"data":{"key_id":config.API_KEY, "secret_key":config.API_SECRET}
	}

def on_close(ws):
	print('closed connection')

def on_message(ws, message):
	global closes
	print('received message')
	print(message)
	json_message = json.loads(message)
	pprint.pprint(json_message)

	candle = json_message['k']

	is_candle_closed = candle['x']
	close = candle['c']

	if is_candle_closed:
		print("candle closed at {}".format(close))
		closes.append(float(close))
		print("closes")
		print(closes)

		if len(closes) > RSI_PERIOD:
			np_closes = numpy.array(closes)
			rsi = talib.RSI(np_closes, RSI_PERIOD)
			print("All rsis calculated so far")
			print(rsi)
			last_rsi = rsi[-1]
			print("The current rsi is {}".format(last_rsi))

			if last_rsi > RSI_OVERBOUGHT:
				if in_position:
					print("Sell! Sell! Sell!")
					# put binance sell logic here
					order_succeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
					if order_succeded:
						in_position = False
				else:
					print("It is overbought, but we don't own any. Nothing to do")

			if last_rsi < RSI_OVERSOLD:
				if in_position:
					print("It is oversold, but you already own it. Nothing to do.")
				else:
					print("Buy! Buy! Buy!")
					# put binance buy order logic here
					order_succeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
					if order_succeded:
						in_position = True


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()