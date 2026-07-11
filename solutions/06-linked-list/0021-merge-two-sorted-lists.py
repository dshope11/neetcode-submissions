# Merge Two Sorted Lists - LC 21 - Easy - [Blind 75]
# Pattern: Linked List (dummy / sentinel node + splice existing nodes -
#          the load-bearing companion move of the fast-slow-pointers section)
# Solved 2026-07-11 | outcome: hint
#
# Raw: Data Structures & Algorithms/merge-two-sorted-linked-lists/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was already optimal in shape; only the tail-advance idiom was
# normalized. David's verbatim accepted submission is preserved as Alt 1.
#
# Definition for singly-linked list:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()          # sentinel: absorbs the "first node is special" case
        tail = dummy
        curr_1 = list1
        curr_2 = list2

        while curr_1 and curr_2:        # both non-None inside the loop -> no None-guarding
            if curr_1.val <= curr_2.val:    # <= makes this a STABLE merge (list1 wins ties)
                tail.next = curr_1          # splice the existing node (no new allocation)
                curr_1 = curr_1.next
            else:
                tail.next = curr_2
                curr_2 = curr_2.next
            tail = tail.next            # advance the tail one step

        tail.next = curr_1 or curr_2    # attach the leftover chain in ONE splice
        return dummy.next               # real head, whatever it turned out to be


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Style-only normalization; logic is identical.
#   - Tail advance `tail = curr_1` / `tail = curr_2` (two branch-local lines)
#     -> a single `tail = tail.next` after the if/else. Same effect (tail.next
#     was just set to the chosen node), but reads as "advance the tail" and
#     collapses two lines into one shared line. No convention slips in the
#     typed version to fix (snake_case, no Unicode, PEP 8 all clean).
#
# Key insight - the two moves that make this O(1) space and branch-free:
#   1. SPLICE, don't allocate: `tail.next = curr_1` re-points at the existing
#      input node instead of building a fresh one -> O(1) space, not O(n).
#   2. Leftover attach is ONE assignment, not a loop: when the main loop exits,
#      the remaining nodes are already a sorted linked chain, so pointing
#      tail.next at its head drags the whole tail along. `curr_1 or curr_2`
#      returns whichever is non-None (a ListNode is truthy), or None if both
#      are exhausted - which also makes both-empty and one-empty inputs fall
#      out with zero special-case code.
#
# `or`-idiom caveat: `tail.next = curr_1 or curr_2` is only safe because a
# valid value here (a ListNode) is never falsy. It would silently drop a
# legitimate 0 / "" / empty value - the falsy-value footgun on the prep hub.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n + m) time, O(1) space
# ---------------------------------------------------------------------------
# class Solution:
#     def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
#         dummy = ListNode()
#         tail = dummy
#         curr_1 = list1
#         curr_2 = list2
#
#         while curr_1 and curr_2:
#             if curr_1.val <= curr_2.val:
#                 tail.next = curr_1
#                 tail = curr_1
#                 curr_1 = curr_1.next
#             else:
#                 tail.next = curr_2
#                 tail = curr_2
#                 curr_2 = curr_2.next
#
#         tail.next = curr_1 or curr_2
#         return dummy.next


# ---------------------------------------------------------------------------
# Alt 2: same splice, explicit-branch leftover attach - O(n + m) time, O(1) space
#        The single-loop shape David reached mid-discussion before collapsing
#        the leftover into one line. Correct, just more verbose: the two if
#        blocks below are exactly what `tail.next = curr_1 or curr_2` replaces.
# ---------------------------------------------------------------------------
# class Solution:
#     def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
#         dummy = ListNode()
#         tail = dummy
#         curr_1, curr_2 = list1, list2
#         while curr_1 and curr_2:
#             if curr_1.val <= curr_2.val:
#                 tail.next = curr_1
#                 curr_1 = curr_1.next
#             else:
#                 tail.next = curr_2
#                 curr_2 = curr_2.next
#             tail = tail.next
#         if curr_1 is not None:
#             tail.next = curr_1
#         else:
#             tail.next = curr_2
#         return dummy.next


# ---------------------------------------------------------------------------
# Alt 3: allocate a new list (David's first-instinct approach) - O(n+m) time,
#        O(n+m) SPACE. Copies each value into a fresh node instead of reusing
#        the inputs. Correct, but the extra allocation is exactly why the
#        splice version is preferred. Kept as the "does the output count as
#        space?" contrast. (Shown here already de-bugged: the original sketch
#        also had the leftover-tail-drop bug from an outer/inner nested loop.)
# ---------------------------------------------------------------------------
# class Solution:
#     def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
#         dummy = ListNode()
#         tail = dummy
#         curr_1, curr_2 = list1, list2
#         while curr_1 and curr_2:
#             if curr_1.val <= curr_2.val:
#                 tail.next = ListNode(curr_1.val)   # fresh node = the O(n) space cost
#                 curr_1 = curr_1.next
#             else:
#                 tail.next = ListNode(curr_2.val)
#                 curr_2 = curr_2.next
#             tail = tail.next
#         rest = curr_1 or curr_2
#         while rest is not None:
#             tail.next = ListNode(rest.val)
#             tail = tail.next
#             rest = rest.next
#         return dummy.next
