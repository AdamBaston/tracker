from datetime import datetime
import pygal
from flask import Flask, render_template
from playhouse.shortcuts import model_to_dict
from tracker.config import DEBUG
from tracker.tracker import Entry

app = Flask(__name__)


@app.route("/")
def index():
    style = "height = 100"
    data = []
    chart = []
    time = []
    for i, c in enumerate(Entry.select().where(Entry.name == "CPU")):
        data.append(c.value)
        time.append(datetime.strftime(c.time, "%Y-%m-%d %H:%M:%S.%f"))
    hist = pygal.Line(x_label_orientation=60, height=200)
    hist.add('Wide bars', data)  # value, start point ,end point
    hist.x_labels = time

    hist = hist.render_data_uri()
    chart.append(hist)
    # this is totally DRY !
    data = []
    time = []
    for i, c in enumerate(Entry.select().where(Entry.name == "RAM")):
            data.append(c.value)
            time.append(datetime.strftime(c.time, "%Y-%m-%d %H:%M:%S.%f"))
    hist = pygal.Line(x_label_orientation=60, height=200)
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
    hist.add('Ram usage', data)  # value, start point ,end point
    hist.x_labels = time
    hist = hist.render_data_uri()
    chart.append(hist)

    return render_template('graphs.html', charts=chart)
    # return hist.render_response()


@app.route("/api/v1/cpu")
def cpu_api():
    data = []
    for i in Entry.select().where(Entry.name == "CPU"):
        data.append(model_to_dict(i))

    # print(data)
    return str(data).strip("[]")


if __name__ == "__main__":
    app.run(debug=DEBUG)
    print("Started")
