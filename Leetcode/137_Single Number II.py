nums = [0, 1, 0, 1, 0, 1, 99]

while len(nums) != 1:
    temp = nums[0]
    nums.pop(0)
    if temp in nums:
        nums.remove(temp)
        nums.remove(temp)
    else:
        nums.append(temp)
        print(temp)
        break

print(nums[0])
