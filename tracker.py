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
    # Entry(time=now, name="CPU", value=psutil.cpu_percent(None)).save()
    cpu_per = psutil.cpu_percent(percpu=True,interval=None)
    for i, c in enumerate(cpu_per):
        Entry(time=now,name="CPU{}".format(i), value=c).save()
    Entry(time=now, name="RAM", value=psutil.virtual_memory()[2]).save()
    # Entry(time=now, name="Net_Errors", value=psutil.net_io_counters()).save()  # errors
    Entry(time=now, name="Net_Sent", value=psutil.net_io_counters()[2]).save()   # Packets sent
    Entry(time=now, name="Net_Recv", value=psutil.net_io_counters()[3]).save()  # Packets recv
    Entry(time=now, name="Net_Errin", value=psutil.net_io_counters()[4]).save()  # errors
    Entry(time=now, name="Net_Errout", value=psutil.net_io_counters()[5]).save()   # Packets sent
    Entry(time=now, name="Net_Dropin", value=psutil.net_io_counters()[6]).save()  # Packets recv
    Entry(time=now, name="Net_Dropout", value=psutil.net_io_counters()[7]).save()
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






