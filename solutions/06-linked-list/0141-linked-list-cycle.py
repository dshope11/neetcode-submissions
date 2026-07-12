# Linked List Cycle - LC 141 - Easy - [Blind 75]
# Pattern: Linked List (fast & slow pointers - Floyd's tortoise & hare;
#          the FIRST true fast/slow problem, the core payoff of the section)
# Solved 2026-07-12 | outcome: solo
#
# Raw: Data Structures & Algorithms/linked-list-cycle-detection/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was already the canonical optimal - only cosmetic alignment to the
# concept-page skeleton. David's verbatim accepted submission is preserved as
# Alt 1; the O(n)-space hash-set brute force is Alt 2.
#
# Definition for singly-linked list:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head

        while fast and fast.next:       # fast FIRST -> short-circuit before .next
            slow = slow.next            # tortoise: one node per step
            fast = fast.next.next       # hare: two nodes per step
            if slow is fast:            # identity, not == : "the same node object"
                return True             # hare lapped tortoise -> a cycle exists

        return False                    # fast hit None -> acyclic, exit clean


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Style-only alignment to the fast-slow-pointers concept-page skeleton; logic
# is identical (same guard, same advance-then-compare, same returns).
#   - Two init lines `fast = head` / `slow = head` -> one line `slow = fast = head`.
#   - Advance `slow` before `fast` inside the loop (canonical skeleton order;
#     no behavior change - both are read off the pre-step positions).
#   - Dropped one trailing-whitespace line.
# No convention slips in the typed version to fix (snake_case, no Unicode,
# PEP 8 all clean). hasCycle / ListNode / Optional are LeetCode's fixed
# signature, not a naming choice.
#
# Key insight - advance-THEN-compare is load-bearing:
#   Both pointers start at `head`, so `slow is fast` is trivially True at the
#   start. Testing collision BEFORE the first move would fire immediately and
#   wrongly return True on every list. Moving first, then comparing, is what
#   makes the shared `slow = fast = head` init safe - the one real trap here.
#
# Why fast/slow over the hash set (Alt 2): both are O(n) time, but fast/slow is
# O(1) SPACE - two pointers, no auxiliary structure. The "detect a cycle without
# extra memory" phrasing is the tell to reach for it. Collision is guaranteed
# in a cycle because the hare gains exactly 1 node on the tortoise each step, so
# the gap shrinks by 1 and can never leapfrog 0 - it must land on it exactly.
#
# Edge cases fall out with zero special-casing: empty list (fast is None, loop
# never runs -> False), single self-loop (cycle, caught inside), single acyclic
# node (fast.next is None, loop never runs -> False). And `slow` is never
# guarded because `fast` runs ahead - slow can't be None while fast isn't.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(1) space
# ---------------------------------------------------------------------------
# class Solution:
#     def hasCycle(self, head: Optional[ListNode]) -> bool:
#         fast = head
#         slow = head
#
#         while fast and fast.next:
#             fast = fast.next.next
#             slow = slow.next
#             if fast is slow:
#                 return True
#
#         return False


# ---------------------------------------------------------------------------
# Alt 2: hash set of visited nodes (brute force) - O(n) time, O(n) SPACE
#        The naive approach reasoned in Phase 1. Store each node OBJECT as it's
#        visited; a repeat means a cycle. Works because a bare ListNode is
#        hashable-by-identity (id()) even though it's mutable - set membership
#        is exactly the "same object?" test. The O(n) space is the whole reason
#        fast/slow is preferred; kept as the motivating contrast.
# ---------------------------------------------------------------------------
# class Solution:
#     def hasCycle(self, head: Optional[ListNode]) -> bool:
#         seen = set()
#         curr = head
#         while curr is not None:
#             if curr in seen:        # membership is by object identity
#                 return True
#             seen.add(curr)
#             curr = curr.next
#         return False
