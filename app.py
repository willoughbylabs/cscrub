from models.helpers import db_connect
from models.members import Alderperson
from models.meetings import Meeting
from models.legislation import Legislation

# CONFIGURATIONS
create_tables_in_db = False
add_members_to_db = False
add_meetings_to_db = False
add_legislation_to_db = True
set_legislation_links_list = True
links_list = [
    "https://chicago.legistar.com/MeetingDetail.aspx?ID=448681&GUID=2F6FF8B5-B8C0-425C-A5A0-AF7120B4F3FC",
    "https://chicago.legistar.com/MeetingDetail.aspx?ID=505011&GUID=AC673713-8FC1-47CF-A160-D31BC131DF03",
    "https://chicago.legistar.com/MeetingDetail.aspx?ID=818175&GUID=D65139E8-BF1C-4F44-9CE4-3C40DA5EC1E9",
]

# APP
if create_tables_in_db:
    db_connect.create_tables()

if add_members_to_db:
    members = Alderperson.fetch_members()
    records = Alderperson.create_records(members)
    Alderperson.add_members_to_db(records)

if add_meetings_to_db:
    meetings = Meeting.fetch_meetings()
    records = Meeting.create_records(meetings)
    Meeting.add_meetings_to_db(records)

if add_legislation_to_db:
    if set_legislation_links_list:
        links = links_list
    entries = Legislation.fetch_legislation(links)
    records = Legislation.create_records(entries)
    Legislation.add_legislation_to_db(records)
