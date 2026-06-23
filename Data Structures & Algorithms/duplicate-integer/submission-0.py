class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        # Seen-set: O(n) time, O(n) space.
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

        # Alternative - sort first, then scan neighbors: O(n log n) time, O(1) space.
        # Trades the hash's O(n) space for time; mutates the input.
        # nums.sort()
        # for i in range(1, len(nums)):
        #     if nums[i] == nums[i - 1]:
        #         return True
        # return False

        # Alternative - set-length one-liner: O(n) time, O(n) space.
        # return len(set(nums)) != len(nums)
