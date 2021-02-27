nums = [17, 12, 5, -6, 12, 4, 17, -5, 2, -3, 2, 4, 5, 16, -3, -4, 15, 15, -4, -5, -6]

while len(nums) != 1:
    temp = nums[0]
    nums.pop(0)
    if temp in nums:
        nums.remove(temp)
    else:
        nums.append(temp)
        break

print(temp)
