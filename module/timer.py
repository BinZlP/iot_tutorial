import threading
import time

runtime = 0
stop_flag = False
t = None

def get():
  return runtime

def update_runtime_forever():
  global runtime
  while stop_flag is False:
    time.sleep(1)
    runtime += 1

def reset():
  global runtime
  runtime=0

def start():
  global runtime, t, stop_flag
  runtime = 0
  stop_flag = False
  t = threading.Thread(target=update_runtime_forever)
  t.daemon = True
  t.start()

def stop():
  global runtime, stop_flag
  runtime = 0
  stop_flag = True
  t.join()




