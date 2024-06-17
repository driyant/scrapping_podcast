import itertools
import threading
import sys
import time

class Spinner:
  def __init__(self, message="Loading..."):
    self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    self.stop_running = threading.Event()
    self.message = message
    self.spinner_thread = threading.Thread(target=self._spin)

  def _spin(self):
    while not self.stop_running.is_set():
      sys.stdout.write(f"\r{next(self.spinner)} {self.message} ")
      sys.stdout.flush()
      time.sleep(0.1)
        
  def start(self):
    self.stop_running.clear()
    self.spinner_thread.start()

  def stop(self):
    self.stop_running.set()
    self.spinner_thread.join()
    sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
    sys.stdout.flush()