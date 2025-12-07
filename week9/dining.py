import threading
import time
import random

n = 4
chopsticks = [threading.Semaphore(1) for _ in range(n)]
room = threading.Semaphore(n - 1)

def philo(i, times):
    for r in range(times):
        print(f"philosopher {i} is thinking ")
        time.sleep(random.uniform(0.2, 0.5))  # shorter so output appears faster

        print(f"philosopher {i} is hungry ")
        room.acquire()
        left = i
        right = (i + 1) % n

        chopsticks[left].acquire()
        chopsticks[right].acquire()
        try:
            print(f"philosopher {i} is eating ")
            time.sleep(random.uniform(0.2, 0.5))
        finally:
            chopsticks[left].release()
            chopsticks[right].release()
            room.release()

        print(f"philo {i} finished eatin")

if __name__ == "__main__":
    print("Starting simulation...")
    threads = []
    for i in range(n):
        t = threading.Thread(target=philo, args=(i, 1))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("Simulation finished.")
