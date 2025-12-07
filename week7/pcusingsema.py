

from multiprocessing import Process, Value, Semaphore
import time
import random

counter = Value('i', 0)
mutex = Semaphore(1)
items = Semaphore(0)
spaces = Semaphore(5)

def producer(pid):
    for _ in range(5):
        spaces.acquire()
        mutex.acquire()
        counter.value += 1
        print(f"Producer {pid} produced : {counter.value}")
        time.sleep(random.uniform(1,2))
        mutex.release()
        items.release()

def consumer(cid):
    for _ in range(5):
        items.acquire()
        mutex.acquire()
        counter.value -= 1
        print(f"Consumer {cid} consumed: {counter.value}")
        time.sleep(random.uniform(1,2))
        mutex.release()
        spaces.release()

if __name__ == "_main_":
    pro = [Process(target=producer,args=(i,)) for i in range(2)]
    con = [Process(target=consumer,args=(i,)) for i in range(2)]

    for p in pro: p.start()
    for c in con: c.start()
    for p in pro: p.join()
    for c in con: c.join()