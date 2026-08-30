
DIRECTIONS = [
    (-1, 0),  # up
    (0, 1),   # right
    (1, 0),   # down
    (0, -1),  # left
]

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m = len(grid)
        n = len(grid[0])
        seen = [[False] * n for _ in range(m)]
        n_islands = 0

        def dfs(row: int, col: int) -> None:
            if row < 0 or row >= m or col < 0 or col >= n:
                return
            if grid[row][col] == "0":
                return
            if seen[row][col] == True:
                return
            seen[row][col] = True
            for dr, dc in DIRECTIONS:
                dfs(row + dr, col + dc)

        for row in range(m):
            for col in range(n):
                if grid[row][col] == "0":
                    continue
                if seen[row][col]:
                    continue
                n_islands += 1
                dfs(row, col)
        return n_islands
