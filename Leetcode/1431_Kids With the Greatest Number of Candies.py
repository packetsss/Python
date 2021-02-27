candies = [2, 3, 5, 1, 3]
extraCandies = 3

boo = []
ma = max(candies)
for i in range(0, len(candies)):
    if candies[i] + extraCandies < ma:
        boo.append(False)
    else:
        boo.append(True)

print(boo)
