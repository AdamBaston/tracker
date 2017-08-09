#!/usr/bin/python3 
from peewee import *
import datetime
db = SqliteDatabase("temp_track.db")

class Entry(Model):
    name = CharField()
    time = DateTimeField()
    value = FloatField()

    class Meta:
        database = db




