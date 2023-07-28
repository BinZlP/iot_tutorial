import RPi.GPIO as GPIO
import time
import threading

DEFAULT_BUZZER_PIN = 27
buzzer_pin = -1

toggled = False


def init(pin):
  global buzzer_pin
  buzzer_pin = pin
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(buzzer_pin, GPIO.OUT)

def _on_for(sec):
  global toggled
  toggled = True
  GPIO.output(buzzer_pin, True)
  time.sleep(sec)
  GPIO.output(buzzer_pin, False)
  toggled = False

def on_for(sec):
  t= threading.Thread(target=_on_for, args=(sec,))
  t.start()
  return t

def on():
  global toggled
  toggled = True
  GPIO.output(buzzer_pin, True)

def off():
  global toggled
  toggled = False
  GPIO.output(buzzer_pin, False)

def cleanup():
  global buzzer_pin, toggled
  toggled = False
  buzzer_pin = -1


if __name__ == "__main__":
  GPIO.setmode(GPIO.BCM)

  init(DEFAULT_BUZZER_PIN)
  t = on_for(2)
  t.join()

  GPIO.cleanup()

