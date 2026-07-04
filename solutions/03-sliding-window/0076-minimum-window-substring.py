# Minimum Window Substring (LC 76) | Sliding Window | Blind 75
# Solved 2026-07-04 on neetcode.io | outcome: hint (approach reasoned solo -
#   variable expand/contract window, have/need coverage counter, >= (not ==)
#   because the window may carry extra chars, record-before-contract for a
#   SHORTEST window; needed three debugging nudges, all in the loop scaffold:
#   (a) an improvised single-move if/else expand loop that skipped s[1] and let
#   `right` run ahead of the window - fixed by switching to the canonical
#   `for right in range(len(s))` shape; (b) a window that turned valid on the
#   final expansion was never recorded because validity was only tested at the
#   top of the loop; (c) an index-based empty-result sentinel
#   (`left == 0 and right == 0`) that collided with a real answer at index 0 -
#   fixed with the `smallest_size == inf` sentinel)
# Raw: Data Structures & Algorithms/minimum-window-with-characters/submission-1.py
# Style: clean - snake_case throughout, PascalCase class, no PEP 8 slips.
#
# ACTIVE CODE BELOW is the CLEANED version (agreed improvements over the typed
# submission), per the /neetcode workflow. The verbatim accepted submission is
# preserved untouched as Alt 1 so the practice record stays honest.
#
# Variable-size expand/contract window. O(|s| + |t|) time - each char enters the
# window once and leaves at most once. O(1) space for a bounded alphabet (strictly
# O(k), k = distinct chars in t; the counts never exceed the alphabet size).
#
# Key idea: grow the window with `right`; the moment it COVERS t (has >= the
# required count of every char of t), it is valid - record it, then greedily
# shrink from the `left` while it stays valid to find the shortest such window,
# and repeat. Coverage is tracked in O(1) per step with a have/need counter:
#   need = number of distinct chars in t
#   have = number of those chars whose window count has REACHED its target
# valid iff have == need. Because window_count moves by exactly +/-1 per step, a
# char crosses its target exactly when window_count[c] == t_count[c] on an add
# (have += 1) and drops below it when window_count[c] < t_count[c] on a removal
# (have -= 1) - so the crossing is detected with a single equality/inequality, no
# before/after snapshot needed.
#
# Two things this problem hinges on:
#   * SHORTEST -> record the answer INSIDE the shrink loop, BEFORE contracting
#     (contrast a LONGEST problem, which records after the while-loop once valid).
#   * >= vs == vs 567: LC 567's fixed window needed an EXACT anagram (== on the
#     whole map). Here the window may be longer and hold junk, so validity is
#     "covers t" (>=). We still detect the have-counter crossing with ==, but that
#     == is the +/-1 step crossing its target, not a whole-map equality.

from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""

        t_count = Counter(t)
        window_count = Counter()
        need = len(t_count)          # distinct chars that must be covered
        have = 0                     # distinct chars currently satisfied

        best_len = float("inf")
        best_left, best_right = 0, 0

        left = 0
        for right in range(len(s)):
            c = s[right]
            window_count[c] += 1
            if c in t_count and window_count[c] == t_count[c]:
                have += 1

            while have == need:                     # valid: record, THEN shrink
                if right - left + 1 < best_len:
                    best_len = right - left + 1
                    best_left, best_right = left, right
                lc = s[left]
                window_count[lc] -= 1
                if lc in t_count and window_count[lc] < t_count[lc]:
                    have -= 1
                left += 1

        return "" if best_len == float("inf") else s[best_left:best_right + 1]


# ---------------------------------------------------------------------------
# What changed from the typed submission (Alt 1) -> the active cleaned version
# ---------------------------------------------------------------------------
#  1. Dropped `right_match_prior` + the `>= ... and not ...` compound toggle.
#     window_count only changes by 1, so a char crosses its target EXACTLY when
#     window_count[c] == t_count[c] (add) / drops below it (remove). One line each,
#     no snapshot variable.
#  2. `Counter` instead of plain dicts + `.get(x, 0)` everywhere: `t_count =
#     Counter(t)` is the whole build loop; a Counter reads a missing key as 0
#     without inserting, so `window_count[c]` needs no `.get` guard (~6 removed).
#  3. Renamed `threshold` -> `have` and `len(t_count)` -> `need`: the have/need
#     vocabulary is the canonical reading of this problem.
#  4. Removed the dead pre-loop `right = 0` (rebound immediately by the for-loop).
#  5. Inlined the `window_valid` variable into `while have == need`.
#  Same algorithm, same O(|s| + |t|) / O(1); ~8 fewer lines and it reads canonical.
#
# ---------------------------------------------------------------------------
# Alternatives (commented; the active code above is the cleaned optimal)
# ---------------------------------------------------------------------------
#
# Alt 1) The accepted submission, VERBATIM as typed (the honest practice record).
#   Same variable expand/contract window and same O(|s| + |t|) / O(1). Differences
#   vs the cleaned active code are purely the five cleanups listed above:
#   `threshold` naming, plain-dict `.get(x, 0)`, and the `right_match_prior` + `>=`
#   toggle instead of the exact `==` crossing.
#
# class Solution:
#     def minWindow(self, s: str, t: str) -> str:
#         if len(s) < len(t):
#             return ""
#
#         t_count = {}
#         window_count = {}
#
#         for c in t:
#             t_count[c] = t_count.get(c, 0) + 1
#
#         threshold = 0
#         smallest_size = float("inf")
#         left_shortest_valid = 0
#         right_shortest_valid = 0
#         left = 0
#         right = 0
#
#         for right in range(len(s)):
#             right_match_prior = window_count.get(s[right],0) >= t_count.get(s[right],0)
#             window_count[s[right]] = window_count.get(s[right],0) + 1
#             if s[right] in t_count and window_count.get(s[right],0) >= t_count.get(s[right],0) and not right_match_prior:
#                 threshold += 1
#
#             window_valid = threshold == len(t_count)
#
#             while window_valid:
#                 if right - left + 1 < smallest_size:
#                     smallest_size = right - left + 1
#                     left_shortest_valid = left
#                     right_shortest_valid = right
#                 window_count[s[left]] = window_count.get(s[left],0) - 1
#                 if s[left] in t_count and window_count.get(s[left],0) < t_count.get(s[left],0):
#                     threshold -= 1
#                 left += 1
#                 window_valid = threshold == len(t_count)
#
#         if smallest_size == float("inf"):
#             return ""
#         else:
#             shortest_valid = s[left_shortest_valid:right_shortest_valid + 1]
#             return shortest_valid
#
# Alt 2) Brute force - the naive "check every substring" reasoned in Phase 1.
#   For each start i, sweep the end j forward, adding chars to a window Counter;
#   the moment the window covers t, this is the shortest window starting at i
#   (extending j only grows it), so record and break to the next start. The
#   coverage test `all(window[c] >= t_count[c] for c in t_count)` is O(k) per step.
#   O(n^2 * k) time (O(n^2) treating the alphabet k as constant), O(k) space. The
#   active window is exactly this with the O(k) per-step coverage rebuild replaced
#   by the incremental have/need counter and the two-pointer sweep folded into one
#   left-to-right pass - collapsing O(n^2) to O(n).
#
# class Solution:
#     def minWindow(self, s: str, t: str) -> str:
#         if len(s) < len(t):
#             return ""
#         t_count = Counter(t)
#         best = ""
#         for i in range(len(s)):
#             window = Counter()
#             for j in range(i, len(s)):
#                 window[s[j]] += 1
#                 if all(window[c] >= t_count[c] for c in t_count):
#                     if best == "" or j - i + 1 < len(best):
#                         best = s[i:j + 1]
#                     break        # shortest window starting at i - stop extending
#         return best
