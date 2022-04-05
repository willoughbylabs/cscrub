from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2:///cscrub", future=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


def create_tables():
    """Create tables in PostgreSQL database."""

    try:
        Base.metadata.create_all(engine)
        print("Tables created.")
    except Exception as e:
        print("Error occured. Unable to create tables.", e)
        return
