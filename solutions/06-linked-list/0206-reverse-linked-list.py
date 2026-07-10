# Reverse Linked List - LC 206 - Easy - [Blind 75]
# Pattern: Linked List (in-place reversal - a companion move of the
#          fast-slow-pointers section; fast/slow itself does not apply here)
# Solved 2026-07-09 | outcome: hint
#
# Raw: Data Structures & Algorithms/reverse-a-linked-list/submission-0.py
#
# Active code below is the accepted submission verbatim - it was already the
# canonical optimal, so no cleanup was applied (see "What changed").
#
# Definition for singly-linked list:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next        # SAVE next before we clobber it
            curr.next = prev        # flip this node's link backward
            prev = curr             # advance prev
            curr = nxt              # advance curr
        return prev                 # prev = old tail = new head


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Nothing. The accepted submission was already the textbook optimal:
# three-pointer in-place reversal, O(n) time / O(1) space, all edge cases
# (empty / single / multi) handled by the one loop with no branching.
# - `nxt` (not `next`) was already used, so no built-in-shadowing slip to fix.
# - The one-line init `prev, curr = None, head` was offered and declined;
#   the two-line form was kept for readability under pressure.
# Active code == Alt 1 verbatim for this problem.
#
# Key correctness dependency: `nxt = curr.next` MUST run before
# `curr.next = prev`. Reorder them and node 1 loses its link to the rest of
# the list on the first iteration (capture-before-overwrite discipline).
#
# Classic bugs avoided (both surfaced and fixed during the discussion):
#   - return `prev`, NOT `curr` (curr walks off to None at loop end).
#   - loop on `while curr is not None`, NOT `while curr.next is not None`
#     (the latter never flips the last node's pointer).


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(1) space
# ---------------------------------------------------------------------------
# class Solution:
#     def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
#         prev = None
#         curr = head
#         while curr is not None:
#             nxt = curr.next
#             curr.next = prev
#             prev = curr
#             curr = nxt
#         return prev


# ---------------------------------------------------------------------------
# Alt 2: recursive reversal - O(n) time, O(n) stack space
#        Reverse the tail first, then hook the current node onto its end.
#        Same idea, different mechanics; the O(n) call stack is why the
#        iterative form is preferred when O(1) space matters.
# ---------------------------------------------------------------------------
# class Solution:
#     def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
#         if head is None or head.next is None:
#             return head              # base: empty or single node
#         new_head = self.reverseList(head.next)   # reverse everything after head
#         head.next.next = head        # make the next node point back at head
#         head.next = None             # head becomes the new tail
#         return new_head              # new_head bubbles up unchanged


# ---------------------------------------------------------------------------
# Alt 3: build a new list by prepending fresh nodes - O(n) time, O(n) space
#        (David's first-instinct approach in the discussion.) Correct, but it
#        ALLOCATES n new nodes instead of reusing the input - which is exactly
#        why the in-place version is preferred. Kept as the instructive
#        contrast for the "does the output count as space?" conversation.
# ---------------------------------------------------------------------------
# class Solution:
#     def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
#         new_head = None
#         curr = head
#         while curr is not None:
#             new_head = ListNode(curr.val, new_head)  # prepend a fresh node
#             curr = curr.next
#         return new_head
