from timeit import default_timer as timer

"""
Return number of ways that the target can be constructed by concatenating strs in a word bank

["skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]] --> 0
["abcdef", ["ab", "abc", "cd", "def", "abcd"]] --> 1
["purple", ["purp", "p", "ur", "le", "purpl"]] --> 2
["eeeeeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee", "c", "r"]] --> 0

Bottom up:
    E.g. ["purple", ["purp", "p", "ur", "le", "purpl"]]
        [1, 0, 0, 0, 0, 0, 0]
        [p, u, r, p, l, e,  ]
        
        [1, 1, 0, 0, 1, 1, 0]
        --> Add purp, p, purpl
        
        [1, 1, 0, 1, 1, 1, 0]
        --> Add ur
        
        [1, 1, 0, 1, 2, 1, 0]
        --> Add p
        
        [1, 1, 0, 1, 2, 1, 2]
        --> Add le
"""

def countConstruct(tar, bank):
    if tar == "":
        return 1

    tot = 0

    for word in bank:
        if word == tar[:len(word)]:
            ways = countConstruct(tar[len(word):], bank)
            tot += ways

    return tot


start = timer()
print(countConstruct("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]))
print(countConstruct("abcdef", ["ab", "abc", "cd", "def", "abcd"]))
print(countConstruct("purple", ["purp", "p", "ur", "le", "purpl"]))
'''print(canConstruct("eeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee"]))'''
end = timer()
print(f"Naive time: {end - start}")
# Time: o(n^m * m)


# Memoization
def countConstruct_topdown(tar, bank, d):
    if tar in d:
        return d[tar]
    if tar == "":
        return 1

    tot = 0

    for word in bank:
        if word == tar[:len(word)]:
            tot += countConstruct_topdown(tar[len(word):], bank, d)
    d[tar] = tot
    # just add the total count to dictionary
    return tot


start = timer()
print(countConstruct_topdown("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"], {}))
print(countConstruct_topdown("abcdef", ["ab", "abc", "cd", "def", "abcd"], {}))
print(countConstruct_topdown("purple", ["purp", "p", "ur", "le", "purpl"], {}))
print(countConstruct_topdown("eeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee"], {}))
end = timer()
print(f"Naive time: {end - start}")
# Time: O(n * m^2)


# Tabulation
def countConstruct_bottom_up(tar, bank):
    lst = [1, *[0] * len(tar)]

    for i in range(len(tar)):
        if lst[i]:
            for word in bank:
                if word == tar[i:len(word) + i]:
                    lst[i + len(word)] += lst[i]
    return lst[len(tar)]


start = timer()
print(countConstruct_bottom_up("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]))
print(countConstruct_bottom_up("abcdef", ["ab", "abc", "cd", "def", "abcd"]))
print(countConstruct_bottom_up("purple", ["purp", "p", "ur", "le", "purpl"]))
print(countConstruct_bottom_up("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee"]))
end = timer()
print(f"Naive time: {end - start}")
# Time: O(n * m^2)
