
DIRECTIONS = [
    (-1, 0),  # up
    (0, 1),   # right
    (1, 0),   # down
    (0, -1),  # left
]

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        pacific_reachable = set()
        atlantic_reachable = set()
        m = len(heights) # number of rows
        n = len(heights[0]) # number of columns

        stack = [(r,0) for r in range(m)]
        stack.extend([(0,c) for c in range(1, n)])

        pacific_reachable.update((r, c) for r, c in stack)

        while stack:
            r, c = stack.pop()
            for dr, dc in DIRECTIONS:
                nr = r + dr
                nc = c + dc
                if nr < 0 or nr >= m or nc < 0 or nc >= n:
                    continue
                if heights[nr][nc] < heights[r][c]:
                    continue
                if (nr, nc) in pacific_reachable:
                    continue
                pacific_reachable.add((nr, nc))
                stack.append((nr, nc))

        stack = [(r,n-1) for r in range(m)]
        stack.extend([(m-1,c) for c in range(n-1)])

        atlantic_reachable.update((r, c) for r, c in stack)

        while stack:
            r, c = stack.pop()
            for dr, dc in DIRECTIONS:
                nr = r + dr
                nc = c + dc
                if nr < 0 or nr >= m or nc < 0 or nc >= n:
                    continue
                if heights[nr][nc] < heights[r][c]:
                    continue
                if (nr, nc) in atlantic_reachable:
                    continue
                atlantic_reachable.add((nr, nc))
                stack.append((nr, nc))

        return [[r,c] for r,c in pacific_reachable & atlantic_reachable]





