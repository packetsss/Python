"""
Giving a stair with n stairs, find # of ways get to the top by taking either 1 or 2 steps

we only care about current step - 1 and - 2
"""

steps = 300

def climb(step, memo=None):
    if memo is None:
        memo = {}
    if step in memo:
        return memo[step]
    if step < 2:
        return 1
    else:
        memo[step] = climb(step - 2, memo) + climb(step - 1, memo)
        return memo[step]


print(climb(steps))
