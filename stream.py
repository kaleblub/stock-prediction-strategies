import websocket, json
from config import *

# 
def on_open(ws):
	print("opened")
	auth_data = {
		"action": "authenticate",
		"data": {"key_id": ALPACA_API_KEY_ID, "secret_key": ALPACA_SECRET_KEY}
	}

	ws.send(json.dumps(auth_data))

	listen_message = {"action": "listen", "data": {"streams": ["T.TSLA", "T.APPL", "T.MSFT"]}}

	ws.send(json.dumps(listen_message))


def on_message(ws, message):
	print("received a message")
	print(message)

def on_close(ws):
	print("closed connection")


socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()


#{"action": "authenticate", "data": {"key_id": ALPACA_API_KEY_ID, "secret_key": ALPACA_SECRET_KEY}}
#