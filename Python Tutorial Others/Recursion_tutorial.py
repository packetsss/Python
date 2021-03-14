def grid_paths(n, m):
    if n == 1 or m == 1:
        return 1
    else:
        return grid_paths(n, m - 1) + grid_paths(n - 1, m)


print(grid_paths(9, 10))


def count_partitions(n, m):
    if n == 0:
        return 1
    elif m == 0 or n < 0:
        return 0
    else:
        return count_partitions(n - m, m) + count_partitions(n, m - 1)


print(count_partitions(9, 60))

'''
steps:
1. What's the simplest possible input?
    - try 0, 1, 2 combination
2. Play around with examples and visualize
3. Relate hard cases to simpler cases
4. Generalize the pattern
5. Write code by combining recursive pattern with the base case
'''
