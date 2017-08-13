from flask import Flask
from peewee import SqliteDatabase
app = Flask(__name__)
app.config.from_object("config")
db = SqliteDatabase("temp_track.db")

from app import views, models