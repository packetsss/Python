from Sudoku_interface import interface
import numpy as np
from timeit import default_timer as timer
from collections import Counter
l = [1, 123, 34, 234, 2]
if 4 in l:
    print(1)


def qq(arr):
    arr[4] = 3.13131
    qq2(arr)
    # print(l)


def qq2(arrrr):
    arrrr[1] = 6234





def mn_index_block(i, l):
    return l[i:i + 2]


mn_index_block(2, l)[1] = 1
# print(l, mn_index_block(2, l)[1])
a = ""
for i in range(9):
    a.join(str(i))

# print("".join(map(str, l)))
#l = set(l)
l1 = {1, 34, 3, 2, 234, 6234}

#print(l1.difference(l))
s0 = list(range(1, 10))
s1 = [2479, 237, 5, 267, 234679, 8, 2346, 236, 1]
s2 = [6, 4, 2378, 1278, 127, 12, 9, 137, 3578]
s3 = [2479, 279, 1, 3, 8, 246, 26, 5, 679]

a = "".join("1231241")

print(Counter(a))
aa = "".join(map(str, l))
if "4" in aa:
    print(1)
print(aa)
i, j = 4, 0
print(i // 3 * 3 + j//3, i // 3 * 3 + j % 3)
