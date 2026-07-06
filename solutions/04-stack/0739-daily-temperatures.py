# Daily Temperatures (LC 739) | Stack (monotonic) | NeetCode 150 (not Blind)
# Solved 2026-07-05 on neetcode.io | outcome: hint (brute force + O(n^2) reasoned
#   solo; derived the monotonic-decreasing "still-waiting" stack through leading
#   questions; needed one correction on the pop mechanics - the first-pass model
#   was "pop entries to reach the resolved ones, then push the un-resolved ones
#   back," which re-pushes and breaks the O(n) bound. Fix: CHECK BEFORE POP - peek
#   the top, pop only if it actually resolves, so each index is pushed once and
#   popped at most once. Amortized-analysis vocabulary was the other new piece.)
# Raw: Data Structures & Algorithms/daily-temperatures/submission-0.py
# Style: clean - snake_case, PascalCase class, no PEP 8 slips. dailyTemperatures /
#        temperatures are LeetCode's fixed method signature.
#
# ACTIVE CODE BELOW is the CLEANED version (agreed style-only improvements over the
# typed submission), per the /neetcode workflow. The verbatim accepted submission
# is preserved untouched as Alt 1 so the practice record stays honest. The
# algorithm is identical - the cleanups are purely surface.
#
# The canonical MONOTONIC STACK. Single left-to-right pass holding a stack of
# INDICES whose temperatures are strictly decreasing (top = most recent, coldest
# still-waiting day). O(n) time - AMORTIZED: any one day can trigger a big pop-fest
# (e.g. [45,44,43,...,100] pops everything at the end), but each index is pushed
# exactly once and popped at most once, so total push+pop work is <= 2n. O(n) space
# for the stack (worst case a strictly-decreasing input - nothing ever resolves, so
# all n indices pile up).
#
# Key idea: keep a stack of days that are still WAITING for a warmer day. Because
# it stays strictly decreasing, every day colder than an arriving day sits in one
# contiguous clump at the TOP. When day i arrives with temperature `temp`:
#   * while the stack is non-empty AND temperatures[stack[-1]] < temp: pop index j
#     (its warmer day is exactly i) and record answer[j] = i - j.
#   * stop the moment the top is NOT colder (peek, don't pop - nothing to restore),
#     then push i as the newest waiting day.
# Days never resolved keep answer[i] = 0 from the pre-filled output array.
#
# Why store INDICES, not temperatures: the index is dual-purpose - stack[-1] recovers
# the temperature (temperatures[stack[-1]]) for the comparison, AND the popped j gives
# the gap i - j. Storing temps alone loses the distance; storing (temp, index) tuples
# carries redundant data (temp is derivable from the index). Index-only is minimal.
#
# Strict `<` is load-bearing: with `<=` an equal-temperature day would wrongly count
# as "warmer" and resolve equal days. On [70,70,70] the comparison never fires, the
# stack just grows, and the answer is correctly [0, 0, 0].

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        answer = [0] * len(temperatures)

        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                j = stack.pop()
                answer[j] = i - j
            stack.append(i)

        return answer


# ---------------------------------------------------------------------------
# What changed from the typed submission (Alt 1) -> the active cleaned version
# ---------------------------------------------------------------------------
#  1. enumerate(temperatures) instead of range(len(temperatures)) - names the
#     current temperature once as `temp` and drops one of the two per-iteration
#     temperatures[i] lookups (the while-loop still indexes stack[-1], which is
#     unavoidable).
#  2. PEP 8 spacing: [0]*len(...) -> [0] * len(temperatures) (spaces around the
#     binary operator).
#  3. Stripped trailing whitespace after the while block.
#  Same algorithm, same O(n) amortized / O(n).
#
# ---------------------------------------------------------------------------
# Alternatives (commented; the active code above is the cleaned optimal)
# ---------------------------------------------------------------------------
#
# Alt 1) The accepted submission, VERBATIM as typed (the honest practice record).
#   Same monotonic-stack algorithm and same O(n) / O(n). Differences vs the cleaned
#   active code are only the three style cleanups listed above.
#
# class Solution:
#     def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
#         stack = []
#         answer = [0]*len(temperatures)
#
#         for i in range(len(temperatures)):
#             while stack and temperatures[stack[-1]] < temperatures[i]:
#                 j = stack.pop()
#                 answer[j] = i - j
#             stack.append(i)
#
#         return answer
#
# Alt 2) Brute force - the naive O(n^2) reasoned first in Phase 1. For each day,
#   scan forward until a strictly warmer day is found; record the gap and break.
#   O(n^2) time (worst case a long descending run then a spike, e.g.
#   [45,44,43,42,41,100] - every day scans the whole tail), O(1) extra space beyond
#   the output. The monotonic stack is this made incremental: instead of re-scanning
#   the tail for every day, the stack remembers the still-waiting days so each pair
#   is resolved once - collapsing O(n^2) to O(n).
#
# class Solution:
#     def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
#         n = len(temperatures)
#         answer = [0] * n
#         for i in range(n):
#             for j in range(i + 1, n):
#                 if temperatures[j] > temperatures[i]:
#                     answer[i] = j - i
#                     break
#         return answer
