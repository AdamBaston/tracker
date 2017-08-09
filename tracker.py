#!/usr/bin/python3 
from datetime import timedelta, datetime
from time import sleep

import psutil
from peewee import *

import config


class Entry(Model):
    name = CharField()
    time = DateTimeField()
    value = FloatField()

    class Meta:
        database = config.DB


# @async
def main():
    now = datetime.utcnow()
    try: # for windows DEV purposes because Im lazy
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            value=str(f.read())
        value = list(value)
        for i in value:
            if i == ".":
                value.remove(i)
        value.insert(2, ".")
        t_value = ""
        for i in value:
            t_value+=i
        value = float(t_value)
        Entry(time=now, name="TEMPERATURE", value=value).save()
    except FileNotFoundError:
        pass
    Entry(time=now, name="CPU", value=psutil.cpu_percent(None)).save()
    Entry(time=now, name="RAM", value=psutil.virtual_memory()[2]).save()


# @async
def clean_db():
    now = datetime.utcnow()
    for i in Entry.select():
        if now-timedelta(hours=config.BACK_LOG) > datetime.strptime(str(i.time), "%Y-%m-%d %H:%M:%S.%f"):
            i.delete_instance()


def run(sleep_time):
    psutil.cpu_percent(interval=None)
    while True:
        main()
        clean_db()
        print("Complete dud")
        sleep(sleep_time)


if __name__ == "__main__":
    run(config.QUERY_TIME)






