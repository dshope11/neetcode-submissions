class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""

        t_count = {}
        window_count = {}

        for c in t:
            t_count[c] = t_count.get(c, 0) + 1

        threshold = 0

        smallest_size = float("inf")

        left_shortest_valid = 0
        right_shortest_valid = 0

        left = 0
        right = 0

        for right in range(len(s)):
            right_match_prior = window_count.get(s[right],0) >= t_count.get(s[right],0)
            window_count[s[right]] = window_count.get(s[right],0) + 1
            if s[right] in t_count and window_count.get(s[right],0) >= t_count.get(s[right],0) and not right_match_prior:
                threshold += 1
            
            window_valid = threshold == len(t_count)

            while window_valid:
                if right - left + 1 < smallest_size:
                    smallest_size = right - left + 1
                    left_shortest_valid = left
                    right_shortest_valid = right
                window_count[s[left]] = window_count.get(s[left],0) - 1
                if s[left] in t_count and window_count.get(s[left],0) < t_count.get(s[left],0):
                    threshold -= 1
                left += 1
                window_valid = threshold == len(t_count)

        if smallest_size == float("inf"):
            return ""
        else:
            shortest_valid = s[left_shortest_valid:right_shortest_valid + 1]
            return shortest_valid
        