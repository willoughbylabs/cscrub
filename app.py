from models.helpers import db_connect
from models.members import Alderperson
from models.meetings import Meeting

# CONFIGURATIONS
create_tables_in_db = False
add_members_to_db = False
add_meetings_to_db = True

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
