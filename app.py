from models.helpers import db_connect
from models.members import Alderperson

# CONFIGURATIONS
create_tables_in_db = True
add_members_to_db = True

# APP
if create_tables_in_db:
    db_connect.create_tables()

if add_members_to_db:
    members = Alderperson.fetch_members()
    records = Alderperson.create_records(members)
    Alderperson.add_members_to_db(records)
