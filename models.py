#!/usr/bin/python3 
from peewee import *
import datetime
db = SqliteDatabase("temp_track.db")

class BaseModel(Model):
    time=DateTimeField(default=datetime.datetime.utcnow)
    class Meta:
        database = db

class Temperature(BaseModel):
    temperature = FloatField()

class Self_usage(BaseModel):
    usage = FloatField()

class Cpu(BaseModel):
    usage = FloatField()

class Ram(BaseModel):
    percent = FloatField()
    used  = IntegerField()




