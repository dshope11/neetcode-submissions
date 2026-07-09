# Search in Rotated Sorted Array (LC 33) | Binary Search | Blind 75
# Solved 2026-07-08 on neetcode.io | outcome: solo
#   Reasoned the whole approach independently: the O(n) brute-force scan, then the
#   two-pass O(log n) plan - find the pivot exactly as in LC 153, then pick which
#   sorted run the target lives in (compare target to nums[-1], the max of the right
#   run) and run a plain inclusive binary search on that run. Correctly worked out
#   the equality boundary (target <= nums[-1] -> right run) and that n == 1 and the
#   non-rotated case both fall out of the general branches with no special case.
# Raw: Data Structures & Algorithms/find-target-in-rotated-sorted-array/submission-0.py
# Style: clean - snake_case, PascalCase class, no PEP 8 slips. search / nums are
#        LeetCode's fixed method signature. The one cosmetic slip in the typed
#        version was two different midpoint names (`mid` in the pivot loop,
#        `middle` in the search loop); unified to `mid` in the active code, visible
#        as-typed in Alt 1.
#
# THE PROBLEM: a sorted-ascending array of UNIQUE values, rotated by some amount.
# Return the INDEX of target, or -1 if absent, in O(log n). A plain binary search
# fails because the rotation breaks the "one comparison tells you which half" rule.
#
# THE TWO-PASS PLAN:
#   Pass 1 - find the pivot p (index of the minimum) with the LC 153 converging
#            search: compare nums[mid] to the RIGHT endpoint nums[hi]; nums[mid] <
#            nums[hi] -> hi = mid (keep mid), else lo = mid + 1. Stop at lo == hi;
#            p = lo. The pivot splits the array into two sorted runs, [0, p-1]
#            (high run) and [p, n-1] (low run, contains the minimum).
#   Pass 2 - pick the run, then binary-search it normally:
#            * target <= nums[-1]  -> the LOW run [p, n-1] (nums[-1] is its max, so
#                                     anything <= it can only be here). The `<=`
#                                     is load-bearing: target == nums[-1] belongs
#                                     to this run.
#            * else (target > nums[-1]) -> the HIGH run [0, p-1].
#            Then a standard inclusive `while lo <= hi` search returns the index or
#            -1. No special-casing needed: n == 1 -> pivot p = 0, a present target
#            routes into the low run and is found, an absent one routes into the
#            empty high run [0, -1] and returns -1; the non-rotated array is just
#            p = 0 with the whole array as the low run.
#
# SHARP POINT (the section's theme): this function uses TWO different interval
# conventions, correctly kept apart. Pass 1 is a CONVERGING boundary search
# (`while lo < hi`, hi = mid, no -1 sentinel because the minimum always exists);
# Pass 2 is a CLASSIC target search (`while lo <= hi`, hi = mid - 1, returns -1
# when absent). Mixing these two - e.g. `while lo <= hi` with `hi = mid` - is the
# canonical off-by-one of binary search. Holding each convention to its own loop
# is exactly what makes this correct.
#
# Complexity: O(log n) time - two sequential binary searches, log n + log n -> O(log n).
# O(1) space (no intermediate structures, iterative).

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo = 0
        hi = len(nums) - 1

        # Pass 1: find the pivot (index of the minimum) - LC 153.
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] < nums[hi]:
                hi = mid
            else:
                lo = mid + 1
        p = lo

        # Pass 2: pick the sorted run, then a plain inclusive binary search.
        if target <= nums[-1]:
            lo = p
            hi = len(nums) - 1
        else:
            lo = 0
            hi = p - 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] > target:
                hi = mid - 1
            else:
                lo = mid + 1

        return -1


# ---------------------------------------------------------------------------
# What changed from the typed submission (Alt 1) -> the active cleaned version
# ---------------------------------------------------------------------------
#   * Renamed the second loop's midpoint variable `middle` -> `mid` so both loops
#     use one consistent name. Cosmetic only; no logic change. Everything else
#     (branches, boundaries, `p = lo` naming) is identical to the typed version.
#
# ---------------------------------------------------------------------------
# Alternatives (commented; the active code above is the optimal)
# ---------------------------------------------------------------------------
#
# Alt 1) The accepted submission, VERBATIM as typed (the honest practice record).
#   Differs from the active code only in the `middle` vs `mid` name in the second
#   loop. O(log n) time, O(1) space.
#
# class Solution:
#     def search(self, nums: List[int], target: int) -> int:
#         lo = 0
#         hi = len(nums) - 1
#
#         while lo < hi:
#             mid = lo + (hi - lo) // 2
#             if nums[mid] < nums[hi]:
#                 hi = mid
#             else:
#                 lo = mid + 1
#         p = lo
#
#         if target <= nums[-1]:
#             lo = p
#             hi = len(nums) - 1
#         else:
#             lo = 0
#             hi = p - 1
#
#         while lo <= hi:
#             middle = lo + (hi - lo) // 2
#             if nums[middle] == target:
#                 return middle
#             if nums[middle] > target:
#                 hi = middle - 1
#             else:
#                 lo = middle + 1
#
#         return -1
#
# Alt 2) Brute force - the O(n) scan reasoned first in Phase 1. Ignore the sorted
#   structure entirely and linear-scan for target. Correct but fails the O(log n)
#   intent. O(n) time, O(1) space. (Python one-liner equivalent: `return
#   nums.index(target) if target in nums else -1`, also O(n).)
#
# class Solution:
#     def search(self, nums: List[int], target: int) -> int:
#         for i, x in enumerate(nums):
#             if x == target:
#                 return i
#         return -1
#
# Alt 3) One-pass single binary search - the interviewer follow-up ("can you avoid
#   the separate pivot pass?"). Fold the pivot logic into the search loop: at each
#   mid, first check for a hit; then decide WHICH HALF IS SORTED by comparing
#   nums[lo] to nums[mid]; then test whether target lies inside that sorted half's
#   value range - if so, search it, else search the other half. Same O(log n) time,
#   O(1) space, but a single pass (~half the comparisons). Trickier to get right
#   live because each branch nests a range test, which is why the two-pass version
#   is the cleaner thing to reach for first.
#
# class Solution:
#     def search(self, nums: List[int], target: int) -> int:
#         lo, hi = 0, len(nums) - 1
#         while lo <= hi:
#             mid = lo + (hi - lo) // 2
#             if nums[mid] == target:
#                 return mid
#             if nums[lo] <= nums[mid]:              # left half [lo, mid] is sorted
#                 if nums[lo] <= target < nums[mid]:
#                     hi = mid - 1
#                 else:
#                     lo = mid + 1
#             else:                                  # right half [mid, hi] is sorted
#                 if nums[mid] < target <= nums[hi]:
#                     lo = mid + 1
#                 else:
#                     hi = mid - 1
#         return -1
