class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # pass 1 - construct prefix array "in-place" in result
        res = [1] * (len(nums))

        running_prefix = 1
        for i in range((len(nums))):
            res[i] = running_prefix
            running_prefix *= nums[i]
        running_postfix = 1
        for i in range(len(nums) - 1, -1, -1):
            res[i] *= running_postfix
            running_postfix *= nums[i]
        return res