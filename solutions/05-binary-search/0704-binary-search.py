# Binary Search (LC 704) | Binary Search | NeetCode 150 (not Blind)
# Solved 2026-07-06 on neetcode.io | outcome: solo (one self-caught bug)
#   Reasoned the O(n) brute force, the O(log n) halving, and the inclusive
#   [lo, hi] convention solo. In the interview discussion nearly shipped the
#   classic off-by-one - mixing hi = len - 1 (inclusive) with a stop-when-
#   lo == hi (half-open) condition, which skips the last single-element window;
#   corrected to `while lo <= hi` after a trace of nums = [5], target = 5.
#   During implementation hit and self-fixed the mid bug (see below).
# Raw: Data Structures & Algorithms/binary-search/submission-0.py
# Style: clean - snake_case, PascalCase class, no PEP 8 slips. search / nums /
#        target are LeetCode's fixed method signature.
#
# ACTIVE CODE BELOW is the CLEANED version (one agreed style-only improvement over
# the typed submission), per the /neetcode workflow. The verbatim accepted
# submission is preserved untouched as Alt 1 so the practice record stays honest.
# The algorithm is identical - the cleanup is purely surface.
#
# The canonical binary search, INCLUSIVE [lo, hi] convention: lo and hi both point
# at real indices, so hi = len - 1 and the loop runs while lo <= hi (when lo == hi
# there is still ONE element left to inspect). O(log n) time - each iteration
# discards half the remaining window; O(1) space (iterative, no call stack).
#
# The two conventions (pick one and hold it consistently - mixing them is THE
# off-by-one of this section):
#   * inclusive [lo, hi]:  hi = len - 1,  while lo <= hi,  lo = mid + 1 / hi = mid - 1
#   * half-open [lo, hi):  hi = len,      while lo <  hi,  lo = mid + 1 / hi = mid
#
# SIGNATURE BUG (self-caught during implementation): mid must be
#   mid = lo + (hi - lo) // 2
# The `lo +` is load-bearing. Without it, (hi - lo) // 2 is an OFFSET into the
# window, not an absolute index. With lo = 2, hi = 3 it gives 0 - a position
# BEHIND the current window - so a `>` branch sets lo = 1, moving lo backwards,
# the window never shrinks, and the loop spins forever. `lo +` re-anchors the
# offset to an absolute index. (The (hi - lo) form itself is the overflow-safe
# habit for C++/Java; in Python (lo + hi) // 2 is equally fine.)

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo = 0
        hi = len(nums) - 1

        while lo <= hi:
            middle = lo + (hi - lo) // 2
            if nums[middle] == target:
                return middle
            if nums[middle] > target:
                hi = middle - 1
            else:
                lo = middle + 1

        return -1


# ---------------------------------------------------------------------------
# What changed from the typed submission (Alt 1) -> the active cleaned version
# ---------------------------------------------------------------------------
#  1. Final branch `elif nums[middle] < target:` -> `else:`. After excluding
#     `==` and `>`, the `<` case is the only possibility left, so the explicit
#     comparison is redundant - `else` drops one comparison per iteration and
#     reads as "the three cases are exhaustive."
#  Same algorithm, same O(log n) / O(1).
#
# ---------------------------------------------------------------------------
# Alternatives (commented; the active code above is the cleaned optimal)
# ---------------------------------------------------------------------------
#
# Alt 1) The accepted submission, VERBATIM as typed (the honest practice record).
#   Same binary search, same O(log n) / O(1). Only difference vs the cleaned active
#   code is the redundant `elif` noted above.
#
# class Solution:
#     def search(self, nums: List[int], target: int) -> int:
#         lo = 0
#         hi = len(nums) - 1
#
#         while lo <= hi:
#             middle = lo + (hi - lo) // 2
#             if nums[middle] == target:
#                 return middle
#             if nums[middle] > target:
#                 hi = middle - 1
#             elif nums[middle] < target:
#                 lo = middle + 1
#
#         return -1
#
# Alt 2) Brute force - the naive O(n) reasoned first in Phase 1. Linear scan,
#   ignores the sortedness entirely. O(n) time, O(1) space. Correct but fails the
#   O(log n) requirement; the point of the problem is to USE the sorted order.
#
# class Solution:
#     def search(self, nums: List[int], target: int) -> int:
#         for i, x in enumerate(nums):
#             if x == target:
#                 return i
#         return -1
#
# Alt 3) bisect one-liner - Python's stdlib binary search. bisect_left returns the
#   leftmost insertion point; check that slot actually holds target. O(log n) / O(1).
#   Fair game when you just need the position; know the manual version for when the
#   interviewer bans the library.
#
# from bisect import bisect_left
#
# class Solution:
#     def search(self, nums: List[int], target: int) -> int:
#         i = bisect_left(nums, target)
#         return i if i < len(nums) and nums[i] == target else -1
