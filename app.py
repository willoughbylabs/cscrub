from models.helpers import db_connect
from models.members import Alderperson

# CONFIGURATIONS
create_tables_in_db = False
fetch_members = True

# APP
if create_tables_in_db:
    db_connect.create_tables()

if fetch_members:
    members = Alderperson.fetch_members()
    print(members)
