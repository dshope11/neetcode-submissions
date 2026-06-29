# 3Sum (LC 15) | Two Pointers | Blind 75
# Solved 2026-06-28 on neetcode.io | outcome: hint (debugged the dedup corner
#   cases via counterexamples - structure was solo, the duplicate handling needed
#   nudges)
# Raw: Data Structures & Algorithms/three-integer-sum/submission-2.py
# Style notes (active code preserved verbatim, not rewritten):
#   - `target = - nums[i]`: conventional is `-nums[i]` (no space after unary minus).
#   - `nums[i-1]` / `nums[left-1]`: PEP 8 wants spaces (`i - 1`, `left - 1`).
#   (threeSum is LeetCode's fixed method signature; `s` correctly avoids shadowing
#   the built-in sum().)
#
# Optimal active below: sort + "Two Sum II inside a loop", O(n^2) time / O(n) space.
#
# Key idea: SORT, then for each anchor nums[i] run a converging two-pointer over
# the suffix looking for a pair summing to -nums[i] (so all three total 0). The
# sort is the lever that makes both the two-pointer scan AND the dedup possible.
#
# The whole difficulty is UNIQUE triplets (the output must not repeat a triplet by
# value). Three dedup/early-exit pieces, and the two corner cases that bit during
# the solve:
#
#   1. Skip duplicate ANCHORS: `if i > 0 and nums[i] == nums[i-1]: continue`.
#      Don't start a new triplet on an anchor value already used.
#
#   2. `break` (not continue) once nums[i] > 0: array is sorted, so nums[left] and
#      nums[right] are both >= nums[i] > 0 -> sum is strictly positive, can never
#      hit 0. Nothing left anywhere, so stop entirely.
#
#   3. Skip duplicate LEFT values AFTER recording a match. Two bugs lived here:
#      - BUG A (dedup in the wrong place): skipping `left` BEFORE testing the pair
#        drops valid triplets whose two smaller values are equal. On [-1,-1,2] a
#        top-of-loop `nums[left]==nums[left-1]` skip compares the first left
#        against the anchor and skips it, losing [-1,-1,2] entirely. The skip must
#        come AFTER an append, not before a test.
#      - BUG B (single if vs while + missing bounds guard): one `if` skips only ONE
#        duplicate; a run of 3+ equal values (e.g. [-2,0,0,0,2]) re-emits the
#        triplet. Needs a `while` - and that while needs `left < right` as its
#        FIRST condition so short-circuit eval stops before `nums[left]` indexes
#        off the end (the out-of-range crash).
#      Deduping LEFT alone is sufficient: for a fixed left value there is exactly
#      one right that completes the sum, so right needs no separate skip (and no
#      decrement after a match - the next iteration re-derives it).
#
# Complexity: outer O(n) x inner two-pointer O(n) = O(n^2) time; sort is
# O(n log n), dominated. Space O(n) for Timsort (O(1) extra beyond the sort+output).

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []

        nums.sort()

        for i in range(len(nums)):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i-1]:
                continue

            left = i + 1
            right = len(nums) - 1

            target = - nums[i]
            while left < right:
                s = nums[left] + nums[right]
                if s < target:
                    left += 1
                elif s > target:
                    right -= 1
                else:
                    res.append([nums[i], nums[left], nums[right]])
                    left += 1
                    while left < right and nums[left] == nums[left-1]:
                        left += 1

        return res

# Alternative - brute force, three nested loops over increasing index ranges:
# O(n^3) time, O(n) space (for the dedup set). Build each triplet, sort it, and
# stash in a set to dedup. The baseline before the sort+two-pointer trade.
# def threeSum(self, nums):
#     n, seen = len(nums), set()
#     for i in range(n):
#         for j in range(i + 1, n):
#             for k in range(j + 1, n):
#                 if nums[i] + nums[j] + nums[k] == 0:
#                     seen.add(tuple(sorted((nums[i], nums[j], nums[k]))))
#     return [list(t) for t in seen]
#
# Alternative - sort + hash set for the inner two-sum: O(n^2) time, O(n) space.
# Same outer anchor loop, but instead of two pointers the inner pass walks j and
# looks for the complement (-nums[i] - nums[j]) in a running set. Same big-O as the
# two-pointer version but uses O(n) extra per anchor and the dedup is fiddlier -
# the two-pointer form above is the cleaner canonical answer.
# def threeSum(self, nums):
#     nums.sort()
#     res = []
#     for i in range(len(nums)):
#         if nums[i] > 0:
#             break
#         if i > 0 and nums[i] == nums[i-1]:
#             continue
#         seen = set()
#         j = i + 1
#         while j < len(nums):
#             complement = -nums[i] - nums[j]
#             if complement in seen:
#                 res.append([nums[i], complement, nums[j]])
#                 while j + 1 < len(nums) and nums[j] == nums[j+1]:
#                     j += 1
#             seen.add(nums[j])
#             j += 1
#     return res
