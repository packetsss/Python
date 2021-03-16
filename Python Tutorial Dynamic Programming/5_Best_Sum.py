from timeit import default_timer as timer

"""
best sum: return shortest list adds up to target sum


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
print(bestSum_topdown(60, [3, 6]))
end = timer()
print(f"Naive time: {end - start}")
# O(m^2 *n)

"""
canSum --> Decision Problem
howSum --> Combinatorics Problem
bestSum --> Optimization Problem
"""
