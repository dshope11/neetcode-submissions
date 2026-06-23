class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Hand-rolled frequency maps: O(n) time, O(1) space (fixed 26-letter
        # alphabet; O(k) for arbitrary Unicode). Length guard is a cheap bail.
        if len(s) != len(t):
            return False
        count_s = {}
        for letter in s:
            count_s[letter] = count_s.get(letter, 0) + 1
        count_t = {}
        for letter in t:
            count_t[letter] = count_t.get(letter, 0) + 1
        return count_s == count_t

        # Alternative - Counter equality: O(n) time, O(1)/O(k) space.
        # Counter.__eq__ compares multisets directly; cleanest form.
        # from collections import Counter
        # return Counter(s) == Counter(t)

        # Alternative - sort both, then compare: O(n log n) time, O(1) space
        # (if sorted in place). Alphabet-agnostic, no auxiliary map.
        # return sorted(s) == sorted(t)
