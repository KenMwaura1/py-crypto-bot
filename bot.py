import websocket as wb
from pprint import pprint
import json

BINANCE_SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"


def on_open(ws):
    # ws.send("{'event':'addChannel','channel':'ethusdt@kline_1m'}")
    print("connected")


def on_close(ws):
    print("closed connection")


def on_error(ws, error):
    print(error)


def on_message(ws, message):
    message = json.loads(message)
    pprint(message)
    candle = message['k']
    is_candle_closed = candle['x']
    if is_candle_closed:
        closed = candle['c']
        open = candle['o']
        high = candle['h']
        low = candle['l']
        volume = candle['v']
        pprint(f"closed: {closed}")


ws = wb.WebSocketApp(BINANCE_SOCKET, on_open=on_open, on_close=on_close, on_error=on_error, on_message=on_message)
ws.run_forever()
