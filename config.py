# from pygal import Style
from peewee import SqliteDatabase
BACK_LOG = 10 # How many hours to keep data for
DEBUG = True
QUERY_TIME = 3 #how many seconds between each query
FORMATTING_TIME = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = True
DB = SqliteDatabase("temp_track.db")
