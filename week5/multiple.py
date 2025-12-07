# multiple_threading.py
import threading
import time

def task(name):
    for i in range(3):
        print(f"{name} running iteration {i}")
        time.sleep(1)

t1 = threading.Thread(target=task, args=("Thread-1",))
t2 = threading.Thread(target=task, args=("Thread-2",))

print("--- Multiple Threading Example ---")
t1.start()
t2.start()

t1.join()
t2.join()
print("Multiple threads finished")