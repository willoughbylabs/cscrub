from models.helpers import db_connect
from models.members import Alderperson

# CONFIGURATIONS
create_tables_in_db = True

if create_tables_in_db:
    db_connect.create_tables()
