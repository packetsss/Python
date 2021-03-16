s = "ababcacac"
s1 = "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff" \
     "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff" \
     "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff" \
     "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff" \
     "ffffffffffffffffffffffffffffffffffffffffffffffffffggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg" \
     "ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg" \
     "ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg" \
     "ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg" \
     "ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg"

"""
ababbcavav <--> babbcavava 11 - 10 + 1 = 2, 0:11, 1:12
ababbcava <--> babbcavav <--> abbcavava 11 - 9 + 1 = 3 0:10, 1:11, 2:12
ababbcav <--> babbcava <--> abbcavav <--> bbcavava 11 - 8 + 1 = 4
ababbca <--> babbcav <--> abbcava <--> bbcavav <--> bcavava 11 - 7 + 1 = 5
"""

def Palindrome(string):
    length = 1
    rst = ""

    for i in range(len(string)):
        for j in range(len(string) + 1):
            slices = string[i:j]
            if len(slices) > 1:

                if slices == slices[::-1] and len(slices) > length:
                    length = len(slices)
                    rst = slices
    if length == 1:
        return string[0]
    return rst


print(Palindrome(s1))


def Palindrome_r(length, string):

    if length == 1:
        return string[0]

    iter_times = len(string) - length + 1

    for i in range(iter_times + 1):
        slices = string[i:len(string) - iter_times + i]
        if slices == slices[::-1]:
            return slices

    return Palindrome_r(length - 1, string)


print(Palindrome_r(len(s1) + 1, s1))


def Palindrome_r1(string, d):
    #print(d)
    if len(string) == 1:
        return string
    if string in d:
        return string if d[string] else ""

    if string == string[::-1]:
        d[string] = True
        return string
    d[string] = False
    return max(Palindrome_r1(string[:-1], d), Palindrome_r1(string[1:], d), key=len)


print(Palindrome_r1(s1, {}))
