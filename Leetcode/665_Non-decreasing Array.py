class Solution:
    @staticmethod
    def check_Possibility(nums):
        for x in range(len(nums)):
            try:
                if nums[x] > nums[x + 1]:
                    if nums[x] == nums[0]:
                        nums[x] = nums[x + 1]
                    elif nums[x + 2] > nums[x]:
                        nums[x + 1] = nums[x]
                    else:
                        nums[x] = nums[x + 1]
                        print(nums)
                    for i in range(len(nums)):
                        if nums[i] > nums[i + 1]:
                            print(nums)
                            return False
                            break
            except:
                print(nums)
                return True


print(Solution.check_Possibility([-1, 4, 2, 3]))
