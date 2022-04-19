from .helpers.db_connect import Base, engine, Session, reset_table
from .helpers.wd_connect import fetch_rss_entries
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

    @classmethod
    def fetch_meetings(cls):
        """Fetch City Council meetings from City Clierk calendar RSS feed."""

        try:
            url = "https://chicago.legistar.com/Feed.ashx?M=Calendar&ID=13369895&GUID=d03e61f9-1d04-47cf-96d1-772746fcb39a&Mode=All&Title=Office+of+the+City+Clerk+-+Calendar+(All)"
            entries = fetch_rss_entries(url, "meetings")
            meetings = map(cls.map_meetings, entries)
            return list(meetings)
        except Exception as e:
            print(
                "Error occurred. Unable to fetch City Council meetings from City Clerk RSS feed.",
                e,
            )

    @classmethod
    def map_meetings(cls, entry):
        """Accepts an entry from the RSS calendar feed, and returns a dictionary of parsed information: {type, date, time, link}."""

        try:
            meeting = cls.split_meeting_title(entry.title)
            meeting["link"] = entry.link
            return meeting
        except Exception as e:
            print("Error occured. Unable to map meetings from RSS feed entries.", e)

    @classmethod
    def split_meeting_title(cls, title):
        """Accepts a string 'title' and splits on each hyphen. Returns a dictionary with keys for the 'type', 'date', and 'time' extracted from 'title': {type, date, time}."""

        try:
            columns = ["type", "date", "time"]
            data = title.split(" - ")
            meeting = dict(zip(columns, data))
            return meeting
        except Exception as e:
            print(
                "Error occurred. Unable to split meeting title from RSS feed entries.",
                e,
            )

    @classmethod
    def create_records(cls, entries):
        """Create new Meeting row objects."""

        try:
            meetings = []
            for entry in entries:
                meeting = cls(
                    type=entry["type"],
                    date=entry["date"],
                    time=entry["time"],
                    link=entry["link"],
                )
                meetings.append(meeting)
            return meetings
        except Exception as e:
            print("Error occured. Unable to create meetings records for database.", e)

    @classmethod
    def add_meetings_to_db(cls, records):
        """Add City Council meetings to database."""

        try:
            session = Session()
            session.query(cls).delete()
            reset_table("meetings")
            print("Adding council meetings to database...")
            session.add_all(records)
            session.commit()
        except Exception as e:
            print("Error occurred. Unable to add meetings to database.", e)
        finally:
            print(f"City Council meetings added to database: {len(records)}")
            session.close()

    @classmethod
    def get_meetings_links(cls):
        """Retrieve the links that point to the list of legislation for each meeting."""

        links = []
        try:
            session = Session()
            for link in session.query(cls.link):
                links.append(link[0])
            session.close()
            return links
        except Exception as e:
            print(
                "Error occurred. Unable to retrieve links from meetings in databse.", e
            )
