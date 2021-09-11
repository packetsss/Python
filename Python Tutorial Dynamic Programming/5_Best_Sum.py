# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

"""
canSum --> Decision Problem
howSum --> Combinatorics Problem
bestSum --> Optimization Problem
"""


from timeit import default_timer as timer
"""
best sum: return shortest list adds up to target sum

Buttom_up:
E.g. [8, [2, 3, 5]]:
    [[], None, None, None, None, None, None, None]
    [[], None, [2], [3], None, [5], None, None] look at 0
    --> Skip 1
    [[], None, [2], [3], [2, 2], [2, 3] | [5], None, [2, 5], None] look at 2
    --> [5] get to stay since shorter
    [[], None, [2], [3], [2, 2], [5], [3, 3], [2, 5], [3, 5]] look at 3
    [[], None, [2], [3], [2, 2], [5], [3, 3], [2, 5], [3, 5]] look at 4
"""

# Brute Force
def bestSum(tar, nums, length=None, lst=None):
    if not length:
        length = tar
    if not tar:
        return []
    elif tar < 0:
        return None

    for num in nums:
        rem = tar - num
        rst = bestSum(rem, nums)
        if rst is not None and len(rst + [num]) < length:
            length = len(rst + [num])
            lst = rst + [num]
    if lst:
        return lst
    return None


start = timer()
print(bestSum(60, [3, 6]))
end = timer()
print(f"Naive time: {end - start}")
# m --> tar, n --> lst length
# Time: O(n^m * m)


# Memoized
def bestSum_topdown(tar, nums, d={}):
    if tar in d:
        return d[tar]
    if not tar:
        return []
    elif tar < 0:
        return None

    shortest_combo = None

    for num in nums:
        rem = tar - num
        rst = bestSum_topdown(rem, nums, d)

        if rst is not None:
            combo = rst + [num]
            if shortest_combo is None or len(combo) < len(shortest_combo):
                shortest_combo = combo

    d[tar] = shortest_combo
    return shortest_combo


start = timer()
print(bestSum_topdown(303, [3, 6, 14]))
end = timer()
print(f"Naive time: {end - start}")
# O(m^2 *n)


# Tabulation
def bestSum_bottom_up(tar, nums):
    lst = [[], *[None] * tar]

    for i in range(tar):
        if lst[i] is not None:
            for num in nums:
                if i + num <= tar:
                    comb = [*lst[i], num]
                    lst[i + num] = comb if not lst[i + num] or len(comb) < len(lst[i + num]) else lst[i + num]
                    # Check the length or is None
    return lst[tar]


start = timer()
print(bestSum_bottom_up(303, [14, 3, 6]))
end = timer()
print(f"Naive time: {end - start}")
# O(m^2 *n)
