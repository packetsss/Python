
import time

for i in reversed(range(100)):
    print(i, end="\r", flush=True)
    time.sleep(0.01)

