# daemon_threading.py
import threading
import time

def task():
    for i in range(5):
        print("Daemon task running", i)
        time.sleep(1)

print("--- Daemon Threading Example ---")
daemon_thread = threading.Thread(target=task)
daemon_thread.setDaemon(True)
daemon_thread.start()

print("Main thread finished, daemon will exit automatically")
time.sleep(2)  # Let daemon run briefly