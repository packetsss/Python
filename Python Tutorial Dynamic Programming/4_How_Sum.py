from timeit import default_timer as timer

"""
given a target n and a list numbers, return 1 combination of elements that add up to exactly target

(7, [2, 4]) --> None
(7, [2, 3]) --> [2, 2, 3]
(7, [5, 3, 4, 7]) --> [7]

                7
       /     /     \    \
      2     4       3    0
           / \       |
          1   0      0

Buttom_up:
E.g. [7, [5, 3, 4]]:
    [[], None, None, None, None, None, None, None]
    [[], None, None, [3], [4], [5], None, None]
    --> Skip 1 & 2 <--
    [[], None, None, [3], [4], [5], [3, 3], [3, 4]]
    --> Already valid <-- (can break out early)
    [[], None, None, [3], [4], [5], [3, 3], [4, 3]]


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
print(howSum(60, [6, 3]))
end = timer()
print(f"Naive time: {end - start}")
# m --> tar, n --> lst length
# Time: O(n^m * m)

# Memoization
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


# Tabulation
def howSum_buttom_up(tar, nums):
    lst = [[], *[None] * tar]

    for i in range(tar):
        if lst[i] is not None:
            for num in nums:
                if i + num <= tar:
                    lst[i + num] = [*lst[i], num]
                    # list concatenation
    return lst[tar]


start = timer()
print(howSum_buttom_up(300, [7, 14, 15]))
end = timer()
print(f"Naive time: {end - start}")
# Time: O(n * m^2)

# Just change type and a few assignments compare to canSum
