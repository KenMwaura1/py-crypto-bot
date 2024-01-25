from sqlalchemy import Date, Column, Integer, String, Float

from base_sql import Base

#         closed = candle['c']
#         open = candle['o']
#         high = candle['h']
#         low = candle['l']
#         volume = candle['v']


class CryptoPrice(Base):
    __tablename__ = "crypto"

    id = Column(Integer, primary_key=True)
    crypto_name = Column(String(90))
    close_price = Column(Float())
    open_price = Column(Float())
    high_price = Column(Float())
    low_price = Column(Float())
    volume = Column(Float())
    time = Column(Date())

    def __int__(self, crypto_name, close_price, open_price, high_price, low_price, volume, time):
        self.crypto_name = crypto_name
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.volume = volume
        self.time = time
