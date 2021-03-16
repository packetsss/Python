from timeit import default_timer as timer

"""
Return a boolean indicates if the target can be constructed by concatenating strs in a word bank

["skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]] --> False
["abcdef", ["ab", "abc", "cd", "def", "abcd"]]
                    abcdef
             /ab     |abc     \abcd (No cd because it's in the middle)
           cdef     def        ef
           /cd       |def       
          ef         "" (True)
"""

def canConstruct(tar, bank):
    if tar == "":
        return True
    for word in bank:
        if word == tar[:len(word)]:
            suffix = tar[len(word):]

            # get the rest of tar - word
            if canConstruct(suffix, bank):
                return True
    return False


start = timer()
print(canConstruct("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]))
print(canConstruct("abcdef", ["ab", "abc", "cd", "def", "abcd"]))
'''print(canConstruct("eeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee"]))'''
end = timer()
print(f"Naive time: {end - start}")
# m --> tar length(height of the tree), n --> bank length
# Time: o(n^m * m)


def canConstruct_topdown(tar, bank, d):
    if tar in d:
        return d[tar]
    if tar == "":
        return True

    for word in bank:
        if word == tar[:len(word)]:
            suffix = tar[len(word):]
            if canConstruct_topdown(suffix, bank, d):
                d[tar] = True
                return True

    d[tar] = False
    return False


start = timer()
print(canConstruct_topdown("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"], {}))
print(canConstruct_topdown("abcdef", ["ab", "abc", "cd", "def", "abcd"], {}))
print(canConstruct_topdown("eeeeeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee", "c", "r"], {}))
end = timer()
print(f"Dynamic time: {end - start}")
# Time: O(n * m^2)
