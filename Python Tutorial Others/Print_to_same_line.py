import sys
import time

for i in range(100):
    print(i, end="\r")
    time.sleep(0.01)
    sys.stdout.flush()
