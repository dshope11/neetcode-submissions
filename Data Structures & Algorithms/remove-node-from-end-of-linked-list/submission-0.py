# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode()
        dummy.next = head
        first = second = dummy
        iter = 0

        while first:
            if iter < n + 1:
                first = first.next
                iter += 1
            else:
                first = first.next
                second = second.next

        second.next = second.next.next

        return dummy.next