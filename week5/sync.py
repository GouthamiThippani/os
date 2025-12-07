# lock_threading.py
import threading
import time

lock = threading.Lock()
shared_counter = 0

def increment(name):
    global shared_counter
    for _ in range(5):
        lock.acquire()
        shared_counter += 1
        print(f"{name} incremented counter to {shared_counter}")
        lock.release()
        time.sleep(0.5)

t1 = threading.Thread(target=increment, args=("Thread-1",))
t2 = threading.Thread(target=increment, args=("Thread-2",))

print("--- Synchronization with Lock Example ---")
t1.start()
t2.start()

t1.join()
t2.join()
print("Final counter:", shared_counter)