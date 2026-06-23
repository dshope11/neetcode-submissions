# Valid Anagram (LC 242) | Arrays & Hashing | Blind 75
# Solved 2026-06-21 on neetcode.io | outcome: solo
# Raw: Data Structures & Algorithms/is-anagram/submission-0.py
# Style notes (David's typed solution preserved as-is below):
#   - Counter_s / Counter_t: capitalized like a class; PEP 8 wants snake_case
#     (counter_s / counter_t) since these are dict variables, not types.
#   - "else: Counter_s[letter] += 1" on one line is legal but PEP 8 prefers
#     the body on its own line.
#   - The manual key-by-key compare loop collapses to a single dict equality
#     (counter_s == counter_t) once both maps are built - see Counter alt below.
#
# Optimal active below (hand-rolled freq maps, O(n) time / O(1) space for a
# fixed alphabet, O(k) for arbitrary Unicode); alternatives at the bottom.

# from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # return Counter(s) == Counter(t)
        if len(s) != len(t):
            return False
        Counter_s = {}
        for letter in s:
            if letter not in Counter_s:
                Counter_s[letter] = 1
            else: Counter_s[letter] += 1
        Counter_t = {}
        for letter in t:
            if letter not in Counter_t:
                Counter_t[letter] = 1
            else: Counter_t[letter] += 1

        for k in Counter_s:
            if k not in Counter_t:
                return False
            elif Counter_t[k] != Counter_s[k]:
                return False
        return True

        # Alternative - Counter equality: O(n) time, O(1)/O(k) space.
        # Counter.__eq__ compares multisets directly; cleanest form.
        # from collections import Counter
        # return Counter(s) == Counter(t)

        # Alternative - sort both, then compare: O(n log n) time, O(1) space
        # (if sorted in place). Alphabet-agnostic, no auxiliary map.
        # return sorted(s) == sorted(t)
