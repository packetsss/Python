import numpy as np

d = {}
with open("User_data.txt", "r") as f:
    for l in f:
        l = str(l).replace(".", "0")
        arr = [[int(i) for i in l[j:(j + 9)]] for j in range(0, 81, 9)]
        with open("puzzle1.txt", "a") as ff:
            d = {"puzzle": arr,
                 "solution": []}
            print(d, file=ff)
