from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

engine = create_engine("postgresql+psycopg2:///cscrub", future=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


def create_tables():
    """Create tables in PostgreSQL database."""

    try:
        Base.metadata.create_all(engine)
        print("Tables created.")
        return
    except Exception as e:
        print("Error occured. Unable to create tables.", e)


def reset_table(table):
    """Resets the autoincrementing index count for a table."""

    statement = text(f"ALTER SEQUENCE {table}_id_seq RESTART")
    with engine.begin() as connection:
        connection.execute(statement)
    return
