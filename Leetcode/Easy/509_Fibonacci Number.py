hash_table = {}
def Fibonacci_topdown(n):
    if n < 2:
        return n
    elif n in hash_table:
        return hash_table[n]
    else:
        hash_table[n] = Fibonacci_topdown(n - 2) + Fibonacci_topdown(n - 1)
        return hash_table[n]
