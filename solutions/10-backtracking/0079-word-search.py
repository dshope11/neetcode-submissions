"""
Word Search - LeetCode 79 (Medium)
Pattern: Backtracking (NeetCode section 10) - GRID backtracking: the accumulator is the
         BOARD ITSELF, and the return value is a bool that must propagate up and
         short-circuit. First problem in the section that does not enumerate.
List: Blind 75
Solved 2026-08-28 | outcome: solo (design greenlit before coding; three submissions,
                    both failures self-diagnosed, one off-by-one fixed one axis at a time)

Raw: Data Structures & Algorithms/search-for-word/submission-2.py

The ACTIVE code below is the CLEANED version - see "What changed" for every difference
from the accepted submission. David's verbatim accepted submission is preserved as Alt 1.

Style notes on the submission: the nested dfs had no parameter annotations (return type
only); wordIdx was camelCase; an `exists` variable held state that could only ever be
False by the time it was returned; the direction deltas were named dx/dy and every
direction comment was wrong. All fixed in the active code, all visible in Alt 1.
neetcode.io pre-imports the typing names, so the submission omits `from typing import
List`; the curated file carries it so the file is honest standalone.
"""

from collections import Counter
from typing import List

# (dr, dc) = (row delta, column delta). Deliberately NOT (dx, dy) - see the
# "Why dr/dc and not dx/dy" note below. The labels here are correct BECAUSE the
# first component moves the row.
DIRECTIONS = [
    (-1, 0),  # up
    (0, 1),   # right
    (1, 0),   # down
    (0, -1),  # left
]


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m = len(board)
        n = len(board[0])

        # Cheap bail 1: the word cannot be longer than the number of cells, since
        # no cell may be reused on a path. O(1).
        if len(word) > m * n:
            return False

        # Cheap bail 2: the board must contain every character of the word in at
        # least the needed multiplicity. One O(m*n) pass; prunes hard on the
        # adversarial "board of all A, word contains a B" shape, which otherwise
        # walks the whole 3^L tree from every cell. Counter subtraction drops
        # zero and negative counts, so the result is empty exactly when covered.
        if Counter(word) - Counter(ch for row in board for ch in row):
            return False

        def dfs(r: int, c: int, word_idx: int) -> bool:
            # A frame is entered ON the cell it must match, so word_idx is always
            # a valid index into word. (The other consistent convention - enter
            # AFTER the match, word_idx meaning "how many matched so far" - lets
            # word_idx legally reach len(word) and must be checked before any
            # board access. Pick one; mixing them is an off-by-one factory.)
            if r < 0 or r >= m or c < 0 or c >= n:
                return False
            if board[r][c] == "#":                 # on the current path already
                return False
            if board[r][c] != word[word_idx]:
                return False
            if word_idx == len(word) - 1:          # matched the last character
                return True                        # note: BEFORE the mark, so the
                                                   # final cell is never written

            saved = board[r][c]
            board[r][c] = "#"                      # choose

            found = False
            for dr, dc in DIRECTIONS:              # explore
                if dfs(r + dr, c + dc, word_idx + 1):
                    found = True
                    break                          # short-circuit, but do NOT return

            board[r][c] = saved                    # un-choose, on BOTH paths
            return found

        for r in range(m):
            for c in range(n):
                # The word[0] guard is redundant with the char check inside dfs,
                # but it skips a function call for every non-matching cell, which
                # is most of them. Kept deliberately. (Safe only because the
                # constraints guarantee len(word) >= 1.)
                if board[r][c] == word[0] and dfs(r, c, 0):
                    return True
        return False


# ---------------------------------------------------------------------------
# What changed from the accepted submission
# ---------------------------------------------------------------------------
# 1. THE RESTORE LEAK - the only correctness change. The submission had
#
#        for dx, dy in DIRECTIONS:
#            if dfs(i + dx, j + dy, wordIdx + 1):
#                return True          # <-- skips board[i][j] = c_tmp
#        board[i][j] = c_tmp
#        return False
#
#    The FAILURE path restores correctly; the SUCCESS path does not. When the
#    word is found, every frame on the winning path returns True at that line
#    and skips its own restore, so the caller gets a board with the entire
#    matched path - O(L) cells - overwritten by "#".
#
#    Demonstrated, not asserted - Alt 1 on the canonical example, board
#    printed after exist returns True for "ABCCED":
#
#        ['#', '#', '#', 'E']     path: A(0,0) B(0,1) C(0,2) C(1,2) E(2,2) D(2,1)
#        ['S', 'F', '#', 'S']     five of six matched cells left as "#"
#        ['A', 'D', '#', 'E']     the D survives - the success check fires
#                                 BEFORE the mark, so the last cell is never
#                                 written in the first place
#
#    It passes the judge because exist returns immediately and nothing reads
#    the board afterward. That makes it unobservable here, not correct: the
#    function mutates an input it does not own. Fixed with `found = True;
#    break`, which gives the frame ONE exit point after the mark, so the
#    unmark is structurally unskippable. That single-exit shape is the durable
#    takeaway - it is what makes the invariant hold by construction instead of
#    by remembering.
#
#    (try/finally around the loop is the other correct fix, and reads well if
#    there are several early returns. With one, the flag is cheaper.)
#
# 2. dx, dy -> dr, dc, and the direction comments corrected. See the note below.
#
# 3. Dropped the `exists` variable. It was initialized False, assigned inside
#    the loop, and returned at the end - but the function returns True the
#    moment dfs succeeds, so the trailing `return exists` could only ever
#    return False. Dead state. `if ...: return True` / `return False` says the
#    same thing with no variable to keep in sync.
#
# 4. wordIdx -> word_idx (snake_case).
#
# 5. Full type hints on the nested dfs: (r: int, c: int, word_idx: int) -> bool.
#    The submission annotated the return only.
#
# 6. dfs now closes over m and n instead of recomputing len(board) and
#    len(board[0]) on every frame. Not just a micro-optimization - it is the
#    structural fix for the bug that cost two submissions. See below.
#
# 7. Counter(c for c in word) -> Counter(word). Counter already consumes any
#    iterable, and a string is one.
#
# 8. The explicit three-line count comparison
#
#        for c in count_word:
#            if count_board[c] < count_word[c]:
#                return False
#
#    collapses to `if Counter(word) - count_board: return False`. Counter
#    subtraction discards non-positive counts, so a non-empty difference means
#    exactly "some character is short." (Counter(word) <= count_board is the
#    same test and reads better, but it is Python 3.10+; the subtraction form
#    is portable.)
#
# 9. Added `from typing import List` and the Counter import at module scope.
#
#
# ---------------------------------------------------------------------------
# The two failed submissions: one off-by-one, two crash sites
# ---------------------------------------------------------------------------
# Both failures came from a single guard:
#
#     if i < 0 or i > len(board) or j < 0 or j > len(board[i]):
#
# SUBMISSION 1 crashed INSIDE THE GUARD ITSELF, at len(board[i]).
# Trace it with i == len(board) (you stepped off the bottom edge):
#
#     i < 0            -> False
#     i > len(board)   -> False    equal is not greater: the guard PASSES the
#                                  exact case it exists to reject
#     j < 0            -> False
#     len(board[i])    -> IndexError
#
# So the bounds check did not fail to stop the bad index - the bounds check WAS
# the bad index.
#
# There are two independent defects stacked there, and separating them matters:
#
#   (a) `>` instead of `>=`. Off by one on both axes.
#
#   (b) `len(board[i])` reads the row that has not been validated yet. Even
#       with `>=` correct, that clause is safe only BECAUSE `or` short-circuits
#       left to right and an earlier clause already rejected bad i. The guard's
#       safety is load-bearing on clause ORDER - reorder it for readability
#       someday and it crashes again.
#
#       General rule, and the reusable one: NEVER INDEX WITH A COORDINATE
#       INSIDE THE GUARD THAT VALIDATES IT. Hoist the dimensions out first.
#       Closing over m and n (change 6) removes the dependency entirely: there
#       is no board access anywhere in the guard.
#
# SUBMISSION 2 fixed the row half and left the column half, so the crash moved
# from the guard (line 24) to the first board access past it (line 26,
# board[i][j]) with j == len(board[i]). The traceback MOVING looks like
# progress and is not - it is the identical off-by-one on the other axis. When
# a fix relocates an exception by one line, check whether the bug was
# symmetric before assuming the fix was partial-but-directionally-right.
#
#
# ---------------------------------------------------------------------------
# Why dr/dc and not dx/dy
# ---------------------------------------------------------------------------
# The submission had (0, -1) labelled "up" and added the first component to the
# ROW index - so (0, -1) actually moved LEFT. Every one of the four labels was
# wrong, and the code was still correct.
#
# It survives because {(0,-1), (1,0), (0,1), (-1,0)} is CLOSED UNDER
# TRANSPOSITION: swap the two components of every element and you get the same
# set back. Transposing the axes therefore permutes the four moves among
# themselves. All four neighbors get visited; only the visit ORDER changes, and
# order is irrelevant to an existence query. The 8-neighborhood is closed too,
# so the same mislabeling survives there as well - which is precisely why the
# habit is dangerous: the common direction sets hide it.
#
# The root cause is the NAMES. dx/dy imports a Cartesian frame where y is
# vertical and conventionally points UP, onto an index space whose first axis
# is a row that grows DOWN. Two mismatches (which axis, which sign) that cancel
# often enough to go unnoticed. dr/dc names the actual thing being incremented
# and makes the error unwriteable.
#
# Where the latent bug detonates: any direction set that is NOT
# transposition-symmetric. "You may only move right or down" - {(0,1), (1,0)}
# is symmetric as a set, but the moment the two directions are treated
# ASYMMETRICALLY (different costs, different legality, a diagonal-only move, a
# direction returned as part of the answer) the mislabeling becomes a wrong
# answer rather than a reordering. Also anywhere the label is consumed: "return
# the direction the word runs in," path reconstruction, printing a trace.
#
#
# ---------------------------------------------------------------------------
# Complexity
# ---------------------------------------------------------------------------
# Let m x n be the board, L = len(word), k = m * n cells.
#
# Depth              L            the base case word_idx == len(word) - 1
# Branching factor   3            the DIRECTIONS loop runs 4 times, but at any
#                                 non-root node one of the four steps walks back
#                                 onto the cell just marked "#" and is rejected
#                                 immediately. 4 is the loop count; 3 is the
#                                 live branching factor.
# Start cells        k            the outer double loop
#
#     Time   O(k * 3^L)   tighter form. O(k * 4^L) is also defensible - it is
#                         the loop count rather than the live fan-out. Know
#                         which one you are quoting and why; "4 because there
#                         are four calls" without the walk-back argument is the
#                         answer that gets followed up on.
#     Prefilter O(k)      one pass, dominated by the search.
#     Aux    O(L)         recursion stack only. The sentinel buys away the
#                         O(k) visited grid - see Alt 2 for the version that
#                         does not, and why you might want it.
#
# The walk-back branch is NOT special-cased in code. It is rejected by the
# ordinary "#" check, which is worth saying out loud: the visited test is doing
# double duty - preventing cell REUSE on a path, and pruning the immediate
# backtrack. One mechanism, two jobs.
#
#
# ===========================================================================
# Alt 1 - David's accepted submission, VERBATIM. O(k * 3^L) time, O(L) aux.
# ===========================================================================
# Correct on the judge. Leaks the "#" sentinel on the success path (change 1),
# and every direction label is wrong while the code still works (see above).
#
# from collections import Counter
#
# DIRECTIONS = [
#     (0, -1),  # up
#     (1, 0),   # right
#     (0, 1),   # down
#     (-1, 0),  # left
# ]
#
# class Solution:
#     def exist(self, board: List[List[str]], word: str) -> bool:
#         exists = False
#         m = len(board)
#         n = len(board[0])
#         if len(word) > m * n:
#             return False
#         count_board = Counter(c for row in board for c in row)
#         count_word = Counter(c for c in word)
#         for c in count_word:
#             if count_board[c] < count_word[c]:
#                 return False
#
#         def dfs(i, j, wordIdx) -> bool:
#             if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]):
#                 return False
#             if board[i][j] == "#":
#                 return False
#             if word[wordIdx] != board[i][j]:
#                 return False
#             if wordIdx == len(word) - 1:
#                 return True
#             c_tmp = board[i][j]
#             board[i][j] = "#"
#             for dx, dy in DIRECTIONS:
#                 if dfs(i + dx, j + dy, wordIdx + 1):
#                     return True
#             board[i][j] = c_tmp
#             return False
#
#         for i in range(len(board)):
#             for j in range(len(board[i])):
#                 if board[i][j] == word[0]:
#                     exists = dfs(i, j, 0)
#                     if exists:
#                         return exists
#         return exists
#
#
# ===========================================================================
# Alt 2 - separate visited grid: O(k * 3^L) time, O(k + L) aux, INPUT UNTOUCHED
# ===========================================================================
# The version to reach for when the interviewer says "don't mutate my input" -
# a completely reasonable constraint if the board is shared, read concurrently,
# or the caller needs it afterward. It is also the only option when the board
# holds values with no spare sentinel (arbitrary ints rather than letters), so
# know both: the in-place trick is not always available.
#
# Trade: you give up O(1) auxiliary space for O(m*n), and gain purity. Same
# tree, same asymptotic time - a bool grid read is as cheap as a char compare.
#
# class Solution:
#     def exist(self, board: List[List[str]], word: str) -> bool:
#         m = len(board)
#         n = len(board[0])
#         if len(word) > m * n:
#             return False
#         if Counter(word) - Counter(ch for row in board for ch in row):
#             return False
#
#         seen = [[False] * n for _ in range(m)]     # NOT [[False] * n] * m
#
#         def dfs(r: int, c: int, word_idx: int) -> bool:
#             if r < 0 or r >= m or c < 0 or c >= n:
#                 return False
#             if seen[r][c]:
#                 return False
#             if board[r][c] != word[word_idx]:
#                 return False
#             if word_idx == len(word) - 1:
#                 return True
#
#             seen[r][c] = True
#             found = False
#             for dr, dc in DIRECTIONS:
#                 if dfs(r + dr, c + dc, word_idx + 1):
#                     found = True
#                     break
#             seen[r][c] = False
#             return found
#
#         for r in range(m):
#             for c in range(n):
#                 if board[r][c] == word[0] and dfs(r, c, 0):
#                     return True
#         return False
#
# The grid construction is a classic trap: [[False] * n] * m builds m
# REFERENCES to one row, so seen[0][0] = True sets it in every row. The
# comprehension builds m distinct lists.
#
#
# ===========================================================================
# Alt 3 - dfs hoisted to a class method (stateless). Same complexity as active.
# ===========================================================================
# Not better for an interview - included because "why is the helper nested?" is
# a real design question, and the answer is not just style.
#
# The nested dfs is a CLOSURE: board, word, m, n are free for the taking. Hoist
# it and they have to travel. Passing them explicitly keeps the method pure -
# no instance state, safe to call repeatedly, and _dfs is testable on its own -
# at the cost of a five-argument signature repeated at every recursive call
# site, and the loss of the cached m/n (hence len(board) inside the frame,
# which is exactly the coupling change 6 removed).
#
# class Solution:
#     def exist(self, board: List[List[str]], word: str) -> bool:
#         m = len(board)
#         n = len(board[0])
#         if len(word) > m * n:
#             return False
#         if Counter(word) - Counter(ch for row in board for ch in row):
#             return False
#
#         for r in range(m):
#             for c in range(n):
#                 if board[r][c] == word[0] and self._dfs(board, word, r, c, 0):
#                     return True
#         return False
#
#     def _dfs(
#         self, board: List[List[str]], word: str, r: int, c: int, word_idx: int
#     ) -> bool:
#         if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]):
#             return False
#         if board[r][c] == "#":
#             return False
#         if board[r][c] != word[word_idx]:
#             return False
#         if word_idx == len(word) - 1:
#             return True
#
#         saved = board[r][c]
#         board[r][c] = "#"
#         found = False
#         for dr, dc in DIRECTIONS:
#             if self._dfs(board, word, r + dr, c + dc, word_idx + 1):
#                 found = True
#                 break
#         board[r][c] = saved
#         return found
#
# The other hoisting option - stashing self.board / self.word / self.rows /
# self.cols in exist and reading them in _dfs - keeps the recursive signature
# short, which is why it is common on LeetCode. Three costs worth naming:
# Solution carries mutable state between calls; the attributes are created
# outside __init__, so _dfs raises AttributeError if called first and linters
# flag it; and every self.board is an instance-dict lookup where a closure
# variable is a direct cell load, in a frame that runs 3^L times.
#
# Keep the nested form for interviews: it is the only one that gets BOTH the
# short signature and no instance state. Hoist when the helper needs to be
# unit-tested or shared across methods - a production concern, not an
# interview one.
