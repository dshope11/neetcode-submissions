"""
Pacific Atlantic Water Flow - LeetCode 417 (Medium)
Pattern: Graphs (NeetCode section 11) - multi-source flood fill run BACKWARDS. The problem
         asks a question per cell ("can water get from here to the ocean?"); the solution
         inverts it into a question per ocean ("which cells can reach me?") and runs one
         search per ocean instead of one per cell.
List: Blind 75
Solved 2026-09-01 | outcome: hint (design driven solo - the inversion, the memoization
                    dead-end, the amortization argument, and the recursion-depth trap were
                    all his; four pushes needed - see the solve log on
                    wiki/concepts/bfs-dfs.md)

Raw: Data Structures & Algorithms/pacific-atlantic-water-flow/submission-0.py

The ACTIVE code below is the CLEANED version - see "What changed" for every difference
from the accepted submission. David's verbatim accepted submission is preserved as Alt 1.

INVERT THE QUERY, AND THE VISITED SET BECOMES THE ANSWER SET.
The forward reading of the problem is "for each of the m*n cells, can I walk downhill to
the ocean?" - m*n searches, each up to O(m*n), so O((m*n)^2). Reverse the edge direction
and the question becomes "starting at the ocean, which cells can I reach walking UPHILL?"
(step to a neighbor only if heights[neighbor] >= heights[current]). That is one search per
ocean, and it collapses two structures into one: because the height comparison is a GUARD
that returns before the mark, a cell is only ever marked after it has been proven
reachable. There is no separate `seen` set - the reachable set is the visited set. The
answer is the intersection of the two.

WHY MEMOIZING THE FORWARD VERSION DOES NOT RESCUE IT.
The obvious repair to the brute force is to cache a (reaches_pacific, reaches_atlantic)
pair per cell. It is unsound, and the reason is worth keeping: water flows between cells of
EQUAL height, so the flow graph contains cycles. While the search from (5,5) is in flight,
it steps to an equal-height (5,6), which steps back at (5,5) - whose memo entry does not
exist yet. So (5,6) recurses, gets bounced by the in-progress visited mark, and concludes
"no path that way." That conclusion is premature, and caching it caches a wrong False.
Memoizing a reachability query over a CYCLIC graph is the general trap. The inversion
sidesteps it rather than patching it.

WHY THIS ONE MUST BE ITERATIVE, UNLIKE LC 133.
A recursive chain cannot contain the same cell twice (the mark forbids it), so the hard
ceiling on depth is m*n - and at the neetcode.io bound of m, n <= 100 that is 10^4 against
CPython's default recursion limit of 1000. The witness is easy to build: a 100x100 grid of
IDENTICAL heights, where every step is legal and one DFS snakes through nearly every cell
in a single unbroken chain. This is the same trap that makes the recursive LC 200 solution
dishonest at its stated bound; here it was recognised BEFORE submitting rather than found
in review. (LC 133 was checked and cleared by the same test - 100 nodes vs a limit of 1000.
Check the constraint every time; do not assume either way.)

THE SEARCH IS A PURE FUNCTION OF ITS SEEDS.
Pacific and Atlantic differ in nothing but their starting cells - not the direction of the
walk, not the comparison, nothing. That is what makes the helper extraction the right shape
rather than mere de-duplication, and it is the answer to the natural follow-up ("what if
there were four oceans?"): call `flood` k times, or carry a k-bit mask per cell and
intersect at the end.
"""

from typing import List, Set, Tuple

DIRECTIONS = [
    (-1, 0),  # up
    (0, 1),   # right
    (1, 0),   # down
    (0, -1),  # left
]


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        m = len(heights)     # number of rows
        n = len(heights[0])  # number of columns

        def flood(starts: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
            """Cells reachable by water flowing INTO the ocean seeded by `starts`.

            Multi-source: every seed goes in at once and they share one set, so
            the m + n - 1 starting cells cost one traversal between them, not
            m + n - 1 of them. Same amortization as LC 200 - outer PLUS total
            fill, never outer TIMES fill - because the marks make the work
            disjoint: each cell is entered exactly once across the whole run.
            """
            # The seeds are border cells, so they are reachable by definition -
            # no height test applies to them, only to steps taken FROM them.
            reachable = set(starts)
            stack = list(starts)  # copy: `starts` is the caller's list, and the
            #                       loop below consumes what it iterates
            while stack:
                r, c = stack.pop()  # pop() = stack = DFS order; popleft() on a
                #                     deque would be BFS. Order is irrelevant
                #                     here - a pure reachability question has no
                #                     shortest-path structure to preserve.
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    # Guard order is a correctness dependency, not style:
                    # bounds FIRST, because the height read below would
                    # IndexError (or silently wrap on a negative index).
                    if nr < 0 or nr >= m or nc < 0 or nc >= n:
                        continue
                    # REVERSED edge condition. Water flows neighbor -> current
                    # exactly when the neighbor is at least as high, so walking
                    # away from the ocean means walking uphill.
                    if heights[nr][nc] < heights[r][c]:
                        continue
                    if (nr, nc) in reachable:
                        continue
                    # Mark on PUSH, never on pop - the same register-on-
                    # discovery rule as LC 133. Marking at pop time here is
                    # not a correctness bug (as it was on 133), only stack
                    # inflation: a cell with k unvisited neighbours would be
                    # pushed k times. Remember the rule, not the severity.
                    reachable.add((nr, nc))
                    stack.append((nr, nc))
            return reachable

        # Pacific touches the top and left edges; Atlantic the bottom and right.
        # Each seed list is m + n - 1 cells: a full side, plus the other side
        # minus the corner they share. Counting them is the cheap check that
        # catches an off-by-one in the range bounds.
        pacific = flood(
            [(r, 0) for r in range(m)] + [(0, c) for c in range(1, n)]
        )
        atlantic = flood(
            [(r, n - 1) for r in range(m)] + [(m - 1, c) for c in range(n - 1)]
        )

        return [[r, c] for r, c in pacific & atlantic]


# ---------------------------------------------------------------------------
# What changed (submission -> active code above)
# ---------------------------------------------------------------------------
# 1. THE STRUCTURAL FIX: the two passes were byte-identical apart from the seed
#    list and the set name - about 30 duplicated lines. Extracted into a nested
#    `flood(starts)` helper. This is not only de-duplication; duplicated logic
#    is a correctness liability (a fix applied to one copy and not the other is
#    invisible), and the extraction is what NAMES the insight that the search
#    depends on nothing but its seeds.
# 2. `pacific_reachable.update((r, c) for r, c in stack)` -> `set(starts)`. The
#    generator unpacked each tuple and rebuilt it identically - a no-op
#    transformation. (Its ancestor was a real bug caught mid-implementation:
#    `.add(<genexpr>)` inserts the generator OBJECT as a single element. `add`
#    takes one element, `update` takes an iterable - the set analogue of
#    list.append vs list.extend.)
# 3. Dropped the two dead `... = set()` inits at the top; the helper returns the
#    set, so there is nothing to pre-declare.
# 4. Separated the two roles of the name `stack`. In the submission one list was
#    both the seed collection (read by `update`) and the working stack (consumed
#    by the loop). That worked only because the `update` happened to sit above
#    the `while`; move it one line down and the set is built from a drained
#    list. In the helper, seeds are a parameter and the stack a local.
# 5. Added type hints, including on the nested helper, plus the
#    `from typing import List, Set, Tuple` line that neetcode.io supplies
#    implicitly.
# 6. PEP 8 spacing throughout: `(r,0)` -> `(r, 0)`, `n-1` -> `n - 1`,
#    `[[r,c] for r,c in ...]` -> `[[r, c] for r, c in ...]`. Merged
#    `nr = r + dr` / `nc = c + dc` into one tuple assignment.
# 7. Added the guard-order, marking-instant, and seed-count comments.
# No logic changed.
#
# Complexity of the active code:
#   Time  O(m*n). Each ocean's search enters every cell at most once (the
#         `reachable` check makes the work disjoint across all m + n - 1 seeds),
#         and each entered cell does O(4) neighbour work. Two oceans and the
#         intersection are additive constants on top, and `pacific & atlantic`
#         is O(min(|pacific|, |atlantic|)) - CPython iterates the smaller set
#         and probes the larger. Total O(m*n).
#   Space O(m*n): the two sets, plus the stack, plus the returned list - all
#         O(m*n), all additive. The explicit stack replaces a recursion stack of
#         the same bound, so iterating buys no asymptotic space; it buys not
#         crashing at 10^4 deep.


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
#     def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
#         pacific_reachable = set()
#         atlantic_reachable = set()
#         m = len(heights) # number of rows
#         n = len(heights[0]) # number of columns
#
#         stack = [(r,0) for r in range(m)]
#         stack.extend([(0,c) for c in range(1, n)])
#
#         pacific_reachable.update((r, c) for r, c in stack)
#
#         while stack:
#             r, c = stack.pop()
#             for dr, dc in DIRECTIONS:
#                 nr = r + dr
#                 nc = c + dc
#                 if nr < 0 or nr >= m or nc < 0 or nc >= n:
#                     continue
#                 if heights[nr][nc] < heights[r][c]:
#                     continue
#                 if (nr, nc) in pacific_reachable:
#                     continue
#                 pacific_reachable.add((nr, nc))
#                 stack.append((nr, nc))
#
#         stack = [(r,n-1) for r in range(m)]
#         stack.extend([(m-1,c) for c in range(n-1)])
#
#         atlantic_reachable.update((r, c) for r, c in stack)
#
#         while stack:
#             r, c = stack.pop()
#             for dr, dc in DIRECTIONS:
#                 nr = r + dr
#                 nc = c + dc
#                 if nr < 0 or nr >= m or nc < 0 or nc >= n:
#                     continue
#                 if heights[nr][nc] < heights[r][c]:
#                     continue
#                 if (nr, nc) in atlantic_reachable:
#                     continue
#                 atlantic_reachable.add((nr, nc))
#                 stack.append((nr, nc))
#
#         return [[r,c] for r,c in pacific_reachable & atlantic_reachable]


# ---------------------------------------------------------------------------
# Alt 2: recursive DFS (the canonical reference form). O(m*n) time, O(m*n) space.
#
# Shorter, and it is what most published solutions show - but note what it costs
# to be recursive here. The helper must be told the height it CAME FROM, because
# there is no popped cell to read it off; the reference form threads a
# `prev_height` parameter and seeds each border call with that cell's own height
# (so the seed's guard is `>= itself`, trivially true). The iterative version
# needs no such payload: `heights[r][c]` of the popped cell IS the predecessor
# height.
#
# DO NOT SUBMIT THIS AT THE STATED BOUND without saying the limit out loud. On a
# 100x100 grid of equal heights the recursion reaches ~10^4 frames against
# CPython's default 1000. An accepted recursive submission here is accepted
# because the judge's tests are small, not because it is correct at the bound.
# VERIFIED, not assumed: this exact code raises RecursionError on a 100x100
# all-equal grid at the default limit, where the active iterative version
# returns all 10000 cells. Unlike LC 200 - where the same trap was real but
# only argued - here the witness was actually run.
# ---------------------------------------------------------------------------
# class Solution:
#     def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
#         m, n = len(heights), len(heights[0])
#         pacific: Set[Tuple[int, int]] = set()
#         atlantic: Set[Tuple[int, int]] = set()
#
#         def dfs(r: int, c: int, reachable: Set[Tuple[int, int]],
#                 prev_height: int) -> None:
#             if r < 0 or r >= m or c < 0 or c >= n:
#                 return
#             if (r, c) in reachable:
#                 return
#             if heights[r][c] < prev_height:
#                 return
#             reachable.add((r, c))
#             for dr, dc in DIRECTIONS:
#                 dfs(r + dr, c + dc, reachable, heights[r][c])
#
#         for c in range(n):
#             dfs(0, c, pacific, heights[0][c])
#             dfs(m - 1, c, atlantic, heights[m - 1][c])
#         for r in range(m):
#             dfs(r, 0, pacific, heights[r][0])
#             dfs(r, n - 1, atlantic, heights[r][n - 1])
#
#         return [[r, c] for r, c in pacific & atlantic]


# ---------------------------------------------------------------------------
# Alt 3: the rejected brute force - one search per cell.
#        O((m*n)^2) time, O(m*n) space.
#
# Kept because naming it and pricing it is the first move in the interview, and
# because the two things that kill it are both instructive. (a) The visited set
# has a PER-KICKOFF lifetime - it must be rebuilt for every start cell, which is
# the opposite of the reversed version's per-ocean lifetime, and it is why
# sinking values into the grid (the LC 200 trick) does not transfer: you would
# have to restore each cell on the way out, and the restore destroys the height
# data you overwrote unless you stash it. (b) At m, n <= 100 this is
# (10^4)^2 = 10^8 operations - not shippable in Python.
# ---------------------------------------------------------------------------
# class Solution:
#     def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
#         m, n = len(heights), len(heights[0])
#         result = []
#
#         for start_r in range(m):
#             for start_c in range(n):
#                 seen = set()            # rebuilt per start cell
#                 hits_pacific = False
#                 hits_atlantic = False
#                 stack = [(start_r, start_c)]
#                 seen.add((start_r, start_c))
#                 while stack:
#                     r, c = stack.pop()
#                     for dr, dc in DIRECTIONS:
#                         nr, nc = r + dr, c + dc
#                         if nr < 0 or nc < 0:          # fell off top/left
#                             hits_pacific = True
#                             continue
#                         if nr >= m or nc >= n:        # fell off bottom/right
#                             hits_atlantic = True
#                             continue
#                         if heights[nr][nc] > heights[r][c]:   # FORWARD walk:
#                             continue                          # downhill only
#                         if (nr, nc) in seen:
#                             continue
#                         seen.add((nr, nc))
#                         stack.append((nr, nc))
#                 if hits_pacific and hits_atlantic:
#                     result.append([start_r, start_c])
#
#         return result
