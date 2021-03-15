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
    matrix = [[0 for m in range(change_amount + 1)] for m in range(len(coin_set) + 1)]
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



