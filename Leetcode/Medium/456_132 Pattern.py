
def find132pattern(nums):
    if len(set(nums)) < 3:
        return False
    cond = False
    fst = max(nums)
    for i in range(len(nums) - 2):
        if nums[i] <= fst:
            fst = nums[i]
            idx = i
            for j in range(idx, len(nums) - 1):

                if nums[j] > nums[i]:
                    for k in range(j, len(nums)):
                        if nums[i] < nums[k] < nums[j]:
                            return True
                if nums[j] < fst:
                    fst = nums[j]
                    idx = j
                    break
    return cond


print(find132pattern([42, 43, 6, 12, 3, 4, 6, 11, 20]))
