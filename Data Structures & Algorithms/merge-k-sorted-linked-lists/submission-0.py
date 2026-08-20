# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

import heapq

class Solution:    
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        enum = 0
        h = []
        for node in lists:
            if node is not None:
                heapq.heappush(h, (node.val, enum, node))
                enum += 1
        while h:
            # pop tuple with minimum value
            _, _, node = heapq.heappop(h)
            # push next value in the list if next isn't None
            if node.next is not None:
                heapq.heappush(h, (node.next.val, enum, node.next))
                enum += 1
            # splice node into return list
            tail.next = node
            tail = tail.next
        return dummy.next


