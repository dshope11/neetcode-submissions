# Permutation in String (LC 567) | Sliding Window | NeetCode 150 (not Blind 75)
# Solved 2026-07-02 on neetcode.io | outcome: hint (approach reasoned solo -
#   fixed-window freq counts, length early-bail, O(1)-per-slide matches counter,
#   matches init to 26-distinct(s1); needed two debugging nudges on the
#   implementation: (a) removed the wrong element on the slide - incremented left
#   before removing so index 0 orphaned in the window, and (b) never checked the
#   FIRST full window - the match-check was nested under `right >= len(s1)` instead
#   of `right >= len(s1) - 1`)
# Raw: Data Structures & Algorithms/permutation-string/submission-2.py
#   (submission-1 was an earlier failing attempt; submission-2 is the accepted one)
# Style: clean - snake_case throughout, PascalCase class, no PEP 8 slips.
#
# Fixed-size frequency-map window. O(n) time / O(1) space (two 26-entry count
# arrays over a fixed lowercase alphabet).
#
# Key idea: s2 contains a permutation of s1 iff some length-len(s1) window of s2 has
# the exact same character counts as s1. Slide a fixed width-len(s1) window across
# s2; the naive check "do the two count maps match?" is O(26) per slide (O(26*n)
# total). The O(1)-per-slide upgrade: carry `matches` = how many of the 26 letters
# currently have window_count == s1_count. Each slide mutates exactly two slots
# (one enters on the right, one leaves on the left), so `matches` is fixed up in
# O(1) around each single mutation instead of rescanning all 26.
#
# Two subtleties this problem hinges on:
#   * matches INIT = s1_count.count(0): every letter absent from s1 (count 0) already
#     agrees with the empty starting window, so it starts matched. Off-by-this and
#     matches can never reach 26. (Empty-window start: the first len(s1) chars go
#     through the same enter-mutation as every other char - they just don't trigger
#     a removal yet.)
#   * the window is full for right in [len(s1)-1 .. len(s2)-1] but a removal only
#     happens for right >= len(s1). Those are DIFFERENT boundaries, so the
#     `matches == 26` check must be gated on `right >= len(s1) - 1`, independent of
#     the removal branch - otherwise window #0 is never tested.

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:

        if len(s1) > len(s2):
            return False

        s1_count = [0]*26
        window_count = [0]*26

        for c in s1:
            s1_count[ord(c) - ord('a')] += 1

        matches = s1_count.count(0)

        left = 0

        for right, c in enumerate(s2):
            c_match_prior = s1_count[ord(c) - ord('a')] == window_count[ord(c) - ord('a')]
            window_count[ord(c) - ord('a')] += 1
            if s1_count[ord(c) - ord('a')] == window_count[ord(c) - ord('a')] and not c_match_prior:
                matches += 1
            elif s1_count[ord(c) - ord('a')] != window_count[ord(c) - ord('a')] and c_match_prior:
                matches -= 1

            if right >= len(s1):
                left_match_prior = s1_count[ord(s2[left]) - ord('a')] == window_count[ord(s2[left]) - ord('a')]
                window_count[ord(s2[left]) - ord('a')] -= 1
                if s1_count[ord(s2[left]) - ord('a')] == window_count[ord(s2[left]) - ord('a')] and not left_match_prior:
                    matches += 1
                elif s1_count[ord(s2[left]) - ord('a')] != window_count[ord(s2[left]) - ord('a')] and left_match_prior:
                    matches -= 1

                left += 1

            if right >= len(s1) - 1 and matches == 26:
                return True

        return False


# ---------------------------------------------------------------------------
# Alternatives (commented; the verbatim accepted solution is active above)
# ---------------------------------------------------------------------------
#
# 1) Cleaned version of the accepted approach (agreed cleanups 1+2+3, same
#    O(n) time / O(1) space). Three simplifications:
#      * extract the alphabet index once per char (i / j) instead of recomputing
#        `ord(c) - ord('a')` ~5x per block - kills the visual noise;
#      * factor the duplicated enter/leave "matches" bookkeeping into one helper.
#        The `after - before` bool-subtraction collapses the whole if/elif to one
#        line: True-False=+1 (newly matched), False-True=-1 (newly broken), else 0;
#      * drop the separate `left` pointer - it always trails right by exactly
#        len(s1), so the departing char is just s2[right - len(s1)].
#
# class Solution:
#     def checkInclusion(self, s1: str, s2: str) -> bool:
#         if len(s1) > len(s2):
#             return False
#
#         s1_count = [0]*26
#         window_count = [0]*26
#         for c in s1:
#             s1_count[ord(c) - ord('a')] += 1
#
#         matches = s1_count.count(0)
#
#         def apply(idx, delta):                       # delta = +1 enter, -1 leave
#             nonlocal matches
#             before = window_count[idx] == s1_count[idx]
#             window_count[idx] += delta
#             after = window_count[idx] == s1_count[idx]
#             matches += after - before                # -1 / 0 / +1
#
#         for right, c in enumerate(s2):
#             apply(ord(c) - ord('a'), 1)              # char enters on the right
#             if right >= len(s1):                     # char leaves on the left
#                 apply(ord(s2[right - len(s1)]) - ord('a'), -1)
#             if right >= len(s1) - 1 and matches == 26:
#                 return True
#         return False
#
# 2) Whole-map compare per slide - the more obvious approach, no `matches` counter.
#    Maintain the window count and just test `window_count == s1_count` each slide.
#    Simpler to write and reason about, but that equality is an O(26) scan every
#    step -> O(26*n) time (still O(n) for a fixed alphabet, but with the constant
#    factor the `matches` trick removes). O(1) space. Using arrays makes `==` a
#    clean elementwise compare; with dicts, pre-seed all 26 keys (or use Counter,
#    whose == treats a missing key and a zero count as equal) so a count that
#    decremented to 0 doesn't spuriously differ from an absent key.
#
# class Solution:
#     def checkInclusion(self, s1: str, s2: str) -> bool:
#         if len(s1) > len(s2):
#             return False
#         s1_count = [0]*26
#         window_count = [0]*26
#         for c in s1:
#             s1_count[ord(c) - ord('a')] += 1
#         for right, c in enumerate(s2):
#             window_count[ord(c) - ord('a')] += 1
#             if right >= len(s1):
#                 window_count[ord(s2[right - len(s1)]) - ord('a')] -= 1
#             if right >= len(s1) - 1 and window_count == s1_count:
#                 return True
#         return False
#
# 3) Brute force - for each of the ~n windows of width len(s1), build its count map
#    from scratch and compare to s1's. O(n * len(s1)) = O(n^2) worst case time,
#    O(1) space. The fixed-window slide (alt 2) is this with the per-window rebuild
#    replaced by an incremental add/remove; the matches counter (active) then also
#    removes the per-step compare.
