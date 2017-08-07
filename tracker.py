#!/usr/bin/python3 
from peewee import *
#import datetime
from datetime import timedelta, datetime
import os
import psutil
from models import *
from time import sleep
import logging
db = SqliteDatabase("temp_track.db")

def main():
    now = datetime.datetime.utcnow()
    with open("/sys/class/thermal/thermal_zone0/temp") as f:  
        value=str(f.read())
    value = list(value)
    for i in value:
        if i == ".":
            v.remove(i)
    value.insert(2,".")
    t_value = ""
    for i in value:
        t_value+=i
    value = float(t_value)
    Temperature(temperature=value,time=now).save()
    #Begin CPU usage
    Cpu(usage = psutil.cpu_percent(interval=None),time=now).save()
    #Begin RAM 
    Ram(percent = psutil.virtual_memory()[2], used = psutil.virtual_memory()[3],time=now).save()

#db.create_tables([Ram,Temperature,Cpu,Self_usage])
def clean_db():
    now =datetime.datetime.utcnow()
    for i in Ram.select():
        dt_o = datetime.datetime.strptime(str(i.time), "%Y-%m-%d %H:%M:%S.%f") # convert back to a datetime object
        if now-timedelta(days=3) > dt_o:
            i.delete_instance()

    for i in Cpu.select():
        dt_o = datetime.datetime.strptime(str(i.time), "%Y-%m-%d %H:%M:%S.%f") # convert back to a datetime object
        if now-timedelta(days=3) > dt_o:
            i.delete_instance()
    for i in Temperature.select():
        dt_o = datetime.datetime.strptime(str(i.time), "%Y-%m-%d %H:%M:%S.%f") # convert back to a datetime object
        if now- timedelta(days=3) > dt_o:
            i.delete_instance()
#if __name__ == "__main__":

#logging.basicConfig(filename="tracker.log",level=logging.DEBUG)


while True:  
  #  main() 
   clean_db()
  #  sleep(300)






