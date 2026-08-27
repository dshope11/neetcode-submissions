
from typing import List

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []
        subset: List[int] = []
        candidates = sorted(nums)

        def dfs(start: int) -> None:
            res.append(subset[:])
            for j in range(start, len(candidates)):
                if j > start and candidates[j] == candidates[j - 1]:
                    continue
                subset.append(candidates[j])
                dfs(j + 1)
                subset.pop()
        
        dfs(0)
        return res