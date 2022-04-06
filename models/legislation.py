from .helpers.db_connect import Base, engine, Session
from sqlalchemy import Column, String, Integer


class Legislation(Base):
    """Table of City Council legislation."""

    __tablename__ = "legislation"

    id = Column(Integer, autoincrement=True, primary_key=True)
    record_num = Column(String)
    type = Column(String)
    title = Column(String)
    result = Column(String)
    action_text = Column(String)
    mtg_date = Column(String)

    def __init__(self, record_num, type, title, result, action_text, mtg_date):
        """Class constructor: type, title, result, action_text, mtg_date."""

        self.record_num = record_num
        self.type = type
        self.title = title
        self.result = result
        self.action_text = action_text
        self.mtg_date = mtg_date

    def __repr__(self):
        """Represent legislation object as <id, record_num, mtg_date>."""

        legislation = self
        return f"<Legislation {legislation.id} {legislation.record_num} {legislation.mtg_date}>"
