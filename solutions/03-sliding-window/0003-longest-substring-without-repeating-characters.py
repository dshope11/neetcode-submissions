# Longest Substring Without Repeating Characters (LC 3) | Sliding Window | Blind 75
# Solved 2026-07-01 on neetcode.io | outcome: hint (spotted own reset bug fast via
#   the "dvdf" counterexample; needed nudges to reach the last-seen-index jump, to
#   drop a bogus O(1)-space claim, and to derive the stale-index max() guard from
#   the "abba" trace)
# Raw: Data Structures & Algorithms/longest-substring-without-duplicates/submission-0.py
# Style: clean (snake_case, no shadowing, no Unicode, PEP 8). lengthOfLongestSubstring
#        is LeetCode's fixed method signature.
#
# First TRUE sliding window in the section (unlike LC 121, which was a running-min
# sweep). Variable-size window over a contiguous run; left contracts on a repeat.
#
# Optimal active below: last-seen-index dict, one pass. O(n) time / O(m) space,
# m = alphabet size (O(1) under a fixed-alphabet assumption, e.g. 128 ASCII).
#
# Key idea: carry left, and `last` = char -> the most recent index it appeared at.
# For each right index i with char c: if c is already in the window, jump left PAST
# c's previous position. Then record the window width i - left + 1.
#
# The crux (fails submissions if missed): the jump is
#     left = max(left, last[c] + 1)
# NOT just last[c] + 1. This design never deletes from `last`, so last[c] may be a
# STALE index sitting BEHIND the current left (a duplicate already evicted). Blindly
# jumping there would move left BACKWARD and silently re-admit evicted chars. The
# max() clamps left to be monotonic (never retreats) - the invariant the window
# pattern depends on. Trace "abba": at the final 'a', last['a'] == 0 but left is
# already 2; naive rule sends left back to 1 (wrong), max() keeps it at 2.
#
# Width is i - left + 1 (inclusive both ends) - the classic off-by-one.

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


# ---------------------------------------------------------------------------
# Alternatives (commented; the verbatim accepted solution is active above)
# ---------------------------------------------------------------------------
#
# 1) Set-based expand/contract - the other canonical O(n). Instead of jumping left
#    with a last-seen index, EVICT from the left one char at a time until the
#    incoming duplicate is gone. State holds only the current window, so no stale
#    entries and no max() guard needed - but left steps rather than jumps.
#    O(n) time (each char enters/leaves once), O(m) space.
#
# class Solution:
#     def lengthOfLongestSubstring(self, s: str) -> int:
#         seen = set()
#         left = 0
#         best = 0
#         for right in range(len(s)):
#             while s[right] in seen:
#                 seen.remove(s[left])
#                 left += 1
#             seen.add(s[right])
#             best = max(best, right - left + 1)
#         return best
#
# 2) Brute force - every substring via two indices, break the inner extension on
#    the first repeat using an incremental set. O(n^2) time, O(m) space. Correct
#    baseline; times out on large inputs.
#
# class Solution:
#     def lengthOfLongestSubstring(self, s: str) -> int:
#         best = 0
#         for i in range(len(s)):
#             seen = set()
#             for j in range(i, len(s)):
#                 if s[j] in seen:
#                     break
#                 seen.add(s[j])
#                 best = max(best, j - i + 1)
#         return best
