from flask import Flask, render_template, redirect, url_for
import server_runtime

app = Flask(__name__)

# MY_APP_NAME="Home Monitor"
# DASHBOARD_PAGE_STRING="STATUS"
# SENSORS_PAGE_STRING="SENSOR VALUES"

CONFIGS={
    "MY_APP_NAME": "Home Monitor",
    "DASHBOARD_PAGE_STRING": "STATUS",
    "SENSORS_PAGE_STRING": "SENSOR VALUES"
}

SENSOR_VALUES={
    "A": "10",
    "B": "20",
    "C": "30"
}

@app.route('/')
def index():
    return render_template('index.html', app_name=CONFIGS["MY_APP_NAME"], menu_string=CONFIGS["DASHBOARD_PAGE_STRING"])

@app.route('/sensor_values')
def sensor_values():
    return render_template('index.html', app_name=CONFIGS["MY_APP_NAME"], menu_string=CONFIGS["SENSORS_PAGE_STRING"], test="Hello!", **SENSOR_VALUES)

@app.route('/reset')
def reset():
    server_runtime.reset_runtime()
    return redirect(url_for('/runtime'))

# Normal routing
@app.route('/runtime')
def board():
    return "Server runtime: "+str(server_runtime.runtime)+"s"

# Get a parameter from URL
@app.route('/board/<article_idx>')
def board_view(article_idx):
    return article_idx

# Function 'board_view' does the role of the end-point
@app.route('/boards',defaults={'page':'index'})
@app.route('/boards/<page>')
def boards(page):
    return "Page: "+page


app.run(host="localhost",port=8080)
