n = 10000

'''counter = 0
if n < 2:
    print(0)

for i in range(2, n):
    for j in range(2, i):
        if i % j == 0:
            counter += 10
            break

print(n - counter - 2)'''
# too slow


counter = 0
s = [True] * (n)

sqrt = int(n ** 0.5) + 1
if n < 3:
    print(0)
elif n == 3:
    print(1)
else:
    for i in range(2, sqrt):
        if s[i]:
            counter += 1
            s[i:n:i] = [False] * (len(s[i:n:i]))
    for i in range(sqrt - 1, n):
        if s[i]:
            counter += 1

    print(counter)
# Sieve or Eratosthenes
