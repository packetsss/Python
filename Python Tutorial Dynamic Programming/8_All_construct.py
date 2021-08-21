from timeit import default_timer as timer

"""
Return a 2D array of all ways that the target can be constructed by concatenating strs in a word bank

["skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]] --> []
["abcdef", ["ab", "abc", "cd", "def", "abcd"]] --> [["abd", "def"]]
["purple", ["purp", "p", "ur", "le", "purpl"]] --> [["purp", "le"], ["p", "ur", "p", "le"]]
["eeeeeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee", "c", "r"]] --> []


Bottom up:
    E.g. ["abcdef", ["ab", "abc", "cd", "def", "abcd", "ef", "c"]]
        [[[]], [], [], [], [], [], [], []]
        [[[]], [], [], [[ab]], [[abc]], [[abcd]], [], []]
        --> look at words start with a
        
        [[[]], [], [], [[ab]], [[abc], [c]], [[abcd], [ab, cd]], [], [[abc, def], [ab, c, def]]]
        --> look at position 3 and 4
        
        [[[]], [], [], [[ab]], [[abc], [c]], [[abcd], [ab, cd]], [], [[abc, def], [ab, c, def], [abcd, ef], [ab,cd,ef]]]
        --> look at position 5 and 7
"""

def allConstruct(tar, bank):
    if tar == "":
        return [[]]

    rst = []

    for word in bank:
        if word == tar[:len(word)]:
            suf_ways = allConstruct(tar[len(word):], bank)
            tar_ways = [[word] + way for way in suf_ways]

            rst.extend(tar_ways)

    return rst


start = timer()
print(allConstruct("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]))
print(allConstruct("abcdef", ["ab", "abc", "cd", "def", "abcd"]))
print(allConstruct("purple", ["purp", "p", "ur", "le", "purpl"]))
'''print(allConstruct("eeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee"]))'''
end = timer()
print(f"Naive time: {end - start}")
# Time: o(n^m * m)


# Memoization
def allConstruct_topdown(tar, bank, d):
    if tar in d:
        return d[tar]
    if tar == "":
        return [[]]

    rst = []

    for word in bank:
        if word == tar[:len(word)]:
            suf_ways = allConstruct_topdown(tar[len(word):], bank, d)
            tar_ways = [[word] + way for way in suf_ways]

            rst.extend(tar_ways)
    d[tar] = rst
    return rst


start = timer()
print(allConstruct_topdown("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"], {}))
print(allConstruct_topdown("abcdef", ["ab", "abc", "cd", "def", "abcd"], {}))
print(allConstruct_topdown("purple", ["purp", "p", "ur", "le", "purpl"], {}))
print(allConstruct_topdown("eeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee"], {}))
end = timer()
print(f"Naive time: {end - start}")
# Time: o(n^m)


# Tabulation
def allConstruct_bottom_up(tar, bank):
    lst = [[] for _ in range(len(tar) + 1)]
    lst[0] = [[]]

    for i in range(len(tar)):
        for word in bank:
            if word == tar[i:len(word) + i]:
                new_combo = [[*way, word] for way in lst[i]]
                # add new word + existing word to the new combo
                lst[i + len(word)].extend(new_combo)
                # concatenate new combo to len(word) ahead

    return lst[len(tar)]


start = timer()
print(allConstruct_bottom_up("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]))
print(allConstruct_bottom_up("abcdef", ["ab", "abc", "cd", "def", "abcd"]))
print(allConstruct_bottom_up("purple", ["purp", "p", "ur", "le", "purpl"]))
print(allConstruct_bottom_up("eeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee"]))
end = timer()
print(f"Naive time: {end - start}")
# Time: o(n^m) --> Very slow for some reason
