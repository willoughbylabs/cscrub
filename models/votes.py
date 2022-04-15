import re
from models.helpers import wd_connect
from .helpers.db_connect import Base, engine, Session
from sqlalchemy import Column, Integer, String, extract


class Vote(Base):
    """Table of city council members' votes on legislation."""

    __tablename__ = "votes"

    id = Column(Integer, autoincrement=True, primary_key=True)
    record_num = Column(String)
    name = Column(String)
    vote = Column(String)

    def __init__(self, record_num, name, vote):
        """Class constructor: record_num, name, vote."""

        self.record_num = record_num
        self.name = name
        self.vote = vote

    def __repr__(self):
        """Represent vote object as <id, name, vote>."""

        vote = self
        return f"<Vote {vote.record_num} {vote.name} {vote.vote}>"
