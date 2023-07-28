from flask import Flask, render_template, redirect, url_for
import module.timer as timer
import atexit
import RPi.GPIO as GPIO
import module.led as led
import module.button as button
import module.buzzer as buzzer
import module.passive_buzzer as passive_buzzer
import module.flame_sensor as flame
import module.ultrasonic as ultrasonic

APP_PORT = 8080

LED_PIN = led.DEFAULT_LED_PIN
BUTTON_PIN = button.DEFAULT_BUTTON_PIN
BUZZER_PIN = buzzer.DEFAULT_BUZZER_PIN
PASSIVE_BUZZER_PIN = passive_buzzer.DEFAULT_PASSIVE_BUZZER_PIN
FLAME_PIN = flame.DEFAULT_FLAME_PIN
ULTRASONIC_TRIG_PIN = ultrasonic.DEFAULT_TRIG_PIN
ULTRASONIC_ECHO_PIN = ultrasonic.DEFAULT_ECHO_PIN

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


######## Please complete this function #########
def is_our_home_safe():
    return True


@app.route('/')
def index():
    render_option = {
        "app_name": CONFIGS["MY_APP_NAME"],
        "menu_string": CONFIGS["DASHBOARD_PAGE_STRING"],
        "is_home_safe": is_our_home_safe(),
        "button_push_count": button.pressed_count
    }
    return render_template('index.html', **render_option)

@app.route('/sensor_values')
def sensor_values():
    render_option = {
        "app_name": CONFIGS["MY_APP_NAME"],
        "menu_string": CONFIGS["SENSORS_PAGE_STRING"],
        "test": "Hello!"
    }
    print(render_option)
    SENSOR_VALUES["timer_value"] = timer.get()
    SENSOR_VALUES["led_status"] = led.status
    return render_template('index.html', **render_option, **SENSOR_VALUES)

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

# Buzzer song
@app.route('/sing')
def sing_with_buzzer():
    passive_buzzer.play_song()
    return redirect(url_for('sensor_values'))

# Get a parameter from URL
@app.route('/board/<article_idx>')
def board_view(article_idx):
    return article_idx

# Function 'board_view' does the role of the end-point
@app.route('/boards',defaults={'page':'index'})
@app.route('/boards/<page>')
def boards(page):
    return "Page: "+page


# Register shutdown event handler
def cleanup_gpio():
    GPIO.cleanup()

atexit.register(cleanup_gpio)

# Initialize sensors
timer.start()
GPIO.setmode(GPIO.BCM)
led.init(LED_PIN)
button.init(BUTTON_PIN)
buzzer.init(BUZZER_PIN)
passive_buzzer.init(PASSIVE_BUZZER_PIN)
flame.init(FLAME_PIN)
ultrasonic.init(trig=ULTRASONIC_TRIG_PIN, echo=ULTRASONIC_ECHO_PIN)

# Server start
app.run(host="192.168.35.201", port=APP_PORT, debug=True)
