import websocket as wb
from pprint import pprint
import json
import talib
import numpy as np

BINANCE_SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"
TRADE_SIZE = 0.05
closed_prices = []


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
    global closed_prices
    if is_candle_closed:
        closed = candle['c']
        open = candle['o']
        high = candle['h']
        low = candle['l']
        volume = candle['v']
        pprint(f"closed: {closed}")
        pprint(f"open: {open}")
        closed_prices.append(closed)

        if len(closed_prices) > RSI_PERIOD:
            closed_prices.pop(0)
        rsi = talib.RSI(np.array(closed_prices), RSI_PERIOD)[-1]
        pprint(f"rsi: {rsi}")

        if rsi > RSI_OVERBOUGHT:
            print("overbought")
            ws.send(json.dumps({"method": "order", "params": {"symbol": TRADE_SYMBOL, "side": "BUY", "type": "LIMIT", "timeInForce": "GTC", "quantity": TRADE_SIZE, "price": open}, "id": 1}))
        elif rsi < RSI_OVERSOLD:
            print("oversold")
            ws.send(json.dumps({"method": "order", "params": {"symbol": TRADE_SYMBOL, "side": "SELL", "type": "LIMIT", "timeInForce": "GTC", "quantity": TRADE_SIZE, "price": open}, "id": 1}))

        closed_prices = []


ws = wb.WebSocketApp(BINANCE_SOCKET, on_open=on_open, on_close=on_close, on_error=on_error, on_message=on_message)
ws.run_forever()
