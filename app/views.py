from datetime import datetime
from difflib import SequenceMatcher as SM
import pygal
from flask import render_template
from playhouse.shortcuts import model_to_dict
from app import app, db
from config import DEBUG,FORMATTING_TIME
from .models import Entry


@app.route("/", type=["GET"])
def index():
    # style = "height = 100"
    data = dict()
    chart = []
    time = dict()
    for c in Entry.select().where(Entry.name.contains("CPU")):
        if c.name in data:
            data[c.name].append(c.value)
        else:
            data[c.name] = [c.value]
        if c.name in time:
            time[c.name].append(c.time)
        else:
            time[c.name] = [c.time]
    hist = pygal.Line(x_label_orientation=60, height=200)
    for i in data.keys():
        hist.add(i, data[i])  # value, start point ,end point

    tea_time = next(iter(time.values()))
    local_time = []
    for i, x in enumerate(tea_time):
        date = datetime.strftime(tea_time[i], FORMATTING_TIME)
        local_time.append(date.split(" ")[1].split(".")[0])
    hist.x_labels = local_time
    hist = hist.render_data_uri()
    chart.append(hist)
    # this is totally DRY !
    data = []
    time = []
    for i, c in enumerate(Entry.select().where(Entry.name == "RAM")):
            data.append(c.value)
            time.append(datetime.strftime(c.time, "%Y-%m-%d %H:%M:%S.%f"))
    hist = pygal.Line(x_label_orientation=90, height=200)
    hist.add('Ram usage', data)  # value, start point ,end point
    hist.x_labels = time
    hist = hist.render_data_uri()
    chart.append(hist)
    # this is totally DRY !
    data = []
    time = []
    for i in Entry.select().where(Entry.name == "TEMPERATURE"):
            data.append(i.value)
            time.append(datetime.strftime(i.time, "%Y-%m-%d %H:%M:%S.%f"))

    hist = pygal.Line(x_label_orientation=60, height=200)

    hist.add('Temperature', data)  # value, start point ,end point
    hist.x_labels = time
    hist = hist.render_data_uri()
    chart.append(hist)
    hist = pygal.Line(x_label_orientation=60, height=200)
    data = dict()
    time = dict()
    for c in Entry.select().where(Entry.name.contains("Net")):
        if c.name in data:
            data[c.name].append(c.value)
        else:
            data[c.name] = [c.value]

        if c.name in time:
            time[c.name].append(c.time)
        else:
            time[c.name] = [c.time]
    t = []
    for i, x in zip(data["Net_Sent"][1:], data["Net_Sent"]):
        if int(i) - int(x) < 0:
            pass
        else:
            t.append(i - x)
    data["Net_Sent"] = t
    t = []
    for i, x in zip(data["Net_Recv"][1:], data["Net_Recv"]):
        if int(i) - int(x) < 0:
            pass
        else:
            t.append(i - x)

    if SM(None,str(t[0]),str(t[1])).quick_ratio() > .4:
        t[0] = 0

    data["Net_Recv"] = t

    for i in data.keys():
        hist.add(i, data[i])  # value, start point ,end point
    hist = hist.render_data_uri()
    chart.append(hist)
    return render_template('graphs.html', charts=chart)
    # return hist.render_response()


@app.route("/api/v1/<datum>")
def any_api(datum):
    data = []
    if datum is None or " ":
        for i in Entry.select().order_by(Entry.name):
            data.append(model_to_dict(i))
    else:
        for i in Entry.select().where(Entry.name == datum.upper()):
            data.append(model_to_dict(i))

    return str(data).strip("[]")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=DEBUG)
    print("Started")
