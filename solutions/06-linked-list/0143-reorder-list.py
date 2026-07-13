# Reorder List - LC 143 - Medium - [Blind 75]
# Pattern: Linked List (the consolidation problem - chains all three moves:
#          find-middle via fast/slow -> reverse second half (LC 206) ->
#          weave the two halves (a value-free LC 21 merge))
# Solved 2026-07-12 | outcome: hint
#
# Raw: Data Structures & Algorithms/reorder-linked-list/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was correct but wove the halves with an LC 21 dummy + tail merge
# skeleton; the active code uses the canonical in-place pointer-swap weave (no
# dummy - `first` already IS the head). David's verbatim accepted submission is
# preserved as Alt 1 (the dummy-weave variant); the O(n)-space array brute force
# reasoned in Phase 1 is Alt 2.
#
# Definition for singly-linked list:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        # Phase 1: find the split point (find-middle payoff of fast/slow).
        # slow = fast = head lands slow on the first node of the second half
        # (even) or the exact middle (odd); cutting at slow.next makes the
        # FIRST half >= the second in both cases.
        slow = fast = head
        while fast and fast.next:       # fast FIRST -> short-circuit before .next
            slow = slow.next            # tortoise: one node per step
            fast = fast.next.next       # hare: two nodes per step
        second = slow.next
        slow.next = None                # LOAD-BEARING cut: severs the two halves

        # Phase 2: reverse the second half in place (the LC 206 three-pointer).
        prev = None
        curr = second
        while curr:
            nxt = curr.next             # save next BEFORE clobbering it
            curr.next = prev            # flip this node's link backward
            prev = curr
            curr = nxt
        second = prev                   # prev is the reversed head (old tail)

        # Phase 3: weave the two halves, alternating (value-free merge).
        # first half is always >= second, so drive the loop on `second`; the
        # leftover first-half tail is already attached (never rewired).
        first = head
        while second:
            tmp1, tmp2 = first.next, second.next   # capture BOTH before rewiring
            first.next = second                    # first -> second
            second.next = tmp1                     # second -> next first
            first = tmp1
            second = tmp2
        # in-place, nothing to return


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Phases 1 and 2 are identical to the accepted submission (same fast/slow split,
# same cut at slow.next, same three-pointer reversal). Only Phase 3 (the weave)
# was rewritten:
#   - Dropped the `dummy` + `tail` merge scaffold. The accepted version reused
#     the LC 21 dummy/tail skeleton to interleave; it is CORRECT (head is the
#     first node appended, so dummy.next is head and the list is rewired in
#     place), but it allocates a dummy and carries an extra `tail` cursor.
#   - Active weave is the canonical in-place pointer swap: `first` already IS
#     the head, so we rewire `first.next`/`second.next` directly, saving BOTH
#     next-nodes first (capture-before-overwrite, twice). No allocation.
#   - Removed the redundant `return None` (signature is -> None, modified in
#     place; a bare fall-through is conventional).
# No convention slips in the typed version to fix (snake_case, no Unicode,
# PEP 8 clean). reorderList / ListNode / Optional are LeetCode's fixed
# signature, not naming choices.
#
# Key insight - the cut (`slow.next = None`) is load-bearing:
#   It is the least visually obvious line and the one most likely to be
#   "cleaned up" by mistake. Without it, after the weave the first half's tail
#   still points into the second half -> a cycle / double-linked overlap, and
#   LeetCode's structure check fails. The cut is a first-class step, not
#   bookkeeping.
#
# Why the halves come out UNEVEN: with slow = fast = head, cutting at slow.next
# gives first >= second (for [1,2,3,4]: first=1->2->3, second=4). That is fine
# and is exactly why the weave drives on `while second` (the shorter/equal half)
# and the leftover first-half node needs no explicit re-attach - its link was
# never touched.
#
# Edge cases fall out with zero special-casing: single node (loop bodies never
# run, list unchanged) and two nodes ([1,2] -> [1,2]) both pass. LeetCode
# guarantees >= 1 node, so head is never None here.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(1) space
#        Weave via the LC 21 dummy + tail merge skeleton (value-free). Correct
#        because head is the first node appended, so dummy.next is head and the
#        list ends up rewired in place - a nice "I recognize this shape" reuse,
#        just one allocation heavier than the in-place swap above.
# ---------------------------------------------------------------------------
# class Solution:
#     def reorderList(self, head: Optional[ListNode]) -> None:
#         # Find midpoint and split lists
#         slow = fast = head
#         while fast and fast.next:
#             slow = slow.next
#             fast = fast.next.next
#         second = slow.next
#         slow.next = None
#         # Reverse second
#         prev = None
#         curr = second
#         while curr:
#             nxt = curr.next
#             curr.next = prev
#             prev = curr
#             curr = nxt
#         first = head
#         second = prev
#         # Weave first and (reversed) second
#         dummy = ListNode()
#         tail = dummy
#         curr_1 = first
#         curr_2 = second
#         while curr_2:
#             curr_1_nxt = curr_1.next
#             curr_2_nxt = curr_2.next
#             tail.next = curr_1
#             tail = curr_1
#             tail.next = curr_2
#             tail = curr_2
#             curr_1 = curr_1_nxt
#             curr_2 = curr_2_nxt
#         tail.next = curr_1
#         return None


# ---------------------------------------------------------------------------
# Alt 2: array of node references (brute force) - O(n) time, O(n) SPACE
#        The naive approach reasoned in Phase 1. Walk once collecting node
#        objects into a list (random access), then two-pointer inward from both
#        ends, rewiring next pointers. The O(n) space is the whole reason the
#        fast/slow + reverse + weave version is preferred; kept as the
#        motivating contrast.
# ---------------------------------------------------------------------------
# class Solution:
#     def reorderList(self, head: Optional[ListNode]) -> None:
#         nodes = []
#         curr = head
#         while curr is not None:
#             nodes.append(curr)
#             curr = curr.next
#         left, right = 0, len(nodes) - 1
#         while left < right:
#             nodes[left].next = nodes[right]
#             left += 1
#             if left == right:           # odd length: middle is now the tail
#                 break
#             nodes[right].next = nodes[left]
#             right -= 1
#         nodes[left].next = None         # terminate at the new tail
