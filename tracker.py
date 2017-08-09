#!/usr/bin/python3 
from datetime import timedelta, datetime
try:
    import psutil
except ModuleNotFoundError:
    pass
from models import *
from time import sleep
import config
from Decorators import async
db = SqliteDatabase("temp_track.db")


# @async
def main():
    now = datetime.datetime.utcnow()
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
    print("Main finished")


# @async
def clean_db():
    now = datetime.datetime.utcnow()
    for i in Entry.select():
        if now-timedelta(hours=config.BACK_LOG) < datetime.datetime.strptime(str(i.time), "%Y-%m-%d %H:%M:%S.%f"):
            i.delete_instance()


def run():
    psutil.cpu_percent(interval=None)
    while True:
        main()
        clean_db()
        sleep(config.QUERY_TIME)


if __name__ == "__main__":
    run()







