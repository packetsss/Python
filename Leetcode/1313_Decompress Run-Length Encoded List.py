nums = [1,1,2,3]

l = []
for x, y in zip(*[iter(nums)] * 2):
    l += [y] * x

print(l)
# print(list(zip(*[iter(nums)]*2)))
print(next(iter(nums)))

