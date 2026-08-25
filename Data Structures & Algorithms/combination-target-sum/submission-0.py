
from typing import List

class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        res: List[List[int]] = []
        subset: List[int] = []
        
        def dfs(start: int) -> None:
            total = 0
            for num in subset:
                total += num
            if total == target:
                res.append(subset[:])
            elif total > target:
                return
            for j in range(start, len(nums)):
                subset.append(nums[j])
                dfs(j)
                subset.pop()
            return

        dfs(0)
        return res