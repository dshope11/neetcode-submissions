# Valid Palindrome (LC 125) | Two Pointers | Blind 75
# Solved 2026-06-27 on neetcode.io | outcome: solo
# Raw: Data Structures & Algorithms/is-palindrome/submission-0.py
# Style: clean (snake_case, no Unicode, PEP 8). isPalindrome is LeetCode's
#        fixed method signature, not a naming choice.
#
# Optimal active below: converging two pointers, O(n) time / O(1) space.
#
# Key idea: don't pre-clean the string (that costs O(n) space) - keep the
# punctuation in place and SKIP it with the pointers. left starts at 0, right at
# len-1; converge while left < right.
#
# The branch ORDER is load-bearing: both non-alphanumeric skips come BEFORE the
# comparison, so you never compare a junk char. Each iteration fires exactly one
# branch (advance left / retreat right / match-advance-both / mismatch-return),
# and `while left < right` is re-checked every iteration - that single condition
# is the entire bounds guard, so no separate skip-loop guard is needed (all-junk
# input like ",.;!" just walks the pointers together and returns True).
#
# Why O(n) not O(n^2): the two pointers only ever move toward each other, so
# their combined travel is bounded by n - each index is visited at most once.
# O(1) space: no auxiliary structure, everything is index arithmetic in place.
#
# Edge cases (all fall out, no special-casing): "" -> True (0 < -1 false);
# single char -> True (0 < 0 false); all-punctuation -> True.

class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1
        while left < right:
            if not s[left].isalnum():
                left += 1
            elif not s[right].isalnum():
                right -= 1
            elif s[left].lower() == s[right].lower():
                left += 1
                right -= 1
            else:
                # not a palindrome
                return False
        # is a palindrome
        return True

# Alternative - two pointers with inner while-loop skips (NeetCode's canonical
# form): O(n) time, O(1) space. Same idea, different control flow - instead of
# one if/elif branch per outer iteration, each outer pass fully advances past
# junk via two inner while-loops, then compares once. Critical difference: each
# inner skip loop needs its OWN `l < r` guard, or it runs off the end on
# all-punctuation input - the bounds safety the active version got for free from
# its single outer condition. (NeetCode often hand-rolls an `alphanum` helper
# instead of str.isalnum(); isalnum() is used here for parity with the active.)
# def isPalindrome(self, s):
#     l, r = 0, len(s) - 1
#     while l < r:
#         while l < r and not s[l].isalnum():   # own bounds guard required
#             l += 1
#         while l < r and not s[r].isalnum():   # own bounds guard required
#             r -= 1
#         if s[l].lower() != s[r].lower():
#             return False
#         l += 1
#         r -= 1
#     return True
#
# Alternative - build cleaned string, compare to its reverse: O(n) time, O(n)
# space. Filter to lowercased alphanumerics in one pass, then check it equals its
# reverse. Simplest to write, but the O(n) extra space loses the follow-up; the
# two-pointer version above is the O(1)-space answer. (Building a separate
# "backward" string with a second loop is wasteful - just reverse the cleaned
# one.)
# def isPalindrome(self, s):
#     cleaned = [c.lower() for c in s if c.isalnum()]
#     return cleaned == cleaned[::-1]
