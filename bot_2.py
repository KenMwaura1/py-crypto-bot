import os
import websocket as wb
from pprint import pprint
import json
import redis
import os
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
from datetime import datetime
from database_insert import create_table
from base_sql import Session
from price_data_sql import CryptoPrice

load_dotenv()

# connect to Redis
r = redis.Redis(host="localhost", port=6379, db=0)

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


def order(side, size, order_type=Client.ORDER_TYPE_MARKET, symbol=TRADE_SYMBOL):
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
    print("connection opened")


def on_close(ws):
    print("closed connection")


def on_error(ws, error):
    print(error)


def on_message(ws, message):
    message = json.loads(message)
    session = Session()
    # pprint(message)
    candle = message["data"]["k"]
    pprint(candle)
    trade_symbol = candle["s"]
    is_candle_closed = candle["x"]
    global closed_prices
    # if is_candle_closed:
    symbol = candle["s"]
    closed = candle["c"]
    open = candle["o"]
    high = candle["h"]
    low = candle["l"]
    volume = candle["v"]
    pprint(f"closed: {closed}")
    pprint(f"open: {open}")
    pprint(f"high: {high}")
    pprint(f"low: {low}")
    pprint(f"volume: {volume}")
    closed_prices.append(float(closed))
    # create price entries
    print(trade_symbol)
    crypto = CryptoPrice(
        crypto_name=symbol,
        open_price=float(open),
        close_price=float(closed),
        high_price=float(high),
        low_price=float(low),
        volume=float(volume),
        time=datetime.utcnow(),
    )
    print(
        f"Time: {crypto.time}, Name: {crypto.crypto_name}, Close Price: {crypto.close_price}, Open Price: {crypto.open_price}, Volume: {crypto.volume}"
    )

    with session.open() as session:
        try:
            session.add(crypto)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            session.close()

    # add message to Redis queue
    message_data = {
        "symbol": symbol,
        "open_price": open,
        "close_price": closed,
        "high_price": high,
        "low_price": low,
        "volume": volume,
        "time": str(crypto.time),
    }
    r.lpush("crypto", json.dumps(message_data))
    print(closed_prices)


# create a WebSocketApp instance
ws = wb.WebSocketApp(BINANCE_SOCKET, on_open=on_open, on_close=on_close, on_error=on_error, on_message=on_message)

# run the WebSocket connection in a separate thread
ws.run_forever()
