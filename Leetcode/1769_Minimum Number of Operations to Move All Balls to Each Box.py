import numpy as np
boxes = "001011"

lists = list(boxes)
out = [0] * len(lists)
ct = 0

for idx in range(len(lists)):
    ct = 0
    for i in reversed(range(idx)):
        if lists[i] == '0':
            continue
        ct += idx - i

    for i in range(idx, len(lists)):
        if lists[i] == '0':
            continue
        ct += i - idx
    out[idx] = ct


print(lists)
print(out)

# --------------------------------------
length = len(boxes)
arr = np.array(list(boxes))
out1 = [0] * length
for i in range(length):
    out1[i] = sum(np.where(arr[i:length] == "1")[0]) + sum(i - np.where(arr[:i] == "1")[0])
print(out1)

