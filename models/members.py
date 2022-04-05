from .helpers.db_connect import Base, engine, Session
from sqlalchemy import Column, String, Integer


class Alderperson(Base):
    """Table of past and present city council members."""

    __tablename__ = "alderpersons"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        """Class constructor: id, name"""

        # self.id = id
        self.name = name

    def __repr__(self):
        """Represent alderperson object as <id, name>"""

        alderperson = self
        return f"<Alderperson {alderperson.id} {alderperson.name}>"
