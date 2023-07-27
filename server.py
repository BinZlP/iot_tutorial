from flask import Flask, render_template, redirect, url_for
import module.timer as timer
import atexit
import RPi.GPIO as GPIO
import module.led as led

APP_PORT = 8080

app = Flask(__name__)

CONFIGS={
    "MY_APP_NAME": "Home Monitor",
    "DASHBOARD_PAGE_STRING": "STATUS",
    "SENSORS_PAGE_STRING": "SENSOR VALUES"
}

SENSOR_VALUES={
    "A": "10",
    "B": "20",
    "C": "30",
}

@app.route('/')
def index():
    return render_template('index.html', app_name=CONFIGS["MY_APP_NAME"], menu_string=CONFIGS["DASHBOARD_PAGE_STRING"])

@app.route('/sensor_values')
def sensor_values():
    SENSOR_VALUES["timer_value"] = timer.get()
    SENSOR_VALUES["led_status"] = led.status
    return render_template('index.html', app_name=CONFIGS["MY_APP_NAME"], menu_string=CONFIGS["SENSORS_PAGE_STRING"], test="Hello!", **SENSOR_VALUES)

# Normal routing
@app.route('/runtime')
def show_runtime():
    return "Server runtime: "+str(timer.get())+"s"

# Reset server runtime
@app.route('/reset')
def reset_runtime():
    timer.reset()
    return redirect(url_for('show_runtime'))

# LED On/Off
@app.route('/led_switch')
def led_switch():
    if led.status == led.LED_ON_VALUE:
        led.off()
        return redirect(url_for('sensor_values'))
    elif led.status == led.LED_OFF_VALUE:
        led.on()
        return redirect(url_for('sensor_values'))
    else:
        return "<script> alert('LED를 먼저 초기화해주세요.'); location.href=\"/\"; </script>"


# Get a parameter from URL
@app.route('/board/<article_idx>')
def board_view(article_idx):
    return article_idx

# Function 'board_view' does the role of the end-point
@app.route('/boards',defaults={'page':'index'})
@app.route('/boards/<page>')
def boards(page):
    return "Page: "+page


def cleanup_gpio():
    GPIO.cleanup()


# Register shutdown event handler
atexit.register(cleanup_gpio)

# Server start
timer.start()
GPIO.setmode(GPIO.BCM)
led.init(17)
app.run(host="192.168.35.201", port=APP_PORT, debug=True)
