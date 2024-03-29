import os
import websocket as wb
from pprint import pprint
import json

# import talib
# import numpy as np
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
from datetime import datetime
from database_insert import create_table
from base_sql import Session
from price_data_sql import CryptoPrice

load_dotenv()

# this functions creates the table if it does not exist
create_table()

# create a session
session = Session()

BINANCE_SOCKET = "wss://stream.binance.com:9443/stream?streams=ethusdt@kline_3m/btcusdt@kline_3m"
B_S = "wss://stream.binance.com:9443/stream?streams=btcusdt@aggTrade/btcusdt@depth"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"
TRADE_SIZE = 0.05
closed_prices = []
in_position = False

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
client = Client(API_KEY, API_SECRET, tld="us")


def order(side, size, order_type=ORDER_TYPE_MARKET, symbol=TRADE_SYMBOL):
    # order_type = "MARKET" if side == "buy" else "LIMIT"
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=size,
        )
        print(order)
        return True
    except Exception as e:
        print(e)
        return False


def on_open(ws):
    # ws.send("{'event':'addChannel','channel':'ethusdt@kline_1m'}")
    print("connection opened")


def on_close(ws):
    print("closed connection")


def on_error(ws, error):
    print(error)


def on_message(ws, message):
    message = json.loads(message)
    # pprint(message)
    candle = message["data"]["k"]
    pprint(candle)
    trade_symbol = candle["s"]
    is_candle_closed = candle["x"]
    global closed_prices
    # if is_candle_closed:
    symbol = candle["s"]
    pprint(symbol)
    closed = candle["c"]
    open = candle["o"]
    high = candle["h"]
    low = candle["l"]
    volume = candle["v"]
    interval = candle["i"]
    pprint(f"closed: {closed}")
    pprint(f"open: {open}")
    pprint(f"high: {high}")
    pprint(f"low: {low}")
    pprint(f"volume: {volume}")
    pprint(f"interval: {interval}")
    pprint(f"is_candle_closed: {is_candle_closed}")
    closed_prices.append(float(closed))
    # create price entries
    # print(TRADE_SYMBOL)
    crypto = CryptoPrice(
        crypto_name=symbol,
        open_price=open,
        close_price=closed,
        high_price=high,
        low_price=low,
        volume=volume,
        time=datetime.utcnow(),
    )
    # print(crypto.time, crypto.crypto_name, crypto.close_price, crypto.open_price, crypto.volume,
    # crypto.high_price, crypto.low_price)
    session.add(crypto)
    session.commit()
    session.close()


"""
        if len(closed_prices) > RSI_PERIOD:
            # closed_prices.pop(0)
            all_rsi = talib.RSI(np.array(closed_prices), RSI_PERIOD)
            pprint(f"all_rsi: {all_rsi}")
            last_rsi = all_rsi[-1]
            if last_rsi > RSI_OVERBOUGHT:
                global in_position
                if in_position:
                    print("Overbought, sell!")
                    success = order(SIDE_SELL, TRADE_SIZE, ORDER_TYPE_MARKET, TRADE_SYMBOL)
                    if success:
                        in_position = False

                else:
                    print("overbought, but we dont have position")
            elif last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("oversold but already in position")
                else:
                    print("buy!")
                    success = order(SIDE_BUY, TRADE_SIZE, ORDER_TYPE_MARKET, TRADE_SYMBOL)
                    if success:
                        in_position = True

"""


ws = wb.WebSocketApp(BINANCE_SOCKET, on_open=on_open, on_close=on_close, on_error=on_error, on_message=on_message)
# ws1 = wb.WebSocketApp(B_S, on_open=on_open, on_close=on_close, on_error=on_error, on_message=on_message)
ws.run_forever()
# ws1.run_forever()
