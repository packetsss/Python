nums = [1,2,3,4,4,3,2,1]
n = 4

num = nums[:n]
l = nums[n:]

for i in range(0, len(nums), 2):
    num.insert(i + 1, l[int(i/2)])

print(num)
