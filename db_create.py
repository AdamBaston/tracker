# from config import
from app import db
from app.models import Entry
db.create_tables([Entry])

