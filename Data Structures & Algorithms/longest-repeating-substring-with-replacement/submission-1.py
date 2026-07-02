class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        max_freq = 0
        count = collections.defaultdict(int)
        left = 0
        right = 0
        best = 0

        for c in s:

            count[c] += 1

            # recalculate max_freq
            max_freq = max(count.values())

            window_length = right - left + 1

            # contract to remain a valid window
            if window_length - max_freq > k:
                count[s[left]] -= 1
                left += 1

            # calculate best from valid window
            best = max(best, right - left + 1)

            # expand window for next iteration
            right += 1

        return best