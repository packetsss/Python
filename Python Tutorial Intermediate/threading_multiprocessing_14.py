# process is a instance of a program
# thread is an entity within a process


from multiprocessing import Process
import os
import time


def square_numbers():
    for i in range(100):
        i * i
        time.sleep(0.1)


if __name__ == "__main__":
    processes = []
    num_processes = os.cpu_count()

for i in range(num_processes):
    p = Process(target=square_numbers)
    processes.append(p)

for p in processes:
    p.start()

for p in processes:
    p.join()

print("end main")
# not working
