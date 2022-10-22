from base_sql import engine, Base, Session
from price_data_sql import CryptoPrice

# Generate schema


# create a new session
session = Session()
# attempts to create the base tables and populate the db in a session. in case of an issue rolls back the session
try:
    session.add(Base.metadata.create_all(engine))
    session.autocommit()
    print(f"connected & db populated: {session}")
except Exception as e:
    # session.autoflush()
    session.rollback()
    print(e)

session.close()
