l = [1, 123, 34, 234, 3, 2]
if 4 in l:
    print(1)


def qq(arr):
    arr[4] = 3.13131
    qq2(arr)
    print(l)


def qq2(arrrr):
    arrrr[1] = 6234

qq(l)
def mn_index_block(i, l):
    return l[i:i + 2]
mn_index_block(2, l)[1] = 1
print(l, mn_index_block(2, l)[1])
