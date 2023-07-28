import RPi.GPIO as GPIO
import time
import threading

DEFAULT_PASSIVE_BUZZER_PIN = 26
passive_buzzer_pin = -1

HZ_C = 261
HZ_D = 294
HZ_E = 329
HZ_F = 349
HZ_G = 392
HZ_A = 440
HZ_B = 493
HZ_HIGH_C = 523

scale = [ HZ_C, HZ_D, HZ_E, HZ_F, HZ_G, HZ_A, HZ_B, HZ_HIGH_C ]

HZ_C_NUM = 0
HZ_D_NUM = 1
HZ_E_NUM = 2
HZ_F_NUM = 3
HZ_G_NUM = 4
HZ_A_NUM = 5
HZ_B_NUM = 6
HZ_HIGH_C_NUM = 7

p = None
toggled = False

def init(pin):
  global passive_buzzer_pin, p, toggled
  passive_buzzer_pin = pin
  GPIO.setup(passive_buzzer_pin, GPIO.OUT)
  p = GPIO.PWM(passive_buzzer_pin, 100)
  p.start(0)
  toggled = False

def on_with_key(k):
  global toggled
  toggled = True
  p.ChangeDutyCycle(85)
  p.ChangeFrequency(k)

def _siren(low, high):
  global toggled
  toggled = True

  for i in range(low, high+1):
    if not toggled:
      break
    p.ChangeFrequency(i)
    time.sleep(0.01)
  for i in range(high, low-1, -1):
    if not toggled:
      break
    p.ChangeFrequency(i)
    time.sleep(0.01)

  toggled = False

def siren(low, high):
  t = threading.Thread(target=_siren, args=(low, high))
  t.start()

def _play_song():
  list = [4, 4, 5, 5, 4, 4, 2, 2, 4, 4, 2, 2, 1, 1]
  for i in list:
    on_with_key(scale[i])
    time.sleep(0.5)
  off()


def play_song():
  t = threading.Thread(target=_play_song)
  t.start()
  return t

def is_toggled():
  return toggled

def off():
  global toggled
  p.ChangeDutyCycle(0)
  toggled = False


if __name__ == "__main__":
  GPIO.setmode(GPIO.BCM)
  init(DEFAULT_PASSIVE_BUZZER_PIN)

  t = play_song()
  t.join()

  print("Thank you for listening!")
  time.sleep(1)

  GPIO.cleanup()
