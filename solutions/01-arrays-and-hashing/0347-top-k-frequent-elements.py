# Top K Frequent Elements (LC 347) | Arrays & Hashing | Blind 75
# Solved 2026-06-24 on neetcode.io | outcome: solo
# Raw: Data Structures & Algorithms/top-k-elements-in-list/submission-0.py
# Style: clean (snake_case, PEP 8 OK)
#
# Optimal active below (bucket sort by frequency, O(n) time / O(n) space - no
# log, no *k factor); alternatives commented at the bottom.
#
# Key idea: a count can only be in [1, n], so index an array BY frequency and
# sweep from the high end - no comparison sort or heap needed. Uniqueness
# guarantee means the k-th boundary is never an ambiguous tie.

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        freq = [[] for _ in range(len(nums) + 1)]

        for num in nums:
            count[num] = 1 + count.get(num, 0)
        for num, cnt in count.items():
            freq[cnt].append(num)

        res = []
        # Example of looping backward
        for i in range(len(freq) - 1, 0, -1):
            for num in freq[i]:
                res.append(num)
                if len(res) == k:
                    return res

        # Alternative - min-heap of size k: O(n + m log k) time, O(n) space
        # (m = number of unique values). Better than sorting when k << m; the
        # heap keeps the weakest of the current top-k at the root (O(1) peek,
        # O(log k) pop/push). This is also what Counter(nums).most_common(k)
        # does internally (heapq.nlargest).
        # import heapq
        # from collections import Counter
        # count = Counter(nums)
        # heap = []
        # for num, cnt in count.items():
        #     heapq.heappush(heap, (cnt, num))
        #     if len(heap) > k:
        #         heapq.heappop(heap)
        # return [num for cnt, num in heap]

        # Alternative - sort the pairs by frequency: O(n + m log m) time,
        # O(n) space. The plain comparison-sort baseline.
        # from collections import Counter
        # count = Counter(nums)
        # ordered = sorted(count.items(), key=lambda p: p[1], reverse=True)
        # return [num for num, cnt in ordered[:k]]
