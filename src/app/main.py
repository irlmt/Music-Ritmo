from src.app.app import app
from src.app.database import init_db
from src.app.service_layer import create_default_user
from src.app.db_loading import scan_and_load

init_db()
create_default_user()
scan_and_load()
