l = [1, 123, 34, 234, 3 ,2]
if 4 in l:
    print(1)

def qq(arr):
    arr[4] = 3.13131
    qq2(arr)

def qq2(arr):
    arr[1] = 6234
qq(l)
print(l)
