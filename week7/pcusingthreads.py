#producer consumer using multithreading or Queues
import threading
import time
import random
import queue #queues automaticallly handles safe state no need of semaphores

BUFFER_SIZE=5
q=queue.Queue(maxsize=BUFFER_SIZE)

def producer():
  while True:
    item=random.randint(0,10)
    q.put(item)
    print(f"[producer] producing : {item} and qsize is: {q.qsize()}")
    time.sleep(random.uniform(0.5,1.5))

def consumer():
  while True:
    item=q.get()
    print(f"[consumer] consumed: {item} and qsize is: {q.qsize()}")
    time.sleep(random.uniform(0.5,2.5)) #uniform -genrates
    q.task_done() #indicates task is done Predefined methods in Queue

if __name__ == "__main__":
  t1=threading.Thread(target=producer)
  t2=threading.Thread(target=consumer)

  t1.daemon=True
  t2.daemon=True

  t1.start()
  t2.start()

  time.sleep(10)

  print("Finished using multithreading")