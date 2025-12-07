# single_threading.py
import time

def task():
    for i in range(5):
        print("Task running:", i)
        time.sleep(1)

print("--- Single Threading Example ---")
task()
print("Single thread finished")