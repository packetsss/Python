# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited


"""
Given 2 strings, find the longest common subsequence present in both strings
"""

from timeit import default_timer as timer
P = "ABTQCID"
Q = "ABACD"


def LCS(P, Q, n, m):

    if n == 0 or m == 0:
        result = 0
    elif P[n-1] == Q[m-1]:

        # if they end with same letter, get rid of it and find LCS without the last letter
        result = 1 + LCS(P, Q, n - 1, m - 1)

    elif P[n-1] != Q[m-1]:
        tmp1 = LCS(P, Q, n-1, m)
        # get rid of the last value of P and try to solve it
        tmp2 = LCS(P, Q, n, m-1)
        # repeat with Q
        result = max(tmp2, tmp1)
    return result


s = timer()
print(LCS(P, Q, len(P), len(Q)))
e = timer()
print(e - s)

def LCS_topdown(P, Q, n, m, d):
    key = f"{n}{m}"
    if key in d:
        return d[key]
    if n == 0 or m == 0:
        result = 0
    elif P[n-1] == Q[m-1]:

        # if they end with same letter, get rid of it and find LCS without the last letter
        result = 1 + LCS_topdown(P, Q, n - 1, m - 1, d)
    elif P[n-1] != Q[m-1]:
        tmp1 = LCS_topdown(P, Q, n-1, m, d)
        # get rid of the last value of P and try to solve it
        tmp2 = LCS_topdown(P, Q, n, m-1, d)
        # repeat with Q
        result = max(tmp2, tmp1)
    d[key] = result
    return result


s = timer()
print(LCS_topdown(P, Q, len(P), len(Q), {}))
e = timer()
print(e - s)
# Time: O(n*m)


def LCS_bottom_up(P, Q, n, m):
    lst = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            if P[i] == Q[j]:

                lst[i + 1][j + 1] += 1 + lst[i][j]
            else:
                lst[i + 1][j + 1] = max(lst[i + 1][j], lst[i][j + 1])

    return lst[n][m]


s = timer()
print(LCS_bottom_up(P, Q, len(P), len(Q)))
e = timer()
print(e - s)
