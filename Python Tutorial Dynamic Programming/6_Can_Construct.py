# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from timeit import default_timer as timer

"""
Return a boolean indicates if the target can be constructed by concatenating strs in a word bank

Top-down:
    ["skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]] --> False
    ["abcdef", ["ab", "abc", "cd", "def", "abcd"]]
    
                        abcdef
                 /ab     |abc     \abcd (No cd because it's in the middle)
               cdef     def        ef
               /cd       |def       
              ef         "" (True)
       
          
Bottom-up:
    E.g. ["abcdef", ["ab", "abc", "cd", "def", "abcd"]]
    
        [True, False, False, False, False, False, False]
        [  a ,   b  ,   c  ,   d  ,   e  ,   f  ]
        --> 1st string is empty so True
        
        [True, False, True, True, True, False, False]
        [             ab  , abc , abcd,             ]
        --> skip False at 1
        
        [True, False, True, True, True, False, True]
        [             ab  , abc , abcd||cd,  , def ]
        --> return True
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


# Memoization
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


# Tabulation
def canConstruct_bottom_up(tar, bank):
    lst = [True, *[False] * len(tar)]

    for i in range(len(tar)):
        if lst[i]:
            for word in bank:
                if word == tar[i:len(word) + i]:
                    # if word match exactly to the correct portion of the target
                    lst[len(word) + i] = True
    return lst[len(tar)]


start = timer()
print(canConstruct_bottom_up("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]))
print(canConstruct_bottom_up("abcdef", ["ab", "abc", "cd", "def", "abcd"]))
print(canConstruct_bottom_up("eeeeeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeee", "c", "r"]))
end = timer()
print(f"Dynamic time: {end - start}")
# Time: O(n * m^2)
