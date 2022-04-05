from .helpers.db_connect import Base, engine, Session
from sqlalchemy import Column, String, Integer


class Meeting(Base):
    """Table of City Council meetings."""

    __tablename__ = "meetings"

    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(String)
    date = Column(String)
    time = Column(String)
    link = Column(String)

    def __init__(self, type, date, time, link):
        """Class constructor: type, date, time, link."""

        self.type = type
        self.date = date
        self.time = time
        self.link = link

    def __repr__(self):
        """Represent meeting object as <id, type, date>."""

        meeting = self
        return f"<Meeting {meeting.id} {meeting.type} {meeting.date}>"
