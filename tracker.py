#!/usr/bin/python3 
from peewee import *
import datetime
import os
import psutil
from models import *
from time import sleep
db = SqliteDatabase("temp_track.db")

def main():
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
#    print("temp is:",value)

    temp = Temperature(temperature=value)
    temp.save()
 #   for i in Temperature.select():
#        print("At {} the computer was {}".format(i.time,i.temperature))
    #Begin CPU usage
    cpu=Cpu(usage = psutil.cpu_percent(interval=None))
    cpu.save()
  #  for i in Cpu.select():
   #     print("At {} the computer was at {}".format(i.time,i.usage))
    #Begin RAM 
    Ram(percent = psutil.virtual_memory()[2], used = psutil.virtual_memory()[3]).save()
   # for i in Ram.select():
    #    print("At {} the computer used {}% of RAM,{}bytes s used".format(i.time,i.percent,i.used)) 

#db.create_tables([Ram,Temperature,Cpu,Self_usage])

while True:  
    main()
#    sleep(300)





