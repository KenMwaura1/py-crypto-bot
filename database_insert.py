from base_sql import engine, Base, Session


def create_table():
    # create a new session
    session = Session()
    # attempts to create the base tables and populate the db in a session. in case of an issue rolls back the session
    try:
        # Generate schema
        Base.metadata.create_all(engine)
        session.commit()
        print(f"connected & db populated")
    except Exception as e:
        session.rollback()
        print(e)

    session.close()
