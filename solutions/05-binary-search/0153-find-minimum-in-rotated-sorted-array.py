# Find Minimum in Rotated Sorted Array (LC 153) | Binary Search | Blind 75
# Solved 2026-07-07 on neetcode.io | outcome: solo
#   Reasoned the whole approach independently: the O(n) pivot-scan brute force,
#   the O(log n) binary search, the choice of nums[hi] as the safe reference
#   (nums[lo] lies on a non-rotated array - nums[mid] > nums[lo] is ALWAYS true
#   there, so it would always send you right and walk off the real minimum), the
#   [lo, hi] / `while lo < hi` / `hi = mid` convention, and the duplicates
#   follow-up (LC 154). Only correction was a post-hoc trace mislabel (which
#   branch fires on [1,2,3]); the algorithm itself was all his.
# Raw: Data Structures & Algorithms/find-minimum-in-rotated-sorted-array/submission-0.py
# Style: clean - snake_case, PascalCase class, no PEP 8 slips. findMin / nums
#        are LeetCode's fixed method signature.
#
# ACTIVE CODE BELOW is the accepted submission unchanged - the review found nothing
# to clean up (algorithm and style already at the curated bar), so the active code
# and the verbatim Alt 1 are identical this time. Alt 1 is kept anyway to preserve
# the standard practice-record shape.
#
# THE PROBLEM: a sorted-ascending array of UNIQUE values, rotated by some amount.
# The minimum is the "pivot" - the single point where the order drops from big to
# small. It splits the array into two sorted runs where EVERY element of the left
# run is greater than every element of the right run. Find that minimum in O(log n).
#
# THE DECISION RULE (one comparison, mid vs the RIGHT endpoint):
#   * nums[mid] < nums[hi]  -> mid is in the same sorted run as hi, so the pivot is
#                              at mid or to its LEFT  -> hi = mid   (keep mid: it
#                              could itself be the minimum, so NOT mid - 1)
#   * else (nums[mid] > nums[hi]) -> mid is stranded in the left/high run, the pivot
#                              is strictly to the RIGHT -> lo = mid + 1 (mid is
#                              bigger than hi, so it can never be the minimum)
#   Loop `while lo < hi`; when lo == hi one element remains - that's the answer.
#   Return nums[lo].
#
# WHY nums[hi] AND NOT nums[lo]: nums[hi] never lies because the minimum is always
# at or before hi in this framing. nums[lo] fails on a NON-rotated array: there
# nums[mid] > nums[lo] is always true, which would always send you right and skip
# the real minimum sitting at lo.
#
# CONVENTION NOTE (the theme of this whole section): this uses `hi = mid` (mid NOT
# excluded), so the loop MUST be `while lo < hi`. Writing `while lo <= hi` here
# (muscle memory from LC 704's inclusive convention) spins forever, because
# hi = mid does not shrink the window when lo == hi. State the interval convention
# up front and hold it - mixing conventions is the off-by-one of binary search.
#
# UNIQUENESS DEPENDENCY (sharp point): the submission's `else` fires on
# nums[mid] >= nums[hi], while the discussion framed the split as `< / <=`. Those
# are IDENTICAL here only because elements are unique AND mid < hi always holds
# in-loop ((hi - lo) // 2 < hi - lo), so nums[mid] == nums[hi] can never occur.
# The == case only matters with DUPLICATES (LC 154), where the fix is `hi -= 1`
# on a tie - which loses the guaranteed halving and degrades the worst case to O(n).
#
# Complexity: O(log n) time (each iteration discards half the window), O(1) space.

class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo = 0
        hi = len(nums) - 1

        while lo < hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] < nums[hi]:
                hi = mid
            else:
                lo = mid + 1
        return nums[lo]


# ---------------------------------------------------------------------------
# What changed from the typed submission (Alt 1) -> the active cleaned version
# ---------------------------------------------------------------------------
#   Nothing. The accepted submission was already clean in both algorithm and
#   style, so the active code is byte-for-byte the typed version. Alt 1 below is
#   identical and kept only to preserve the standard file shape.
#
# ---------------------------------------------------------------------------
# Alternatives (commented; the active code above is the optimal)
# ---------------------------------------------------------------------------
#
# Alt 1) The accepted submission, VERBATIM as typed (the honest practice record).
#   Identical to the active code above this cycle. O(log n) time, O(1) space.
#
# class Solution:
#     def findMin(self, nums: List[int]) -> int:
#         lo = 0
#         hi = len(nums) - 1
#
#         while lo < hi:
#             mid = lo + (hi - lo) // 2
#             if nums[mid] < nums[hi]:
#                 hi = mid
#             else:
#                 lo = mid + 1
#         return nums[lo]
#
# Alt 2) Brute force - the pivot scan reasoned first in Phase 1. Walk left to
#   right; the first element smaller than its predecessor is the minimum. If none
#   is found the array was never rotated, so the minimum is nums[0]. Ignores the
#   sorted structure and so stays O(n) time, O(1) space - correct but fails the
#   O(log n) intent of the problem. (The truly naive form is just `min(nums)`,
#   also O(n) - see Alt 3.)
#
# class Solution:
#     def findMin(self, nums: List[int]) -> int:
#         for i in range(1, len(nums)):
#             if nums[i] < nums[i - 1]:
#                 return nums[i]
#         return nums[0]
#
# Alt 3) The one-liner - Python's built-in min(). O(n) time, O(1) space. The
#   honest baseline: if O(log n) were not required, this is the whole solution.
#   State it so the interviewer knows you see it, then reach for binary search.
#
# class Solution:
#     def findMin(self, nums: List[int]) -> int:
#         return min(nums)
