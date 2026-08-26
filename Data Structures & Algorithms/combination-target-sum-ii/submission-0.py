from typing import List

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        res: List[List[int]] = []
        subset: List[int] = []
        cands = sorted(candidates)

        def dfs(start: int, total: int) -> None:
            if total == target:
                res.append(subset[:])
                return
            
            for j in range(start, len(cands)):
                if j > start and cands[j] == cands[j-1]:
                    continue
                if total + cands[j] > target:
                    break
                subset.append(cands[j])
                dfs(j+1, total + cands[j])
                subset.pop()
            
        dfs(0, 0)
        return res