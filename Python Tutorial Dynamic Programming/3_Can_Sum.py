from timeit import default_timer as timer


"""
given a target sum n and a list numbers, return True if numbers in the list can sum up to the target sum

(7, [2, 4]) --> False
(7, [2, 3]) --> True

"""

def canSum(target, numbers):
    if target == 0:
        return True
    elif target < 0:
        return False

    for i in numbers:
        reminder = target - i
        if canSum(reminder, numbers):
            return True
    return False


start = timer()
print(canSum(91, [6, 3]))
end = timer()
print(f"Naive time: {end - start}")
# Time: O(n^m)


### Memoized
def canSum_d(target, numbers, d=None):
    if d is None:
        d = {}
    if target == 0:
        return True
    elif target < 0:
        return False
    elif target in d:
        return d[target]

    for i in numbers:
        reminder = target - i
        d[target] = canSum_d(reminder, numbers, d)
        if d[target]:
            return True
    return False


start = timer()
print(canSum_d(1121, [6, 7]))
end = timer()
print(f"Dynamic time: {end - start}")
# m --> tar, n --> length
# Time: O(m * n)


def canSum_d2(target, numbers, d=None):
    if d is None:
        d = {}
    if target == 0:
        return True
    elif target < 0:
        return False
    elif target in d:
        return d[target]

    for i in numbers:
        reminder = target - i

        if canSum_d(reminder, numbers, d):
            d[target] = True
            return True
    d[target] = False
    return False


start = timer()
print(canSum_d2(1121, [6, 7]))
end = timer()
print(f"Dynamic time: {end - start}")
# m --> tar, n --> length
# Time: O(m * n)


### Tabulation
def canSum_botup(tar, nums):

    lst = [False] * (tar + 1)
    lst[0] = True
    for i in range(tar):
        if lst[i]:
            for num in nums:

                lst[i + num] = True
        if lst[-1]:
            return True
    return False


start = timer()
print(canSum_botup(1121, [6, 7]))
end = timer()
print(f"Dynamic time: {end - start}")
# Time: O(m * n)

