# Merge K Sorted Lists - LC 23 - Hard - [Blind 75]
# Pattern: Linked List (k-way merge via a min-heap frontier; dummy/sentinel
#          node + splice, reusing the LC 21 merge as the conceptual building
#          block). Closes the Linked List section's Blind spine.
# Solved 2026-08-19 | outcome: hint
#
# Raw: Data Structures & Algorithms/merge-k-sorted-linked-lists/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"). David's
# verbatim accepted submission is preserved as Alt 1.
#
# Typing note: the `class Solution` line and the fully-annotated
# `mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]`
# signature are neetcode.io BOILERPLATE - they were pre-filled by the platform,
# not typed by David (his first typed line was `dummy = ListNode()`). The
# annotations are correct as given: `List[Optional[ListNode]]` properly admits
# an empty list inside `lists` (a None head). neetcode.io also pre-imports the
# typing names, so the submission omits the import; it is added below so this
# file is honest and runnable standalone.
#
# Style notes on the typed submission (all fixed in the active code, all still
# visible in Alt 1): `enum` as a counter name SHADOWS the stdlib `enum` module;
# four characters of trailing whitespace on `class Solution:`; one blank line
# before the top-level class where PEP 8 wants two.

from typing import List, Optional
import heapq


# Definition for singly-linked list:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode()          # sentinel: absorbs the "first node is special" case
        tail = dummy
        heap = []
        counter = 0                 # monotonic tiebreaker - see "the 3-tuple" below

        # Seed the frontier with one entry per NON-EMPTY list. This None guard
        # is a SEPARATE code path from the steady-state guard in the loop:
        # pushing a None head fails on the `node.val` attribute access, before
        # the heap ever compares anything. `lists = []` and `lists = [[], []]`
        # both leave the heap empty, so the drain loop never runs and
        # `dummy.next` is None - the empty cases need no special-casing.
        for node in lists:
            if node is not None:
                heapq.heappush(heap, (node.val, counter, node))
                counter += 1

        while heap:
            # heappop REMOVES and returns the min in O(log k). (h[0] would only
            # PEEK, in O(1) - different operation, easy to conflate.)
            _, _, node = heapq.heappop(heap)

            tail.next = node        # SPLICE the existing node - no allocation
            tail = tail.next

            # Safe to read node.next AFTER the splice: `tail.next = node` wrote
            # the PREVIOUS node's next pointer, not this node's. This node's
            # next is not overwritten until the following iteration.
            if node.next is not None:
                heapq.heappush(heap, (node.next.val, counter, node.next))
                counter += 1

        return dummy.next


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
#   1. `enum` -> `counter`. `enum` is a STDLIB MODULE NAME; using it as a local
#      shadows it for the rest of the scope. Harmless in this file, a real bug
#      in any file that also does `import enum`. Third appearance of the
#      shadowing gotcha in the solve log (after `height` on LC 543 and `iter`
#      on LC 19).
#   2. Added `from typing import List, Optional` (neetcode pre-imports it;
#      spelled out here so the file stands alone).
#   3. Stripped four trailing spaces from `class Solution:`; two blank lines
#      before the top-level class per PEP 8.
#   4. `h` -> `heap` (reads better in review; no behavior change).
#   5. Moved the SPLICE above the successor-push, so the loop body reads in the
#      order the work actually happens: pop -> splice -> advance -> queue the
#      successor. Verified equivalent: the splice writes the *previous* node's
#      `.next`, so `node.next` is still untouched when it is read one line
#      later. Readability only.
# Logic was already optimal and is unchanged.
#
# ---------------------------------------------------------------------------
# The 3-tuple, and the failure it prevents
# ---------------------------------------------------------------------------
# Pushing a bare `node.val` is LOSSY - you get the value back but no way to
# splice the right node or find its successor. So the node rides along in the
# tuple. But a 2-tuple `(val, node)` breaks the moment two values tie: Python
# compares tuples element-by-element and falls through to the node, giving
#     TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'
# The middle element is an unconditionally-unique key, so the comparison can
# never reach element three. A monotonic counter (used here) needs no
# justification; the LIST INDEX 0..k-1 also works, because at most one entry
# per list is live at a time (a list's successor is only pushed after its
# predecessor is popped) - a real invariant, but one more thing to keep true.
# Free bonus of the counter: ties resolve in insertion order, so the merge is
# STABLE.
#
# ---------------------------------------------------------------------------
# Why the output list terminates without ever being null-terminated
# ---------------------------------------------------------------------------
# A spliced node keeps pointing into its ORIGINAL list; nothing nulls it. Each
# one is corrected on the FOLLOWING iteration, when `tail.next` is rewritten -
# except the last. That is safe only because a node with a live successor can
# never BE the last pop: if `node.next` is not None it gets pushed, so the heap
# is non-empty and the loop continues. The terminal None falls out of the
# algorithm's structure rather than being assigned. Same flavor as LC 21's
# one-splice leftover attach.
#
# ---------------------------------------------------------------------------
# Complexity - and one nuance worth not over-claiming
# ---------------------------------------------------------------------------
# N = total nodes across all lists; k = number of lists.
#   Active: O(k + N log k) time, O(k) auxiliary space (output excluded).
# The O(k) term is NOT dominated: lists[i] may be empty, so with k up to 1e4
# and N up to 1e4, k can EXCEED N. Scanning all k lists costs O(k) regardless.
# Nuance: the heap is built with k' individual O(log k') pushes rather than one
# O(k) heapify, where k' = the count of non-empty lists. That looks like a
# missed optimization but is NOT an asymptotic one - k' <= N always (each
# non-empty list contributes at least one node), so the build is dominated by
# the O(N log k) drain either way. heapify here is a constant-factor tidy only.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(k + N log k) time, O(k) space
# ---------------------------------------------------------------------------
# import heapq
#
# class Solution:
#     def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
#         dummy = ListNode()
#         tail = dummy
#         enum = 0
#         h = []
#         for node in lists:
#             if node is not None:
#                 heapq.heappush(h, (node.val, enum, node))
#                 enum += 1
#         while h:
#             # pop tuple with minimum value
#             _, _, node = heapq.heappop(h)
#             # push next value in the list if next isn't None
#             if node.next is not None:
#                 heapq.heappush(h, (node.next.val, enum, node.next))
#                 enum += 1
#             # splice node into return list
#             tail.next = node
#             tail = tail.next
#         return dummy.next


# ---------------------------------------------------------------------------
# Alt 2: PAIRWISE / TOURNAMENT MERGE - O(N log k) time, O(k) space for the
#        round buffer (O(1) if done with index arithmetic in place).
#        The approach David proposed first and asked to have recorded. This is
#        also NeetCode's own reference solution.
#
#        Same asymptotic time as the heap, and it needs no auxiliary structure
#        during the merge itself - just repeated application of the LC 21
#        two-list merge. Each ROUND touches all N nodes once and halves the
#        number of lists, so there are log2(k) rounds: N * log k.
#        The heap was chosen instead mainly for the streaming shape (it never
#        materializes intermediate merged lists) and because the frontier
#        framing generalizes to k-way merges over anything, not just lists.
# ---------------------------------------------------------------------------
# class Solution:
#     def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
#         if not lists:
#             return None
#
#         while len(lists) > 1:
#             merged = []
#             for i in range(0, len(lists), 2):
#                 l1 = lists[i]
#                 # ODD COUNT: the unpaired last list is merged against None,
#                 # which the two-list merge returns unchanged. It is CARRIED
#                 # INTO THE NEXT ROUND, never dropped.
#                 l2 = lists[i + 1] if i + 1 < len(lists) else None
#                 merged.append(self.merge_two(l1, l2))
#             lists = merged
#
#         return lists[0]
#
#     def merge_two(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
#         dummy = ListNode()
#         tail = dummy
#         while l1 and l2:
#             if l1.val <= l2.val:      # <= keeps the merge STABLE
#                 tail.next = l1
#                 l1 = l1.next
#             else:
#                 tail.next = l2
#                 l2 = l2.next
#             tail = tail.next
#         tail.next = l1 or l2          # leftover chain attaches in ONE splice
#         return dummy.next


# ---------------------------------------------------------------------------
# Alt 3: NAIVE K-WAY FRONTIER (linear scan instead of a heap)
#        O(N*k) time, O(1) auxiliary space.
#        The conceptual bridge between the brute force and the heap: the loop
#        shape is already right - maintain k candidates, take the smallest,
#        splice it - but finding the min costs a full O(k) scan instead of
#        O(log k). Swapping the scan for a heap IS the optimization.
# ---------------------------------------------------------------------------
# class Solution:
#     def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
#         heads = list(lists)
#         dummy = ListNode()
#         tail = dummy
#
#         while True:
#             best = -1
#             for i, node in enumerate(heads):        # the O(k) scan, N times
#                 if node is not None and (best == -1 or node.val < heads[best].val):
#                     best = i
#             if best == -1:                          # every list exhausted
#                 break
#             node = heads[best]
#             heads[best] = node.next
#             tail.next = node
#             tail = tail.next
#
#         return dummy.next


# ---------------------------------------------------------------------------
# Alt 4: SEQUENTIAL REPEATED TWO-MERGE (the brute force)
#        O(N*k) time, O(1) auxiliary space.
#        Merge list 0 with list 1, then that result with list 2, and so on.
#        Costs 2n + 3n + ... + k*n = n*(k(k+1)/2 - 1) ~ n*k^2/2, and with
#        n = N/k that is N*k/2 = O(N*k).
#        Note it lands on the SAME bound as Alt 3 by a different mechanism: it
#        never pays k comparisons per node, but the growing accumulator gets
#        re-walked on every merge, so early nodes are visited k times instead
#        of once. The cost moves from the comparison counter to the visit
#        counter.
# ---------------------------------------------------------------------------
# class Solution:
#     def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
#         result = None
#         for node in lists:
#             result = self.merge_two(result, node)
#         return result
#
#     def merge_two(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
#         dummy = ListNode()
#         tail = dummy
#         while l1 and l2:
#             if l1.val <= l2.val:
#                 tail.next = l1
#                 l1 = l1.next
#             else:
#                 tail.next = l2
#                 l2 = l2.next
#             tail = tail.next
#         tail.next = l1 or l2
#         return dummy.next


# ---------------------------------------------------------------------------
# Alt 5: FLATTEN THEN DRAIN - O(N log N) time, O(N) space.
#        Dump every value into one heap up front, heapify in O(N), then pop all
#        N. Correct, and a legitimate stepping stone to state in an interview,
#        but strictly worse on both axes: log N instead of log k, and O(N)
#        space instead of O(k). It also ALLOCATES a fresh node per output
#        element rather than splicing, since only values were kept.
#        Honest caveat: at N, k <= 1e4 the gap between log N and log k is small
#        in practice; the space difference is the more defensible objection.
# ---------------------------------------------------------------------------
# class Solution:
#     def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
#         vals = []
#         for node in lists:
#             curr = node
#             while curr is not None:
#                 vals.append(curr.val)
#                 curr = curr.next
#         heapq.heapify(vals)
#
#         dummy = ListNode()
#         tail = dummy
#         while vals:
#             tail.next = ListNode(heapq.heappop(vals))   # fresh node = the O(N) cost
#             tail = tail.next
#         return dummy.next
