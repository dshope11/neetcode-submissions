from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []
        used: List[int] = []
        perm: List[int] = []

        def dfs(used: List[int]):
            if len(used) == len(nums):
                res.append(perm[:])
                return
            for i in range(len(nums)):
                if i in used:
                    continue
                perm.append(nums[i])
                used.append(i)
                dfs(used)
                perm.pop()
                used.pop()

        dfs(used)
        return res
