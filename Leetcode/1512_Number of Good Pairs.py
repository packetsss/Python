nums = [1,2,3]

tot = 0
for i in range(len(nums)):
    tot = tot + nums[i:].count(nums[i]) - 1

print(tot)