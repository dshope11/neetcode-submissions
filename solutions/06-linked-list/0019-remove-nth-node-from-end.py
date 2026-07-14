# Remove Nth Node From End of List - LC 19 - Medium - [Blind 75]
# Pattern: Linked List (same-speed fixed-GAP two-pointer + dummy/sentinel node).
#          Open a gap of n+1 between two same-speed pointers, walk both until the
#          lead hits None, and the trailing pointer lands just BEFORE the target.
# Solved 2026-07-14 | outcome: solo
#
# Raw: Data Structures & Algorithms/remove-node-from-end-of-linked-list/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was correct O(n)/O(1), but fused the gap-opening and the lockstep
# walk into ONE loop with a per-iteration `if iter < n + 1` branch. The active
# code splits it into two loops (open the gap once, then walk in lockstep) - no
# counter, no per-node comparison, and it reads as the mental model directly.
# David's verbatim accepted submission is preserved as Alt 1; the two-pass
# length-first brute force reasoned in Phase 1 is Alt 2.
#
# Definition for singly-linked list:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Dummy anchors the list so "remove the head" needs no special branch:
        # if the target is head, `second` never leaves dummy and dummy.next is
        # simply repointed past it.
        dummy = ListNode(0, head)
        first = second = dummy

        # Open a gap of n+1 between the two same-speed pointers (do it once).
        for _ in range(n + 1):
            first = first.next

        # Walk both in lockstep until the lead runs off the end. `second` then
        # sits exactly one node BEFORE the target (the node whose .next we drop).
        while first:
            first = first.next
            second = second.next

        second.next = second.next.next     # splice out the nth-from-end node
        return dummy.next


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Same algorithm, same invariant (gap of n+1, stop when lead is None, trailing
# lands before target). Two changes, both cleanup - no correctness/complexity
# difference:
#   - Split the single `while first: if iter < n + 1: ... else: ...` loop into a
#     `for _ in range(n + 1)` gap-open followed by a `while first` lockstep walk.
#     The typed version ran the `iter < n + 1` test on EVERY node for the whole
#     list even after the gap was fully open and the branch never flipped again;
#     the two-loop form drops the `iter` counter and the per-step comparison
#     entirely. Fewer ops per node (same O(n)), and it reads as "open a gap, then
#     walk together" instead of forcing the reader to re-derive that from a
#     counter.
#   - Collapsed `dummy = ListNode(); dummy.next = head` into the one-liner
#     `dummy = ListNode(0, head)`.
#
# Convention slip in the typed version (fixed here, preserved in Alt 1):
#   - `iter = 0` SHADOWS the built-in `iter()`. Harmless in this snippet, but
#     it's exactly the "shadowing a built-in" gotcha on the DSA cheat sheet - a
#     later `iter(...)` call would raise `TypeError: 'int' object is not
#     callable`. The two-loop rewrite removes the counter, so the name is gone.
# removeNthFromEnd / ListNode / Optional are LeetCode's fixed signature.
#
# Key insight - why the dummy erases the head special-case:
#   Without a dummy, removing the head (n == length) has no `prev` node to
#   repoint, forcing an `if <target is head>: head = head.next` branch. Anchoring
#   with dummy -> head means `second` starts one step BEHIND head; if the target
#   IS head, the lead pointer runs off during the initial n+1 advance, `second`
#   never leaves dummy, and `second.next = second.next.next` splices head out
#   like any interior node. Returning dummy.next yields the new head whether or
#   not it changed. Same device that was load-bearing in LC 21 / LC 143.
#
# Why the gap is n+1 (not n): we want `second` to stop on the node BEFORE the
#   target (position L-n), and the lead to stop at None (position L+1). The gap
#   is (L+1) - (L-n) = n+1. The sibling formulation advances the lead only n
#   steps and stops on `while first.next` instead - lands `second` on the same
#   node. Either works; pick one and be consistent or you're off by one.
#
# Edge cases fall out with no special-casing: remove head (n == length, traced
#   above) and single node [1], n=1 (lead advances to None, second stays at
#   dummy, dummy.next -> None, returns []). LeetCode guarantees 1 <= n <= length,
#   so second.next is never None at the splice.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(1) space
#        Correct - fuses the gap-open and lockstep walk into one loop with an
#        `iter` counter and a per-node `if iter < n + 1` branch. Same invariant
#        (gap n+1, stop at None). Note `iter` shadows the built-in.
# ---------------------------------------------------------------------------
# class Solution:
#     def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
#         dummy = ListNode()
#         dummy.next = head
#         first = second = dummy
#         iter = 0
#
#         while first:
#             if iter < n + 1:
#                 first = first.next
#                 iter += 1
#             else:
#                 first = first.next
#                 second = second.next
#
#         second.next = second.next.next
#
#         return dummy.next


# ---------------------------------------------------------------------------
# Alt 2: two-pass, length first (brute force) - O(n) time, O(1) space
#        The naive approach reasoned in Phase 1. Pass 1 measures the length;
#        pass 2 walks to the node BEFORE the target (length - n steps from dummy)
#        and splices it out. Same O(n)/O(1), but touches the list TWICE - the
#        one-pass gap version is preferred when a single traversal matters.
# ---------------------------------------------------------------------------
# class Solution:
#     def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
#         length = 0
#         curr = head
#         while curr:
#             length += 1
#             curr = curr.next
#         dummy = ListNode(0, head)
#         prev = dummy
#         for _ in range(length - n):     # walk to the node before the target
#             prev = prev.next
#         prev.next = prev.next.next
#         return dummy.next
