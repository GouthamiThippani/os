# threadpool_executor.py
from concurrent.futures import ThreadPoolExecutor
import time

def task(n):
    print(f"Task {n} starting")
    time.sleep(2)
    print(f"Task {n} finished")
    return n*n

print("--- ThreadPoolExecutor Example ---")
with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(task, [1, 2, 3, 4, 5])

print("Results:", list(results))