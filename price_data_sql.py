from sqlalchemy import Date, Column, Integer, String

from base_sql import Base


class CryptoPrice(Base):
    __tablename__ = "crypto"

    id = Column(Integer, primary_key=True)
    crypto_name = Column(String(90))
