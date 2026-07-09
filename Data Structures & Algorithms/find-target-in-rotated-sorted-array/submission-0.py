class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo = 0
        hi = len(nums) - 1

        while lo < hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] < nums[hi]:
                hi = mid
            else:
                lo = mid + 1
        p = lo

        if target <= nums[-1]:
            lo = p
            hi = len(nums) - 1
        else:
            lo = 0
            hi = p - 1

        while lo <= hi:
            middle = lo + (hi - lo) // 2
            if nums[middle] == target:
                return middle
            if nums[middle] > target:
                hi = middle - 1
            else:
                lo = middle + 1

        return -1