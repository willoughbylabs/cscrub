from models.helpers import db_connect
from models.members import Alderperson
from models.meetings import Meeting
from models.legislation import Legislation
from models.votes import Vote

# CONFIGURATIONS
create_tables_in_db = False

add_members_to_db = False

add_meetings_to_db = False

add_legislation_to_db = False

set_legislation_links_list = False

add_votes_to_db = True

set_votes_links_list = True

links_list = [
    "https://chicago.legistar.com/MeetingDetail.aspx?ID=505011&GUID=AC673713-8FC1-47CF-A160-D31BC131DF03"
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
    else:
        links = Meeting.get_meetings_links()
    entries = Legislation.fetch_legislation(links)
    records = Legislation.create_records(entries)
    Legislation.add_legislation_to_db(records)

if add_votes_to_db:
    if set_votes_links_list:
        links = links_list
    action_links = Legislation.fetch_action_details_links(links)
    print(action_links)
