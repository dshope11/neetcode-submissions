# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        # Find midpoint and split lists
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None
        # Reverse second
        prev = None
        curr = second
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        first = head
        second = prev
        # Weave first and (reversed) second
        dummy = ListNode()
        tail = dummy
        curr_1 = first
        curr_2 = second
        while curr_2:
            curr_1_nxt = curr_1.next
            curr_2_nxt = curr_2.next
            tail.next = curr_1
            tail = curr_1
            tail.next = curr_2
            tail = curr_2
            curr_1 = curr_1_nxt
            curr_2 = curr_2_nxt
        tail.next = curr_1
        return None

