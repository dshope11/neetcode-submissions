# Two Sum II - Input Array Is Sorted (LC 167) | Two Pointers | NeetCode 150
# Solved 2026-06-28 on neetcode.io | outcome: solo
# Raw: Data Structures & Algorithms/two-integer-sum-ii/submission-0.py
# Style notes (active code preserved verbatim, not rewritten):
#   - `sum` shadows the Python built-in sum(); conventional name is `s` or `total`.
#   - `left+1` / `right+1`: PEP 8 wants spaces around the operator (`left + 1`).
#   (twoSum is LeetCode's fixed method signature, not a naming choice.)
#
# Optimal active below: converging two pointers, O(n) time / O(1) space.
#
# Key idea: the array is SORTED - that's the whole lever (vs. LC 1, unsorted,
# which needs a hash map). Start the pointers at OPPOSITE ends: left at 0, right
# at len-1. Starting at opposite ends is what kills the "which pointer do I move?"
# ambiguity - from there each move changes the sum monotonically in exactly one
# direction:
#   - sum < target -> only moving `left` up can grow the sum  -> left += 1
#   - sum > target -> only moving `right` down can shrink it  -> right -= 1
#   - sum == target -> found it.
#
# Why each move is safe: when sum < target and you increment left, you eliminate
# the ENTIRE current left index - because `right` is currently its largest
# possible partner, so if even that pair is too small, every smaller partner is
# too small too. Symmetric argument for retreating right.
#
# Why O(n) not O(n^2): the pointers only ever move toward each other, so combined
# travel is bounded by n - each index visited at most once. O(1) space: pure index
# arithmetic, no auxiliary structure.
#
# Return is 1-INDEXED (per the problem) -> [left + 1, right + 1]. Classic dropped
# point on this problem.
#
# Assumption the missing fallthrough leans on: the problem GUARANTEES exactly one
# solution, so the loop always hits `return` before the pointers meet. If no
# solution were guaranteed, you'd fall out of `while left < right` and need a
# trailing `return []`. (Array length >= 2 guaranteed, so no empty-input case.)

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            sum = numbers[left] + numbers[right]
            if sum < target:
                left += 1
            elif sum > target:
                right -= 1
            else:
                return [left+1, right+1]

# Alternative - brute force, check every pair: O(n^2) time, O(1) space. The
# baseline before using the sorted property; ignores that the array is sorted, so
# it does redundant work the converging pointers skip.
# def twoSum(self, numbers, target):
#     n = len(numbers)
#     for i in range(n):
#         for j in range(i + 1, n):
#             if numbers[i] + numbers[j] == target:
#                 return [i + 1, j + 1]
#
# Alternative - binary search for the complement: O(n log n) time, O(1) space.
# For each i, binary-search target - numbers[i] in numbers[i+1:]. Uses the sorted
# property but only halfway - still beaten by the O(n) two-pointer scan above.
# def twoSum(self, numbers, target):
#     import bisect
#     for i in range(len(numbers)):
#         need = target - numbers[i]
#         j = bisect.bisect_left(numbers, need, i + 1)
#         if j < len(numbers) and numbers[j] == need:
#             return [i + 1, j + 1]
