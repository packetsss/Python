from timeit import default_timer as timer


def Fibonacci(n):
    if n < 2:
        return n
    else:
        return Fibonacci(n - 2) + Fibonacci(n - 1)


start = timer()
Fibonacci(30)
end = timer()
print(f"Naive time: {end - start}")
# Slow O(2^n) complexity since there are 2 recursive calls, O(n) space complexity

"""
Bottom-Up Dynamic Programming:
    - Start by looking at the smallest possible sub-problem
    - Use loop
    
    - Tabulation: 
        - Storing results of sub-problems from a bottom-up approach

Top-down Dynamic Programming:
    - First looks at the main problem and breaks it into smaller and smaller necessary sup-problems 
    until the base case is reached
    - Use recursion
    
    - Memoization:
        - Storing sub-problem results in a top-down approach.
        - Use dictionary
"""

hash_table = {}
def Fibonacci_topdown(n):
    # Store n in dict
    if n < 2:
        return n
    elif n in hash_table:
        return hash_table[n]
    else:
        hash_table[n] = Fibonacci_topdown(n - 2) + Fibonacci_topdown(n - 1)
        return hash_table[n]


start = timer()
Fibonacci_topdown(100)
end = timer()
print(f"Top down time: {end - start}")
# Way faster, O(n)


def Fibonacci_bottomup(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    # table for tabulation
    table = [None] * (n + 1)
    table[0] = 0  # base case 1, Fibonacci_bottomup(0) = 0
    table[1] = 1  # base case 2, Fibonacci_bottomup(1) = 1
    # filling up tabulation table starting from 2 and going upto n
    for i in range(2, n + 1):
        # we have result of i-1 and i-2 available because these had been evaluated already
        table[i] = table[i - 1] + table[i - 2]
        # return the value of n in tabulation table
    return table[n]


start = timer()
Fibonacci_bottomup(100)
end = timer()
print(f"Bottom up time: {end - start}")
# Even Faster
