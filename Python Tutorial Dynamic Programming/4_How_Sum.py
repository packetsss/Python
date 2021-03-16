from timeit import default_timer as timer

"""
given a target n and a list numbers, return 1 combination of elements that add up to exactly target

(7, [2, 4]) --> Null
(7, [2, 3]) --> [2, 2, 3]
(7, [5, 3, 4, 7]) --> [7]

                7
       /     /     \    \
      2     4       3    0
           / \       |
          1   0      0

"""

def howSum(tar, nums):
    if not tar:
        return []
    elif tar < 0:
        return None

    for num in nums:
        rem = tar - num
        rst = howSum(rem, nums)
        if rst is not None:
            return rst + [num]
    return None


start = timer()
print(howSum(92, [6, 3]))
end = timer()
print(f"Naive time: {end - start}")
# m --> tar, n --> lst length
# Time: O(n^m * m)

def howSun_topdown(tar, nums, d=None):
    if d is None:
        d = {}
    elif tar in d:
        return d[tar]
    # return memorized value instead of recalculating
    elif not tar:
        return []
    elif tar < 0:
        return None

    for num in nums:
        rem = tar - num
        rst = howSun_topdown(rem, nums, d)
        if rst is not None:
            d[tar] = rst + [num]
            # memorize it
            return d[tar]
    d[tar] = None
    return None


start = timer()
print(howSun_topdown(300, [7, 14, 15]))
end = timer()
print(f"Naive time: {end - start}")
# Time: O(n * m^2)



