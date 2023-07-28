import RPi.GPIO as GPIO
import time

DEFAULT_TRIG_PIN = 6
DEFAULT_ECHO_PIN = 5

trig_pin = -1
echo_pin = -1

def init(trig, echo):
  global trig_pin, echo_pin
  trig_pin = trig
  echo_pin = echo
  GPIO.setup(trig_pin, GPIO.OUT)
  GPIO.setup(echo_pin, GPIO.IN)


def get_distance():
  GPIO.output(trig_pin, False)
  time.sleep(0.5)

  # Shoot ultrasonic wave
  GPIO.output(trig_pin, True)
  time.sleep(0.00001)
  GPIO.output(trig_pin, False)

  # Set start time
  while GPIO.input(echo_pin) == 0:
    start = time.time()

  # Wait until ultrasonic wave returns
  while GPIO.input(echo_pin) == 1:
    stop = time.time()

  # Calculate distance
  time_interval = stop - start
  distance = time_interval * 17000
  distance = round(distance, 2)

  return distance


def cleanup():
  global trig_pin, echo_pin
  trig_pin = -1
  echo_pin = -1





if __name__ == "__main__":
  GPIO.setmode(GPIO.BCM)
  init(DEFAULT_TRIG_PIN, DEFAULT_ECHO_PIN)

  print("Press SW or input Ctrl+C to quit")

  try:
    while True:
      print("Distance => ", get_distance(), "cm")

  except KeyboardInterrupt:
    GPIO.cleanup()
    print("bye~")
