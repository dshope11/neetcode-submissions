
import heapq


class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []
        for i, num in enumerate(nums):
            if i <= k-1:
                heapq.heappush(self.heap, num)
            else:
                heapq.heappushpop(self.heap, num)
        return

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        else:
            heapq.heappushpop(self.heap, val)
        return self.heap[0]