# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

"""
Bottom up:
    coints = [1, 2, 5], amount = 11

     0  1   2   3   4   5   6   7   8   9   10  11
    [0, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12] --> 1 - 1

    [0, 1 , 12, 12, 12, 12, 12, 12, 12, 12, 12, 12] --> 2 - 2

    [0, 1 , 1 , 12, 12, 12, 12, 12, 12, 12, 12, 12] --> 3 - 2 - lst[1]

    [0, 1 , 1 , 2 , 12, 12, 12, 12, 12, 12, 12, 12] --> 4 - 2 - lst[2]

    [0, 1 , 1 , 2 , 2 , 12, 12, 12, 12, 12, 12, 12] --> 5 - 5

    [0, 1 , 1 , 2 , 2 , 1 , 12, 12, 12, 12, 12, 12] --> 6 - 5 - lst[1]

    [0, 1 , 1 , 2 , 2 , 1 , 2 , 12, 12, 12, 12, 12] --> 7 - 5 - lst[2]

    [0, 1 , 1 , 2 , 2 , 1 , 2 , 2 , 12, 12, 12, 12] --> 8 - 5 - lst[3]

    [0, 1 , 1 , 2 , 2 , 1 , 2 , 2 , 3 , 12, 12, 12] --> 9 - 5 - lst[4]

    [0, 1 , 1 , 2 , 2 , 1 , 2 , 2 , 3 , 3 , 12, 12] --> 10 - 5 - lst[5]

    [0, 1 , 1 , 2 , 2 , 1 , 2 , 2 , 3 , 3 , 2 , 12] --> 11 - 5 - lst[5] = 3 (answer)

    [0, 1 , 1 , 2 , 2 , 1 , 2 , 2 , 3 , 3 , 2 , 3 ]
"""

def num_coins(cents):
    coins = [25, 10, 5, 1]
    count = 0
    for coin in coins:
        while cents >= coin:
            cents = cents - coin
            count = count + 1

    return count


print(num_coins(32))


def _change_matrix(coin_set, change_amount):
    matrix = [[0 for _ in range(change_amount + 1)] for _ in range(len(coin_set) + 1)]
    for i in range(change_amount + 1):
        matrix[0][i] = i

    return matrix


def change_making(coins, change):
    matrix = _change_matrix(coins, change)
    for c in range(1, len(coins) + 1):
        for r in range(1, change + 1):
            if coins[c - 1] == r:
                matrix[c][r] = 1
            elif coins[c - 1] > r:
                matrix[c][r] = matrix[c-1][r]
            else:
                matrix[c][r] = min(matrix[c - 1][r], 1 + matrix[c][r - coins[c - 1]])

    return matrix[-1][-1]


print(change_making([1, 10, 25], 32))



