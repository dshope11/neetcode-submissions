class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo = 0
        hi = len(nums) - 1

        while lo <= hi:
            middle = lo + (hi - lo) // 2
            if nums[middle] == target:
                return middle
            if nums[middle] > target:
                hi = middle - 1
            elif nums[middle] < target:
                lo = middle + 1

        return -1