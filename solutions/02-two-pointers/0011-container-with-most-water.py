# Container With Most Water (LC 11) | Two Pointers | Blind 75
# Solved 2026-06-30 on neetcode.io | outcome: hint (move rule + loop solo; the
#   "why moving the taller wall is provably useless" correctness argument came via
#   Socratic nudges)
# Raw: Data Structures & Algorithms/max-water-container/submission-0.py
# Style: clean (snake_case, no shadowing, no Unicode, PEP 8). maxArea is
#        LeetCode's fixed method signature.
#
# Optimal active below: converging two pointers, O(n) time / O(1) space.
#
# Key idea: area = (right - left) * min(h[left], h[right]) - it depends on BOTH
# the width (the index distance) AND the height. That is why you must NOT sort:
# sorting destroys the indices, which ARE the width. Start at the WIDEST base
# (left=0, right=n-1) so the first area uses the max possible width, then converge.
#
# The move rule and its proof (the crux): always move the SHORTER wall inward.
# Why moving the taller wall is provably useless - say h[left] < h[right]. Of ALL
# containers that use the left (shorter) wall, the current (left, right) is already
# the best:
#   - width is maximal right now (right is as far as it can be), and
#   - height is capped at h[left] no matter how tall a partner you find, since the
#     shorter wall limits it.
# So the left wall can never beat what it just scored -> discard it (left += 1).
# Keep the taller wall; it may still pair well with a future wall. (A taller wall
# found by moving right instead would still be capped by h[left] and be narrower,
# so it cannot improve on the current area for THIS shorter wall.)
#
# Tie (h[left] == h[right]): move either - both walls are equally maxed out.
# Moving just one (as below) is sufficient; you don't need to move both.
#
# Loop `while left < right` (at left == right the width is 0). Carry a running
# max_area, updated before each move. O(n): each step retires one pointer, so
# combined travel is bounded by n. O(1) space.

class Solution:
    def maxArea(self, heights: List[int]) -> int:
        left = 0
        right = len(heights) - 1

        max_area = 0

        while left < right:
            area = (right - left) * min(heights[left], heights[right])
            max_area = max(max_area, area)

            if heights[left] < heights[right]:
                left += 1
            elif heights[left] > heights[right]:
                right -= 1
            else:
                left += 1

        return max_area

# Variant - fold the tie into the "move left" branch (same O(n)/O(1), 2 branches
# instead of 3): the tie and the h[left] < h[right] case both advance left.
# while left < right:
#     area = (right - left) * min(heights[left], heights[right])
#     max_area = max(max_area, area)
#     if heights[left] <= heights[right]:
#         left += 1
#     else:
#         right -= 1
#
# Alternative - brute force, check every pair: O(n^2) time, O(1) space. The
# baseline; the two-pointer move rule is what collapses it to O(n).
# def maxArea(self, heights):
#     n, best = len(heights), 0
#     for i in range(n):
#         for j in range(i + 1, n):
#             best = max(best, (j - i) * min(heights[i], heights[j]))
#     return best
