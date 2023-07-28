import RPi.GPIO as GPIO
import time

DEFAULT_BUTTON_PIN = 22

button_pin = -1
pressed_count = 0

def pressed(channel):
  global pressed_count
  print("Button pressed!")
  pressed_count += 1

def init(pin):
  global button_pin
  button_pin = pin
  GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  pressed_count = 0
  GPIO.add_event_detect(button_pin, GPIO.RISING, callback=pressed)

def clear_count():
  global pressed_count
  pressed_count = 0

def cleanup():
  global pressed_count, button_pin
  pressed_count = 0
  button_pin = -1


if __name__ == "__main__":
  GPIO.setmode(GPIO.BCM)
  init(DEFAULT_BUTTON_PIN)
  while True:
    time.sleep(0.1)
