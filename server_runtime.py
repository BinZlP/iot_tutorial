import threading
import time

runtime=0

def update_runtime_forever():
  global runtime;
  while True:
    time.sleep(1)
    runtime += 1

t = threading.Thread(target=update_runtime_forever)
t.daemon = True
t.start()

