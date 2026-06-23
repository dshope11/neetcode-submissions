class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # One-pass complement map (value -> index): O(n) time, O(n) space.
        # Check-before-insert stops an element from matching itself.
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i

        # Alternative - brute force, every pair: O(n^2) time, O(1) space.
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [i, j]
