from multiprocessing import Process, Value, Array
import time

# Function to increment a shared value
def increment(shared_val, n):
    for _ in range(n):
        shared_val.value += 1

# Function to modify a shared array
def modify_array(shared_arr, n):
    for i in range(len(shared_arr)):
        shared_arr[i] += n

if __name__ == "__main__":
    # Shared memory objects
    counter = Value('i', 0)  # 'i' means integer type
    arr = Array('i', [1, 2, 3, 4, 5])

    # Creating processes
    p1 = Process(target=increment, args=(counter, 1000))
    p2 = Process(target=increment, args=(counter, 1000))
    p3 = Process(target=modify_array, args=(arr, 10))

    # Starting processes
    p1.start()
    p2.start()
    p3.start()

    # Waiting for processes to finish
    p1.join()
    p2.join()
    p3.join()

    # Display shared memory results
    print(f"Shared counter = {counter.value}")
    print(f"Shared array = {list(arr)}")