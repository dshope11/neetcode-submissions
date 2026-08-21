# Kth Largest Element in a Stream - LC 703 - Easy
# Pattern: Heap / Priority Queue (section opener). A MIN heap capped at size k
#          holding the k largest values seen so far, so heap[0] is at once the
#          weakest member - the eviction candidate a new arrival must beat -
#          AND the answer, the kth largest.
# Solved 2026-08-20 | outcome: hint
#
# Raw: Data Structures & Algorithms/kth-largest-integer-in-a-stream/submission-2.py
#      (NeetCode's own slug says "integer"; the "-2" is their internal counter -
#      it is the only file in that folder, not a re-solve.)
#
# Active code below is the CLEANED version (see "What changed"). David's
# verbatim accepted submission is preserved as Alt 1.
#
# Typing note: neetcode.io pre-fills the class/method signatures and pre-imports
# the typing names, so the submission omits `from typing import List`; it is
# added below so this file is honest and runnable standalone.
#
# Style notes on the typed submission (all fixed in the active code, all still
# visible in Alt 1): a dead `return` as the last statement of `__init__`;
# `i <= k-1` where `i < k` is the idiomatic "first k" test - and that expression
# is exactly where the solve's first bug lived, as `i <= k`; `__init__` missing
# its `-> None`.

from typing import List
import heapq


class KthLargest:
    """Streaming kth-largest, backed by a min heap capped at size k."""

    def __init__(self, k: int, nums: List[int]) -> None:
        self.k = k
        # Slice rather than heapify(nums) directly: heapify mutates IN PLACE, and
        # a constructor that silently permutes the caller's list is an API bug.
        # Slicing also clamps - nums[:k] is safe even when len(nums) < k, where
        # nums[k] would raise IndexError.
        self.heap = nums[:k]
        heapq.heapify(self.heap)                 # O(k) build, not O(k log k)
        for num in nums[k:]:
            heapq.heappushpop(self.heap, num)    # one sift, not push-then-pop

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:              # stream hasn't reached k yet
            heapq.heappush(self.heap, val)
        else:
            heapq.heappushpop(self.heap, val)    # admit val, evict the weakest
        return self.heap[0]                      # kth largest - NOT the evicted
                                                 # value, which ranks k+1
#
# Constructor: O(k + (n - k) log k), i.e. O(n log k).  add: O(log k).
# Space: O(k) - independent of stream length, which is what makes this work on
# an unbounded stream at all.
#
# ---------------------------------------------------------------------------
# What changed from the accepted submission (Alt 1):
#   1. Dropped the dead `return` at the end of `__init__`.
#   2. Replaced the `enumerate` + `if i <= k-1` index test with slicing
#      (`nums[:k]` / `nums[k:]`). Same result, one less branch in the loop, and
#      it removes the off-by-one surface where the solve's first bug lived.
#   3. Built the initial heap with `heapq.heapify` - O(k) - instead of k
#      individual `heappush` calls at O(k log k). Does not change the overall
#      O(n log k), since the pushpop pass dominates, but it is free.
#   4. Added `-> None` on `__init__` and an explicit `from typing import List`
#      so the file is runnable outside neetcode.io.
#   5. Comments naming the invariant and the heapify-mutates-in-place hazard.
# ---------------------------------------------------------------------------
#
#
# Alt 1 - David's accepted submission, VERBATIM: O(n log k) init, O(log k) add,
#         O(k) space. Correct as submitted; only style/constant-factor changes
#         above.
#
# import heapq
#
#
# class KthLargest:
#
#     def __init__(self, k: int, nums: List[int]):
#         self.k = k
#         self.heap = []
#         for i, num in enumerate(nums):
#             if i <= k-1:
#                 heapq.heappush(self.heap, num)
#             else:
#                 heapq.heappushpop(self.heap, num)
#         return
#
#     def add(self, val: int) -> int:
#         if len(self.heap) < self.k:
#             heapq.heappush(self.heap, val)
#         else:
#             heapq.heappushpop(self.heap, val)
#         return self.heap[0]
#
#
# Alt 2 - the DRY-est form: O(n log k) init, O(log k) add, O(k) space.
#         The constructor loop IS `add` minus the return value, so it can just
#         delegate. Shortest and least duplicated, but it forfeits the O(k)
#         heapify - every one of the first k elements goes in via heappush.
#         A fine answer to "can you tighten this up?"; the active version is
#         the one to give when asked for the fastest constructor.
#
# class KthLargest:
#     def __init__(self, k: int, nums: List[int]) -> None:
#         self.k = k
#         self.heap: List[int] = []
#         for num in nums:
#             self.add(num)
#
#     def add(self, val: int) -> int:
#         if len(self.heap) < self.k:
#             heapq.heappush(self.heap, val)
#         else:
#             heapq.heappushpop(self.heap, val)
#         return self.heap[0]
#
#
# Alt 3 - brute force, sort on every call: O(n log n) PER add, O(n) space.
#         The baseline to state and then beat. Kept here for the complexity
#         argument, not because it passes.
#
# class KthLargest:
#     def __init__(self, k: int, nums: List[int]) -> None:
#         self.k = k
#         self.nums = list(nums)
#
#     def add(self, val: int) -> int:
#         self.nums.append(val)
#         return sorted(self.nums)[-self.k]
#
#         # Why it fails the judge: n grows to ~6000 and add is called up to
#         # 5000 times, so this is ~5000 * 6000 * log(6000) ~ 4 * 10^8 heavy
#         # comparisons. The variant reasoned in the interview - rescan all n
#         # per call while tracking the top k by linear comparison - is O(n*k)
#         # per call, ~10^10 total. CPython runs ~10^7 pure-Python loop
#         # iterations/sec, so that is ~15 minutes against a few-second limit.
#         # Budget rule: ~10^8 simple ops for a C/C++ judge, ~10^6-10^7 in
#         # Python. Always plug the constraint maxima into the final Big-O.
#
#
# Follow-up reasoned in the interview (no code - the reformulation is not
# available for THIS problem, and that is the point):
#   The kth largest of n elements is the (n - k + 1)th SMALLEST, so the same
#   question can always be answered with a heap of size min(k, n - k + 1) -
#   for k = n - 3 that is a max heap of size 4, and for k = n it degenerates to
#   just tracking the minimum. The heap's advantage therefore lives at the ENDS
#   of the k range and vanishes near k = n/2, where both formulations cost
#   O(n log n) and plain sorting is equally good and simpler.
#   That flip needs n to be KNOWN. Here the input is a stream and n grows with
#   every add, so k is genuinely fixed and small against an unbounded n - which
#   is exactly the regime the size-k heap is built for.
