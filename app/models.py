from app import db, app
from peewee import *


class Entry(Model):
    name = CharField()
    time = DateTimeField()
    value = FloatField()

    class Meta:
        database = db