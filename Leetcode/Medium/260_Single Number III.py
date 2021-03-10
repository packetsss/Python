nums = [1]
list1 = []

while len(nums) != 0:
    temp = nums[0]
    nums.pop(0)
    if temp in nums:
        nums.remove(temp)
    else:
        list1.append(temp)


print(list1)
