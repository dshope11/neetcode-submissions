"""
K Closest Points to Origin - LeetCode 973 (Medium)
Pattern: Heap / Priority Queue (NeetCode section 9) - heap keyed by a COMPUTED score
List: NeetCode 150 (not Blind 75)
Solved 2026-08-22 | outcome: solo (with recall - the 3-tuple heap entry came from
                   Merge K Sorted Lists / LC 23, met earlier in section 6)

Raw: Data Structures & Algorithms/k-closest-points-to-origin/submission-0.py

The ACTIVE code below is the CLEANED version, not the verbatim submission.
David's accepted submission is preserved verbatim as Alt 1.

Style notes on the submission (fixed in the active code, visible in Alt 1):
  - `math.sqrt` used without `import math`, and `List` used without importing it.
    neetcode.io injects both, so the file ran there but would NameError standalone.
  - `result = []` initialized above the loop that does not use it.
  - `for i in range(k)` reuses `i` as a throwaway; `_` states the intent.
"""

from typing import List, Tuple
import heapq


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Squared distance is enough: sqrt is strictly increasing, so it preserves
        # order, and the ordering is the only thing the distance is used for.
        heap: List[Tuple[int, int, int]] = [(x * x + y * y, x, y) for x, y in points]
        heapq.heapify(heap)                      # O(n), not O(n log n)

        result: List[List[int]] = []
        for _ in range(k):
            _, x, y = heapq.heappop(heap)        # O(log n) each
            result.append([x, y])
        return result


# ---------------------------------------------------------------------------
# What changed from the accepted submission
# ---------------------------------------------------------------------------
# 1. DROPPED `math.sqrt`. It is a monotone (strictly increasing) transform applied
#    only for comparison, so it cannot change the ordering - it is pure cost.
#    The real win is not speed (n sqrt calls is noise) but EXACTNESS: comparing
#    ints is exact, comparing floats is approximate. At these constraints
#    (|x|,|y| <= 10^4 so dist^2 <= 2*10^8) float64 has ample headroom and the
#    submission was not buggy - but the habit generalizes to magnitudes where it is.
#    NOT a space saving: CPython float is 24 bytes, an int this size is 28.
#
# 2. HEAPIFY ONCE instead of n heappush calls. n pushes is O(n log n); building
#    the list and heapifying is O(n) (Floyd's bottom-up build). The k pops are
#    unchanged at O(log n) each, so the total drops from
#        O(n log n)  ->  O(n + k log n).
#    It does NOT collapse to O(n) - the pops survive unless k is constant.
#
# 3. DROPPED THE TIEBREAKER INDEX. The submission carried `(dist, i, point)`,
#    reusing the unique-counter trick from LC 23. It is dead weight HERE, and the
#    reason is the whole lesson: LC 23 needed it because its payload was a
#    `ListNode`, which defines no ordering, so a distance tie sent tuple
#    comparison into a `TypeError`. This payload is a `list`, and lists compare
#    lexicographically exactly like tuples - `[1, 2] < [3, 4]` is fine. The rule
#    was never "heaps need a tiebreaker"; it is "check whether the payload is
#    orderable." Flattening to `(dist, x, y)` makes every element an int, so the
#    question cannot arise at any position. (Ties are also free here: the problem
#    states the answer may be returned in any order.)
#
# 4. Added real imports (`typing`, and no `math` needed once sqrt is gone),
#    annotated the heap and result, moved `result` to its point of use, and
#    used `_` for the unused loop variable.
#
# Not done deliberately: the pops can be folded into a nested comprehension
# one-liner. It is denser without being clearer, so the explicit loop stays.
#
# Active: O(n + k log n) time, O(n) space.


# ---------------------------------------------------------------------------
# Alt 1 - David's accepted submission, VERBATIM (the honest practice record)
# O(n log n) time (n individual pushes), O(n) space
# ---------------------------------------------------------------------------
# import heapq
#
# class Solution:
#     def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
#         heap = []
#         result = []
#         for i, point in enumerate(points):
#             dist = math.sqrt(point[0]*point[0] + point[1]*point[1])
#             heapq.heappush(heap, (dist, i, point))
#         for i in range(k):
#             _, _, point = heapq.heappop(heap)
#             result.append(point)
#         return result


# ---------------------------------------------------------------------------
# Alt 2 - bounded size-k MAX-heap (the LC 703 pattern applied here)
# O(n log k) time, O(k) SPACE - the streaming / huge-n answer
# ---------------------------------------------------------------------------
# Keep the k closest seen so far. To evict cheaply you need the FARTHEST of them
# in O(1), so the heap must be a max-heap -> negate the key (heapq is min-only).
# The same inversion as 703: the value you need at the root is the one you are
# about to THROW AWAY, not the one you report.
#
# def k_closest_bounded(points: List[List[int]], k: int) -> List[List[int]]:
#     heap: List[Tuple[int, int, int]] = []
#     for x, y in points:
#         heapq.heappush(heap, (-(x * x + y * y), x, y))
#         if len(heap) > k:
#             heapq.heappop(heap)          # drop the current farthest
#     return [[x, y] for _, x, y in heap]  # heap order is arbitrary - fine, any order allowed
#
# Worth being precise about the trade: this is NEVER asymptotically faster than
# the active version. Compare n log k against n + k log n - the first is worse or
# equal for every k. What it buys is SPACE, O(k) instead of O(n), and it is the
# only version that works when `points` is a stream you cannot hold in memory.
# That is the "what if there are 10^9 points?" follow-up.


# ---------------------------------------------------------------------------
# Alt 3 - QUICKSELECT (Hoare's selection algorithm)
# O(n) AVERAGE time, O(n^2) worst, O(1) extra space - the true time-optimal answer
# ---------------------------------------------------------------------------
# This is quicksort's Lomuto partition (see wiki concepts/sorting-algorithms) with
# exactly one change: after partitioning, the pivot sits at its FINAL index, so you
# already know which side holds rank k-1 - and you recurse into that side ONLY.
# Quicksort recurses into both, which is where its log factor comes from. Dropping
# one side makes the work a geometric series: n + n/2 + n/4 + ... = 2n = O(n).
#
# The O(n^2) worst case is inherited unchanged (every pivot the extreme element,
# so each round peels off one element). A RANDOM pivot makes that adversarially
# unreachable, which is why the swap-to-hi below is not decoration.
#
# import random
#
# def k_closest_quickselect(points: List[List[int]], k: int) -> List[List[int]]:
#     def dist(p: List[int]) -> int:
#         return p[0] * p[0] + p[1] * p[1]
#
#     def partition(lo: int, hi: int) -> int:
#         pivot = dist(points[hi])
#         store = lo
#         for i in range(lo, hi):
#             if dist(points[i]) < pivot:
#                 points[store], points[i] = points[i], points[store]
#                 store += 1
#         points[store], points[hi] = points[hi], points[store]
#         return store                      # pivot's final index
#
#     target = k - 1                        # we want ranks 0 .. k-1 settled
#     lo, hi = 0, len(points) - 1
#     while lo < hi:
#         r = random.randint(lo, hi)        # random pivot -> guards the O(n^2) case
#         points[r], points[hi] = points[hi], points[r]
#         p = partition(lo, hi)
#         if p == target:
#             break                         # slots 0..k-1 now hold the k closest
#         elif p < target:
#             lo = p + 1                    # recurse RIGHT only
#         else:
#             hi = p - 1                    # recurse LEFT only
#     return points[:k]
#
# Two caveats an interviewer will probe:
#   - It MUTATES `points` in place (permutes the caller's list). Same in-place
#     hazard as heapq.heapify on someone else's list - copy first if it is not
#     yours to reorder.
#   - It cannot stream. It needs random access to all n elements at once, so it is
#     strictly a one-shot, static-array algorithm. Alt 2 is the opposite trade.
# This is the technique LC 215 (Kth Largest Element in an Array) drills.


# ---------------------------------------------------------------------------
# Alt 4 - just sort (the baseline worth SAYING in an interview before optimizing)
# O(n log n) time, O(n) space
# ---------------------------------------------------------------------------
# def k_closest_sort(points: List[List[int]], k: int) -> List[List[int]]:
#     return sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1])[:k]
#
# One line, obviously correct, and `sorted` returns a new list so it does not
# mutate the input. Stating it first and then beating it is the right opening
# move; handing it in as the final answer is not, since it is dominated by both
# the heap (space, streaming) and quickselect (time).
