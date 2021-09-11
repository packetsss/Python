# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

"""
Given an array, find the longest subsequence oof the current array, it doesn't has to be adjacent to each other

consider all the possibilities(smaller than cur num) before the current position and add the max with 1

[3, 12, 4, 11]
[1] 1

[1, 2] --> 3 < 12, 1 + 1

[1, 2, 2] --> 3 < 4, 1 + 1

[1, 2, 2, 3] --> 4 < 11 so 2 + 1
"""

arr = [3, 12, 4, 11, 11]

def find(lst, idx=None):
    if idx is None:
        idx = len(lst) - 1
    if idx == 0:
        return 1
    maxx = 0
    for i in range(idx):
        if arr[i] < arr[idx]:
            maxx = max(maxx, find(lst, i) + 1)
    return maxx


print(find(arr))
