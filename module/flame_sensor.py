import RPi.GPIO as GPIO
import time

DEFAULT_FLAME_PIN = 19
flame_pin = -1

def init(pin):
  global flame_pin
  flame_pin = pin
  GPIO.setup(flame_pin, GPIO.IN)

def detect():
  return GPIO.input(flame_pin) == GPIO.HIGH

def cleanup():
  global flame_pin
  flame_pin = 0


if __name__ == "__main__":
  GPIO.setmode(GPIO.BCM)
  init(DEFAULT_FLAME_PIN)

  while True:
    if GPIO.input(flame_pin) == GPIO.HIGH:
      print("Safe")
    else:
      print("Fire!")
    time.sleep(0.5)

