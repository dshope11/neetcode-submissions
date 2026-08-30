"""
Number of Islands - LeetCode 200 (Medium)
Pattern: Graphs (NeetCode section 11) - CONNECTED COMPONENTS via flood fill. The grid is
         an implicit graph: each land cell is a node, edges join 4-adjacent land cells.
         Counting islands = counting connected components = "how many times did I have to
         start a traversal."
List: Blind 75
Solved 2026-08-29 | outcome: solo (solved unassisted before any design discussion;
                    accepted on the first submission)

Raw: Data Structures & Algorithms/count-number-of-islands/submission-0.py

The ACTIVE code below is the CLEANED version - see "What changed" for every difference
from the accepted submission. David's verbatim accepted submission is preserved as Alt 1.

Style notes on the submission: `if seen[row][col] == True:` is an explicit comparison to
True (PEP 8 E712), and inconsistent with the plain truthiness test the same file uses six
lines later in the outer loop; the two outer `continue` guards restate one condition
("unvisited land") as two negatives. Both fixed in the active code, both visible in Alt 1.
Type hints were complete in the submission, including the nested `dfs` - nothing added.
neetcode.io pre-imports the typing names, so the submission omits `from typing import
List`; the curated file carries it so the file is honest standalone.

KNOWN LIMIT OF THE ACTIVE (RECURSIVE) FORM: LC 200 allows m, n <= 300, i.e. 90000 cells.
An all-land grid admits a snake path through nearly every cell, so recursion depth reaches
O(m*n) - roughly 90000 against CPython's default limit of 1000. This solution is accepted
because NeetCode's test set never hands it a large dense grid, not because it is safe at
the constraint bound. Alt 3 (iterative BFS) is the form that survives it, and is the
better answer if an interviewer asks about the upper bound.
"""

from collections import deque
from typing import List

# (dr, dc) = (row delta, column delta). First component moves the ROW, so the
# labels below are correct as written. Same table as LC 79 Word Search.
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

        # A parallel visited grid, rather than mutating `grid`. Costs O(m*n)
        # extra space but leaves the caller's input intact - see Alt 2 for the
        # destructive form that drops this array.
        seen = [[False] * n for _ in range(m)]
        n_islands = 0

        def dfs(row: int, col: int) -> None:
            """Flood fill: mark every land cell reachable from (row, col).

            Unlike the backtracking searches in section 10, the mark is NEVER
            undone. A path search must release its sentinel so other paths can
            reuse the cell; a flood fill's whole job is to make the cell
            permanently unavailable, so that the outer scan never starts a
            second island on the same landmass.
            """
            # Bounds FIRST - the value lookup below would IndexError otherwise.
            if row < 0 or row >= m or col < 0 or col >= n:
                return
            # Water, or already claimed by this or an earlier island.
            if grid[row][col] == "0" or seen[row][col]:
                return
            seen[row][col] = True
            for dr, dc in DIRECTIONS:
                dfs(row + dr, col + dc)

        for row in range(m):
            for col in range(n):
                # Every fire from here is a NEW island, because the flood fill
                # already consumed every cell of every earlier one.
                if grid[row][col] == "1" and not seen[row][col]:
                    n_islands += 1
                    dfs(row, col)

        return n_islands


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code above)
# ---------------------------------------------------------------------------
# 1. `if seen[row][col] == True:` -> folded into the value guard as a plain
#    truthiness test: `if grid[row][col] == "0" or seen[row][col]:`. Two
#    separate early returns that both mean "this cell is not fresh land"
#    collapse into one. Also fixes PEP 8 E712 (comparison to True).
# 2. Outer loop: the two negative `continue` guards became one positive
#    condition, `if grid[row][col] == "1" and not seen[row][col]:`. Same
#    branch count, but it states what fires a DFS instead of what skips one.
# 3. Added `from typing import List` and `from collections import deque`
#    (the latter for Alt 3), which neetcode.io supplies implicitly.
# 4. Added the docstring on `dfs` naming the mark-without-unmark contrast
#    against section 10, and the header note on the recursion-depth limit.
# No logic changed. The guard ORDER in dfs is untouched and deliberate:
# bounds before the grid lookup, which is the crash LC 79 taught.
#
# Complexity of the active code:
#   Time  O(m*n). The outer scan is O(m*n), and the total work across ALL flood
#         fills is O(m*n) as well, not O(m*n) each - `seen` makes the fills
#         disjoint, so each cell is ENTERED by exactly one of them. Each cell is
#         additionally CALLED up to 4 times by its neighbors and once by the
#         outer scan, but those extra calls return at a guard in O(1), so they
#         are a constant factor. Outer plus total-DFS, never outer times DFS.
#   Space O(m*n): the `seen` grid, plus an O(m*n) worst-case recursion stack on
#         a dense grid. Dropping `seen` (Alt 2) does not improve the bound - the
#         stack alone is already O(m*n), and so is the BFS queue in Alt 3. O(m*n)
#         space is not escapable here, only relocatable.


# ---------------------------------------------------------------------------
# Alt 1: David's accepted submission, verbatim. O(m*n) time, O(m*n) space.
# ---------------------------------------------------------------------------
# DIRECTIONS = [
#     (-1, 0),  # up
#     (0, 1),   # right
#     (1, 0),   # down
#     (0, -1),  # left
# ]
#
# class Solution:
#     def numIslands(self, grid: List[List[str]]) -> int:
#         m = len(grid)
#         n = len(grid[0])
#         seen = [[False] * n for _ in range(m)]
#         n_islands = 0
#
#         def dfs(row: int, col: int) -> None:
#             if row < 0 or row >= m or col < 0 or col >= n:
#                 return
#             if grid[row][col] == "0":
#                 return
#             if seen[row][col] == True:
#                 return
#             seen[row][col] = True
#             for dr, dc in DIRECTIONS:
#                 dfs(row + dr, col + dc)
#
#         for row in range(m):
#             for col in range(n):
#                 if grid[row][col] == "0":
#                     continue
#                 if seen[row][col]:
#                     continue
#                 n_islands += 1
#                 dfs(row, col)
#         return n_islands


# ---------------------------------------------------------------------------
# Alt 2: in-place sinking - no `seen` array. O(m*n) time, O(m*n) space (stack
#        only; O(1) AUXILIARY beyond the recursion).
#
# The insight: sunk land is unreachable land, so the grid IS the visited set.
# Overwrite each visited cell with "0" and the parallel array disappears.
#
# The trade is that it DESTROYS the caller's input. Worth saying out loud in an
# interview rather than doing silently - "I can drop the visited array if you
# will let me consume the grid" is the sentence. If the caller needs the grid
# afterwards, this is a bug, and it is the exact bug LC 79 review caught in the
# other direction: there the leftover mark leaked a matched path back to the
# caller. Same mechanism, opposite verdict, because here the mark is the point.
# ---------------------------------------------------------------------------
# class Solution:
#     def numIslands(self, grid: List[List[str]]) -> int:
#         m = len(grid)
#         n = len(grid[0])
#         n_islands = 0
#
#         def sink(row: int, col: int) -> None:
#             if row < 0 or row >= m or col < 0 or col >= n:
#                 return
#             if grid[row][col] == "0":
#                 return
#             grid[row][col] = "0"          # mark by destroying; never undone
#             for dr, dc in DIRECTIONS:
#                 sink(row + dr, col + dc)
#
#         for row in range(m):
#             for col in range(n):
#                 if grid[row][col] == "1":
#                     n_islands += 1
#                     sink(row, col)
#         return n_islands


# ---------------------------------------------------------------------------
# Alt 3: iterative BFS with an explicit queue. O(m*n) time, O(m*n) space.
#
# The form that actually survives the stated constraints (m, n <= 300 => up to
# 90000-deep recursion in the recursive versions). No call stack to overflow;
# the frontier lives in a deque on the heap.
#
# THE ONE PLACE THIS GOES WRONG: mark on ENQUEUE, not on dequeue. If a cell is
# only marked when it comes off the queue, a cell with k unvisited neighbours
# gets pushed k times before any of them pops, and the queue inflates (and the
# same cell is processed repeatedly). Marking at push time is what keeps every
# cell in the queue at most once. Same guard-on-enqueue coupling as LC 102.
# ---------------------------------------------------------------------------
# class Solution:
#     def numIslands(self, grid: List[List[str]]) -> int:
#         m = len(grid)
#         n = len(grid[0])
#         seen = [[False] * n for _ in range(m)]
#         n_islands = 0
#
#         for start_row in range(m):
#             for start_col in range(n):
#                 if grid[start_row][start_col] == "0" or seen[start_row][start_col]:
#                     continue
#                 n_islands += 1
#                 seen[start_row][start_col] = True        # mark on ENQUEUE
#                 queue = deque([(start_row, start_col)])
#                 while queue:
#                     row, col = queue.popleft()
#                     for dr, dc in DIRECTIONS:
#                         next_row, next_col = row + dr, col + dc
#                         if not (0 <= next_row < m and 0 <= next_col < n):
#                             continue
#                         if grid[next_row][next_col] == "0":
#                             continue
#                         if seen[next_row][next_col]:
#                             continue
#                         seen[next_row][next_col] = True  # mark on ENQUEUE
#                         queue.append((next_row, next_col))
#         return n_islands
