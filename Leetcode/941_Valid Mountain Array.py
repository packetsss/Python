arr = [4, 5, 6, 1]

v = True

if len(arr) == 1 or arr[0] >= arr[1] or arr[len(arr) - 1] >= arr[len(arr) - 2]:
    v = False
else:
    for i in range(0, len(arr)):
        try:
            if arr[i + 1] <= arr[i]:
                for j in range(i, len(arr)):
                    if arr[j + 1] >= arr[j]:
                        v = False
                        break
            if not v:
                break
        except:
            pass
print(v)
