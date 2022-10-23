import os

import websocket as wb
from pprint import pprint
import json
# import talib
import numpy as np
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
from datetime import datetime

from base_sql import Base, engine, Session
from price_data_sql import CryptoPrice

load_dotenv()

# 1 generate database schema
Base.metadata.create_all(engine)

# 2 Create a new session
session = Session()

BINANCE_SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"
TRADE_SIZE = 0.05
closed_prices = []
in_position = False

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
client = Client(API_KEY, API_SECRET, tld='us')


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
        pprint(f"high: {high}")
        pprint(f"low: {low}")
        pprint(f"volume: {volume}")
        closed_prices.append(float(closed))
        # create price entries
        print(TRADE_SYMBOL)
        crypto = CryptoPrice(crypto_name=TRADE_SYMBOL, open_price=open, close_price=closed,
                             high_price=high, low_price=low, volume=volume, time=datetime.utcnow())
        # print(crypto.time, crypto.crypto_name, crypto.close_price, crypto.open_price, crypto.volume,
        # crypto.high_price, crypto.low_price)
        try:
            session.add(crypto)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
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
ws.run_forever()
