class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        last = {}
        best = 0

        for i, c in enumerate(s):
            if c in last:
                left = max(left, last[c] + 1)
            last[c] = i
            best = max(best, i - left + 1)

        return best
