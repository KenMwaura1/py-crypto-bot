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
in_position = False


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
        closed_prices.append(float(closed))

        if len(closed_prices) > RSI_PERIOD:
            # closed_prices.pop(0)
            all_rsi = talib.RSI(np.array(closed_prices), RSI_PERIOD)
            pprint(f"all_rsi: {all_rsi}")
            last_rsi = all_rsi[-1]
            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("overbought, already in position")
                    print("sell!")
                else:
                    print("overbought, but we dont have position")
                ws.send(json.dumps({
                    "event": "addChannel",
                    "channel": f"{TRADE_SYMBOL}@trade"
                }))
            elif last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("oversold but already in position")
                else:
                    print("buy!")
                ws.send(json.dumps({
                    "event": "addChannel",
                    "channel": f"{TRADE_SYMBOL}@trade"
                }))


ws = wb.WebSocketApp(BINANCE_SOCKET, on_open=on_open, on_close=on_close, on_error=on_error, on_message=on_message)
ws.run_forever()
