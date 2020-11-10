import requests, json, websocket
from config import *


#import pyotp
#import robin_stocks as r
#totp = pyotp.TOTP("946689 131880")

# URLs To Send Requests To
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(APCA_API_BASE_URL)
ORDERS_URL = "{}/v2/orders".format(APCA_API_BASE_URL)
HEADERS = {'APCA-API-KEY-ID': ALPACA_API_KEY_ID, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY}

def get_account():
	r = requests.get(ACCOUNT_URL, headers=HEADERS)

	return json.loads(r.content)

def create_order(symbol, qty, side, type, time_in_force):
	data = {
		"symbol": symbol,
		"qty": qty,
		"side": side,
		"type": type,
		"time_in_force": time_in_force
	}

	r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

	return json.loads(r.content)

def get_orders():
	r = requests.get(ORDERS_URL, headers=HEADERS)

	return json.loads(r.content)


#response = create_order("AAPL", 100, "buy", "market", "gtc")
#response = create_order("MSFT", 100, "buy", "market", "gtc")

orders = get_orders()

account = get_account()
print(account["account_number"])