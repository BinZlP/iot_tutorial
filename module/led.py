import RPi.GPIO as GPIO
import time

DEFAULT_LED_PIN = 17

LED_ON_VALUE = "ON"
LED_OFF_VALUE = "OFF"
LED_NOT_INITIALIZED = "NOT_INIT"

pwm = None
status = LED_NOT_INITIALIZED

led_pin = -1

def led_pwm(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    pwm = GPIO.PWM(pin, 100) # pwm 설정 (100Hz)
    pwm.start(0)

    for i in range(101):
        pwm.ChangeDutyCycle(i)
        time.sleep(0.1)

    pwm.stop()
    GPIO.cleanup()


def init(pin):
    global pwm, status, led_pin
    led_pin = pin
    GPIO.setup(led_pin, GPIO.OUT)
    pwm = GPIO.PWM(led_pin, 100)
    status = LED_OFF_VALUE

def cleanup():
    global pwm, status
    status = LED_NOT_INITIALIZED
    pwm.stop()

def on():
    global pwm, status
    pwm.start(50)
    status = LED_ON_VALUE

def off():
    global pwm, status
    status = LED_OFF_VALUE
    pwm.stop()


def on_for(sec):
    global pwm, status
    pwm.start(50)
    time.sleep(sec)
    pwm.stop()
    status = LED_OFF_VALUE


if __name__ == "__main__":
    led_pwm(DEFAULT_LED_PIN)
