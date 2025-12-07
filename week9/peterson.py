#peterson or mutual exclusion
import threading
import time
turn=0
N=2
flag=[False]*N
def peterson(id, iterations):
    global turn
    other = 1 - id
    for _ in range(iterations):
        flag[id] = True
        turn = other
        while flag[other] and turn == other:
            time.sleep(0.001)  # busy wait
        print(f"Process {id} entered into critical section")
        time.sleep(0.01)  # simulate work inside critical section
        flag[id] = False
        print(f"Process {id} is in remainder section")
        time.sleep(0.005)  # simulate remainder work

if __name__=="__main__":
  iterations=1
  t1=threading.Thread(target=peterson,args=(0,iterations))
  t2=threading.Thread(target=peterson,args=(1,iterations))
  t1.start()
  t2.start()
  t1.join()
  t2.join()