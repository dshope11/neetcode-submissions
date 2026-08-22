# Find Median from Data Stream - LC 295 - Hard - Blind 75
# Pattern: Heap / Priority Queue. TWO heaps facing each other across the median:
#          a MAX heap holding the lower half (stored negated, since heapq is
#          min-only) and a MIN heap holding the upper half. The two values that
#          define the median are then both at a heap root, readable in O(1).
#          The one problem in this section where a single heap is not enough.
# Solved 2026-08-22 | outcome: solo
#          (Prior exposure: the two-heap median was met while prepping the
#          Anthropic ICF assessment, so the pattern was recalled rather than
#          derived from nothing. Everything downstream of the recall - the
#          routing comparison, the size invariant, the rebalance - was driven
#          unaided, with no code or technique taken.)
#
# Raw: Data Structures & Algorithms/find-median-in-a-data-stream/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"). David's
# verbatim accepted submission is preserved as Alt 1.
#
# Typing note: neetcode.io pre-fills the class/method signatures and pre-imports
# the typing names, so the submission omits `from typing import List`; it is
# added below so this file is honest and runnable standalone. The camelCase
# method names `addNum` / `findMedian` are LeetCode's required API and are kept
# deliberately - they are not a naming-convention slip.
#
# Style notes on the typed submission (all fixed in the active code, all still
# visible in Alt 1): `__init__` missing its `-> None`; no attribute annotations;
# the odd-length branch of `findMedian` returns an `int` while the method is
# annotated `-> float`; a stray blank line after the `class` statement.

from typing import List
import heapq


class MedianFinder:
    """Streaming median, backed by two heaps that partition the stream in half.

    TWO invariants hold after every addNum returns, and BOTH are load-bearing:

      1. ORDERING: every element of `small` is <= every element of `large`.
         This is what makes a heap root mean "the middle element" at all. The
         size invariant alone does not give a correct median - two heaps of the
         right sizes holding the wrong elements return garbage.

      2. SIZE: len(small) == len(large), or len(small) == len(large) + 1.
         The lower half is allowed to run one long, never the upper half, so an
         odd-length stream always puts the median at small's root.

    Invariant 1 survives despite routing comparing ONLY against large[0] and
    never against small[0], because all three operations move exactly the
    boundary element - the only element that can cross without breaking order:
      - routing:   num <= large[0] means num <= the MINIMUM of large, hence <=
                   every element of large, so small is a safe home.
      - small -> large: moves small's MAXIMUM, which is <= all of large, so it
                   lands as large's new minimum.
      - large -> small: moves large's MINIMUM, which is >= all of small, so it
                   lands as small's new maximum.
    """

    def __init__(self) -> None:
        # Lower half as a MAX heap: heapq is min-only, so every value is stored
        # negated. -self.small[0] is the true maximum of the lower half.
        self.small: List[int] = []
        # Upper half as a plain MIN heap; self.large[0] is its true minimum.
        self.large: List[int] = []

    def addNum(self, num: int) -> None:
        # Route on a SINGLE comparison. The `self.large and` guard is the only
        # concession to emptiness anywhere in the class - no special case is
        # needed for the first or second insert, because the size repair below
        # already handles n = 1 and n = 2.
        if self.large and num > self.large[0]:
            heapq.heappush(self.large, num)
        else:
            heapq.heappush(self.small, -num)

        # Repair the SIZE invariant. Note the deliberate asymmetry in the two
        # thresholds: small may exceed large by one, large may never exceed
        # small at all. A single push shifts a length by exactly 1, so the
        # imbalance can never exceed the slack by more than one element and one
        # transfer always suffices.
        #
        # if/elif, not two ifs: the second test reads lengths the first branch
        # just mutated (the LC 703 / LC 235 mutually-exclusive-branches bug).
        # They are in fact provably exclusive here - after either repair the
        # difference is already legal - but the elif makes that non-negotiable
        # rather than something a reader has to re-derive.
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        elif len(self.small) < len(self.large):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        # Odd length: the lower half is the longer one, so its root IS the
        # median. This branch is also what keeps n = 1 safe - `large` is empty
        # then, and large[0] is never evaluated on this path.
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        # Even length: average the two elements straddling the split.
        return (-self.small[0] + self.large[0]) / 2
#
# addNum: O(log n) - at most two heap operations, each O(log n).
# findMedian: O(1) - two array reads, no traversal.
# Space: O(n) - every element seen is retained across the two heaps.
#
# ---------------------------------------------------------------------------
# What changed from the accepted submission (Alt 1):
#   1. Added `-> None` on `__init__` and `List[int]` annotations on both heap
#      attributes; added an explicit `from typing import List` so the file runs
#      outside neetcode.io.
#   2. `float(-self.small[0])` in the odd branch. The submission returned a bare
#      `int` from a method annotated `-> float`. The judge accepts it (an int is
#      numerically exact, well inside the 10^-5 tolerance) and Python does not
#      enforce annotations at runtime - but the annotation is a contract, and
#      honoring it costs nothing.
#   3. Dropped the stray blank line after the `class` statement (PEP 8).
#   4. Collapsed `findMedian`'s `else` into a bare trailing return - the `if`
#      branch already returns.
#   5. Comments naming BOTH invariants and, in the docstring, the argument for
#      why the ordering invariant survives a routing test that only ever looks
#      at large[0]. That argument is the actual correctness proof and was the
#      one thing missing from the interview discussion.
#   No algorithmic changes: the submission was correct and already optimal.
# ---------------------------------------------------------------------------
#
#
# Alt 1 - David's accepted submission, VERBATIM: O(log n) addNum, O(1)
#         findMedian, O(n) space. Correct as submitted; only style changes
#         above.
#
# import heapq
#
# class MedianFinder:
#
#     def __init__(self):
#         self.small = []
#         self.large = []
#
#     def addNum(self, num: int) -> None:
#         if self.large and num > self.large[0]:
#             heapq.heappush(self.large, num)
#         else:
#             heapq.heappush(self.small, -num)
#         if len(self.small) > len(self.large) + 1:
#             heapq.heappush(self.large, -heapq.heappop(self.small))
#         elif len(self.small) < len(self.large):
#             heapq.heappush(self.small, -heapq.heappop(self.large))
#
#     def findMedian(self) -> float:
#         if len(self.small) > len(self.large):
#             return -self.small[0]
#         else:
#             return (-self.small[0] + self.large[0]) / 2
#
#
# Alt 2 - UNCONDITIONAL ROUTE ("push blind, then repair"): O(log n) addNum,
#         O(1) findMedian, O(n) space.
#         Drops the routing comparison AND the empty-heap guard entirely. Every
#         value goes into `small` unconditionally; small's maximum is then
#         shuttled to `large` unconditionally, which ENFORCES the ordering
#         invariant instead of relying on a comparison to preserve it; only then
#         is the size invariant restored.
#         Trade: always 3 heap operations where the active version does 1 to 3,
#         so a constant-factor loss for a genuine drop in branching. Worth
#         knowing as the answer to "can you make the case analysis go away?"
#
# class MedianFinder:
#     def __init__(self) -> None:
#         self.small: List[int] = []   # max heap (negated), lower half
#         self.large: List[int] = []   # min heap, upper half
#
#     def addNum(self, num: int) -> None:
#         heapq.heappush(self.small, -num)
#         # Force the largest of the lower half across. No comparison needed:
#         # whatever is now small's max is by construction the correct candidate
#         # for large's min.
#         heapq.heappush(self.large, -heapq.heappop(self.small))
#         # `large` may now be one too long; the lower half is the one allowed
#         # to run long, so pull the boundary element back.
#         if len(self.large) > len(self.small):
#             heapq.heappush(self.small, -heapq.heappop(self.large))
#
#     def findMedian(self) -> float:
#         if len(self.small) > len(self.large):
#             return float(-self.small[0])
#         return (-self.small[0] + self.large[0]) / 2
#
#
# Alt 3 - SORTED INSERT via bisect.insort: O(n) addNum, O(1) findMedian,
#         O(n) space.
#         The middle rung between brute force and the heaps - and the one that
#         makes the ops budget interesting, because it ACTUALLY PASSES the judge
#         despite being asymptotically worse.
#
# from bisect import insort
#
# class MedianFinder:
#     def __init__(self) -> None:
#         self.nums: List[int] = []
#
#     def addNum(self, num: int) -> None:
#         insort(self.nums, num)          # O(log n) to locate, O(n) to shift
#
#     def findMedian(self) -> float:
#         n = len(self.nums)
#         mid = n // 2
#         if n % 2:
#             return float(self.nums[mid])
#         return (self.nums[mid - 1] + self.nums[mid]) / 2
#
#         # Why it passes anyway - the ops-budget lesson:
#         # 5*10^4 addNum calls over an average n of 2.5*10^4 is ~1.25*10^9
#         # element moves. Against the 703 budget (~10^7 pure-Python loop
#         # iterations/sec) that should be hopeless. It is not, because the
#         # shift is NOT a Python loop: list.insert moves a contiguous block of
#         # pointers with a C-level memmove at memory-bandwidth speed, roughly
#         # 10^9 moves/sec - about 100x faster per "operation" than an
#         # interpreted iteration. Total: on the order of a second.
#         #
#         # The transferable rule: THE OPS BUDGET IS PER-OPERATION-KIND, NOT
#         # UNIVERSAL. This is exactly why an O(n^2)-on-paper solution built out
#         # of C-level bulk calls sometimes beats an O(n log n) one written as
#         # Python loops.
#         #
#         # Still the wrong answer to give: O(n) per add degrades the moment the
#         # interviewer says "now imagine 10^7 elements", where the heaps' O(log
#         # n) does not.
#
#
# Alt 4 - BRUTE FORCE, re-sort every call: O(n log n) per call, O(n) space.
#         The baseline to state and then beat.
#
# class MedianFinder:
#     def __init__(self) -> None:
#         self.nums: List[int] = []
#
#     def addNum(self, num: int) -> None:
#         self.nums.append(num)
#
#     def findMedian(self) -> float:
#         s = sorted(self.nums)
#         n = len(s)
#         mid = n // 2
#         if n % 2:
#             return float(s[mid])
#         return (s[mid - 1] + s[mid]) / 2
#
#         # Why it fails: sorting per call over an average n of 2.5*10^4 across
#         # 5*10^4 calls is ~5*10^4 * 2.5*10^4 * log2(2.5*10^4) ~ 1.8*10^10
#         # comparisons. Even at C speed that is tens of seconds.
#
#
# Alt 5 - FOLLOW-UP 1, all values in [0, 100]: O(1) addNum, O(1) findMedian,
#         O(1) SPACE - which is the real win, and the column that is easy to
#         miss when comparing only the time complexities.
#         COUNTING SORT's trade: a bounded key range lets you INDEX instead of
#         COMPARE. Same reason bucket sort beat the heap on Top K Frequent
#         Elements (347) back in section 1.
#         Note the constraint is on the VALUES, not on their multiplicity - the
#         stream may be unbounded and duplicates are the normal case, which is
#         precisely why the buckets hold COUNTS rather than presence flags.
#
# class MedianFinder:
#     def __init__(self) -> None:
#         self.counts: List[int] = [0] * 101
#         self.n = 0
#
#     def addNum(self, num: int) -> None:
#         self.counts[num] += 1
#         self.n += 1
#
#     def findMedian(self) -> float:
#         # 1-based ranks of the middle element(s). For odd n these coincide, so
#         # one sweep covers both parities - the two middle values can land in
#         # DIFFERENT buckets when n is even, so do not sweep twice.
#         lo_rank = (self.n + 1) // 2
#         hi_rank = (self.n + 2) // 2
#         seen = 0
#         # -1 as the "not yet found" sentinel, NOT 0: every bucket index is a
#         # legitimate answer, and 0 is one of them. Keying an empty sentinel on
#         # a value the answer can actually take is the LC 76 bug.
#         lo = hi = -1
#         for value, count in enumerate(self.counts):
#             if count == 0:
#                 continue
#             seen += count
#             if lo < 0 and seen >= lo_rank:
#                 lo = value
#             if seen >= hi_rank:
#                 hi = value
#                 break
#         return (lo + hi) / 2
#
#         # findMedian is O(101) = O(1), a constant sweep - fatter than the
#         # heaps' two array reads, but still constant. addNum drops from
#         # O(log n) to O(1), and space from O(n) to O(1).
#
#
# Alt 6 - FOLLOW-UP 2, 99% of values in [0, 100], 1% arbitrary (reasoned, not
#         coded).
#         Keep the counting array for the in-range values, plus two counters,
#         `below` and `above`, for the out-of-range ones. The minimum you need
#         to know about an outlier is only WHICH SIDE it fell on: `below` values
#         precede every bucket, so sweep the 101 buckets for rank (k - below)
#         instead of rank k. Equal counts on both sides is just the special case
#         where the offset cancels.
#         That is sufficient unless (k - below) falls outside [1, in_range_count]
#         - i.e. the median is itself an outlier. Only then do you need the
#         actual outlier VALUES, so keep them in something ordered (a small
#         sorted list, or the two heaps above) - cheap precisely because it is
#         1% of the stream. Naming that boundary and its fallback is a stronger
#         answer than the counters alone.
