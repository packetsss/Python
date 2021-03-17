from timeit import default_timer as timer
import numpy as np

"""
How many possible ways a traveller can travel through a N x M grid?

1x1: [0]
1 way

1x2: [0, 0]
1 way

2x2: [0, 0]
     [0, 0]
2 ways


2x3: [0, 0, 0] == 2 + 1
     [0, 0, 0]
3 ways

3x3: [0, 0, 0]    [0, 0, 0]   [0, 0]
     [0, 0, 0] == [0, 0, 0] + [0, 0] == 2 + 1 + 2 + 1
     [0, 0, 0]                [0, 0]

6 ways

3x4: [0, 0, 0, 0]    [0, 0, 0]   [0, 0, 0, 0]
     [0, 0, 0, 0] == [0, 0, 0] + [0, 0, 0, 0] == 6 + 3 + 1
     [0, 0, 0, 0]    [0, 0, 0]

 

"""


def grid_traveller(n, m):
    if n == 0 or m == 0:
        return 0
    elif n < 2 and m < 2:
        return min(n, m)
    else:
        return grid_traveller(n - 1, m) + grid_traveller(n, m - 1)


start = timer()
print(grid_traveller(13, 10))
end = timer()
print(end - start)
# Slow naive recursive solution


### Memoized
d = {}
def grid_traveller_topdown(n, m):
    key = f"{n}{m}"
    if n == 0 or m == 0:
        return 0
    elif n < 2 and m < 2:
        return min(n, m)
    elif key in d:
        return d[key]
    else:
        d[key] = grid_traveller_topdown(n - 1, m) + grid_traveller_topdown(n, m - 1)
        return d[key]


start = timer()
print(grid_traveller_topdown(13, 100))
end = timer()
print(end - start)


### Tabulation
def grid_traveller_bottom_up(n, m):
    if n == 0 or m == 0:
        return 0

    lst = np.zeros((n + 1, m + 1))
    lst[1:, 1] = 1
    lst[1, 1:] = 1

    for i in range(2, n + 1):
        for j in range(2, m + 1):
            lst[i, j] = lst[i - 1, j] + lst[i, j - 1]
    return int(lst[-1, -1])


start = timer()
print(grid_traveller_bottom_up(13, 100))
end = timer()
print(end - start)
# 2x faster

# best to use 0 for counting problems
def grid_traveller_bottom_up_1(n, m):
    table = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    # correct way to create a 2d array

    table[1][1] = 1

    # add the current value of i to it's right and bottom
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cur = table[i][j]
            if i < m:
                table[i + 1][j] += cur
            if j < n:
                table[i][j + 1] += cur

    return table[m][n]


start = timer()
print(grid_traveller_bottom_up_1(13, 100))
end = timer()
print(end - start)
