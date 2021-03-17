"""
Dynamic Programming:
    - Notice any overlapping subproblems
    - decide what is the trivially smartest input
    - think recursively to use Memoization
    - think iteratively to use Tabulation
    - Draw strategy FIRST!!!!

    Bottom-Up Dynamic Programming:
        - Start by looking at the smallest possible sub-problem then work the way up until reach the result
        - Use loop

        - Tabulation:
            - Storing results of sub-problems from a bottom-up approach

            - Visualize the problem as a table
            - Size the table based on inputs (Usually off by 1)
            - Initialize table with default values(depends on the answer required)
            - Seed the trivial answer into the table
            - Iterate through the table
            - Fill further positions based on current position

    Top-down Dynamic Programming:
        - First looks at the main problem and breaks it into smaller and smaller necessary sup-problems
        until the base case is reached
        - Use recursion

        - Memoization:
            - Storing sub-problem results in a top-down approach.
            - Use dictionary

            - Make it work
                - Visualize the problem as a tree
                - Implement the tree using recursion (brute force recursion)
                - Test it
            - Make it efficient
                - Adding a dict(memo) object
                - Add a base case to return dict values
                - Store return values into the dict
"""

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


hash_table = {}
def Fibonacci_topdown(n):
    # Store n in dict
    if n < 2:
        return n
    elif n in hash_table:
        return hash_table[n]
    else:
        hash_table[n] = Fibonacci_topdown(n - 2) + Fibonacci_topdown(n - 1)
        # calculate and store all values in n - 2, and then use (n - 3) + (n - 2) to calculate n - 1
        return hash_table[n]


start = timer()
Fibonacci_topdown(100)
end = timer()
print(f"Top down time: {end - start}")
# Way faster, O(n)

# Tabulation
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
print(Fibonacci_bottomup(100))
end = timer()
print(f"Bottom up time: {end - start}")
# Even Faster

def Fibonacci_bottomup_1(n):
    lst = [0] * (n + 1)
    lst[1] = 1
    for i in range(len(lst) - 1):
        if i > n - 2:
            lst[i + 1] += lst[i]
        else:
            lst[i + 1] += lst[i]
            lst[i + 2] += lst[i]
    return lst[n]


start = timer()
print(Fibonacci_bottomup_1(100))
end = timer()
print(f"Bottom up time: {end - start}")
