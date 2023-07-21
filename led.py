import RPi.GPIO as GPIO
import time

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

led_pwm(17)
