# Two Sum (LC 1) | Arrays & Hashing | Blind 75
# Solved 2026-06-21 on neetcode.io | outcome: solo
# Style: clean. Minor: the `else` after the `return` is redundant - the
#   `seen[x] = i` line could be un-indented since the early return makes
#   the else moot.
#
# Optimal active below (one-pass complement map, value -> index, O(n) time /
# O(n) space); alternative commented at the bottom.

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            else:
                seen[x] = i

        # Alternative - brute force, every pair: O(n^2) time, O(1) space.
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [i, j]
