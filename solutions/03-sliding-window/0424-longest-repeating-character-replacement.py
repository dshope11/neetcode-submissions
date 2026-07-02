# Longest Repeating Character Replacement (LC 424) | Sliding Window | Blind 75
# Solved 2026-07-01 on neetcode.io | outcome: hint (nailed the validity formula
#   fast; needed the misread corrected - "one distinct char", not "all distinct" -
#   and guidance on if-vs-while contract and the stale-max_freq follow-up)
# Raw: Data Structures & Algorithms/longest-repeating-substring-with-replacement/submission-0.py
#   (submitted twice by accident; submission-0 and submission-1 are byte-identical)
# Active code note: condensed from the raw submission at David's request - the
#   original maintained a manual `right` counter (`right = 0` + `right += 1`) in
#   parallel with `for c in s`; here that is folded into `for right, c in
#   enumerate(s)` (one source of truth, no drift risk). The byte-verbatim typed
#   version lives in the raw zone at the `# Raw:` path above, so the practice
#   record stays honest. `collections.defaultdict` relies on neetcode/LeetCode's
#   implicit import of `collections` (same env that provides `List`).
#   characterReplacement is the fixed method signature.
#
# Variable-size frequency-map window. O(26*n) = O(n) time / O(1) space (<=26-entry
# count map, fixed uppercase alphabet).
#
# Key idea: a window can be made all-one-letter with <= k replacements iff
#     window_length - (count of the most frequent char) <= k
# i.e. replacements_needed = everything that ISN'T the majority char. Expand right,
# maintain per-char counts; when window_length - max_freq > k the window is invalid,
# so contract left by one. best = longest valid window seen.
#
# Why a single `if` contract suffices here (not a `while`): once valid, adding one
# char raises window_length by 1 and max_freq by at most 1, so validity can be
# violated by at most 1 - one removal restores it. (Standing rule is default to
# `while`; this problem is a documented exception where `if` is safe.) Correctness
# also leans on the fact that `best` only advances on genuinely-valid (expanding)
# steps, so a contract step never overcounts.
#
# This is the ACCURATE-RECOMPUTE variant: max_freq = max(count.values()) every
# iteration, an O(26) scan -> the O(26) factor. The stale-max_freq trick (alt #1
# below) drops that factor and is flagged in the research backlog to revisit.

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        max_freq = 0
        count = collections.defaultdict(int)
        left = 0
        best = 0

        for right, c in enumerate(s):
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

        return best


# ---------------------------------------------------------------------------
# Alternatives (commented; the verbatim accepted solution is active above)
# ---------------------------------------------------------------------------
#
# 1) Stale-max_freq slide - the canonical O(n) (no O(26) factor). NEVER recompute
#    or decrement max_freq: only let it grow. With an `if` contract the window then
#    never shrinks, only slides. Why a too-high (stale) max_freq is safe: the
#    validity test is merely too lenient, so the window can only COAST at its
#    current size, never grow past a size that was legitimately valid earlier - and
#    `best` only advances when the window grows. O(n) time, O(1) space.
#    (Correctness argument flagged in research-backlog to internalize.)
#
# class Solution:
#     def characterReplacement(self, s: str, k: int) -> int:
#         count = collections.defaultdict(int)
#         left = 0
#         max_freq = 0
#         best = 0
#         for right in range(len(s)):
#             count[s[right]] += 1
#             max_freq = max(max_freq, count[s[right]])   # never decreases
#             if (right - left + 1) - max_freq > k:       # window invalid
#                 count[s[left]] -= 1
#                 left += 1
#             best = max(best, right - left + 1)
#         return best
#
# 2) Brute force - every substring via two indices; valid iff
#    len - max_freq <= k; break the inner loop once invalid (len - max_freq is
#    monotonically non-decreasing as the window grows). O(n^2) time, O(1) space.
#
# class Solution:
#     def characterReplacement(self, s: str, k: int) -> int:
#         best = 0
#         for i in range(len(s)):
#             count = collections.defaultdict(int)
#             for j in range(i, len(s)):
#                 count[s[j]] += 1
#                 window_length = j - i + 1
#                 if window_length - max(count.values()) > k:
#                     break
#                 best = max(best, window_length)
#         return best
