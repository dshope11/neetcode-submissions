
import heapq

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []
        result = []
        for i, point in enumerate(points):
            dist = math.sqrt(point[0]*point[0] + point[1]*point[1])
            heapq.heappush(heap, (dist, i, point))
        for i in range(k):
            _, _, point = heapq.heappop(heap)
            result.append(point)
        return result