import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

db = os.environ.get("DB")
# check if there is an
if db:
    db = db
else:
    db = "postgresql+psycopg2://test:testpassword@localhost:5432/price_data"
