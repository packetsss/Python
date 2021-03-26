m, n = 3, 7

def uniquePaths(m, n):
    table = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    table[1][1:] = [1] * n
    for i in range(1, m + 1):
        table[i][1] = 1
    
    for i in range(2, m + 1):
        for j in range(2, n + 1):
            table[i][j] = table[i - 1][j] + table[i][j - 1]
    return table[m][n]


print(uniquePaths(m, n))

def uniquePaths1(n, m):
    table = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    table[1][1] = 1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cur = table[i][j]
            if i < m:
                table[i + 1][j] += cur
            if j < n:
                table[i][j + 1] += cur

    return table[m][n]


print(uniquePaths1(m, n))
