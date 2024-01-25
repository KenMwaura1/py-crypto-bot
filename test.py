# crypto_bot.py
import os
import json
import websocket
from dotenv import load_dotenv
from binance import BinanceSocketManager
from binance.client import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

# load environment variables
load_dotenv()

# create engine
engine = create_engine(os.getenv("DB"))

# create session
Session = sessionmaker(bind=engine)
session = Session()

# create base
Base = declarative_base()


# create table
class Crypto(Base):
    __tablename__ = "crypto"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    price = Column(Float)
    time = Column(DateTime)


# create table if it does not exist
Base.metadata.create_all(engine)

# create client
client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))

# create socket manager
bm = BinanceSocketManager(client)


# process message
def process_message(msg):
    print(msg)
    if msg["e"] == "error":
        print(msg["m"])
        return
    symbol = msg["s"]
    price = float(msg["c"])
    time = msg["E"]
    crypto = Crypto(symbol=symbol, price=price, time=time)
    session.add(crypto)
    session.commit()
    session.close()  # close session after each message


# create socket
socket = bm.symbol_ticker_socket("BTCUSDT")

# start socket
bm.start()

# close socket
bm.close()
