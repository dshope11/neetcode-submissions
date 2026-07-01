# Best Time to Buy and Sell Stock (LC 121) | Sliding Window | Blind 75
# Solved 2026-07-01 on neetcode.io | outcome: hint (brute force + the
#   "best buy for a fixed sell = min so far" insight came fairly readily; needed a
#   nudge to name the second running variable, max_profit, and to reason through
#   why the update order is correctness-neutral)
# Raw: Data Structures & Algorithms/buy-and-sell-crypto/submission-0.py
# Style: clean (snake_case, no shadowing, no Unicode, PEP 8). maxProfit is
#        LeetCode's fixed method signature.
#
# Filing note: NeetCode files this under Sliding Window, but it is really a
# single-pass RUNNING-MINIMUM sweep, not an expand/contract window - there is no
# left pointer that contracts. The kinship to sliding window is only that both
# carry incremental O(1) state across one left-to-right pass.
#
# Optimal active below: one pass, O(n) time / O(1) space.
#
# Key idea: fix the SELL day; the best BUY for it is the cheapest price seen on any
# EARLIER day. So sweep once, carry min_so_far (cheapest price to date) and
# max_profit (best spread to date). At each price: candidate profit = price -
# min_so_far, and max_profit = max(max_profit, candidate). O(n) is the floor - you
# must read every price at least once, so no algorithm beats a single pass.
#
# Update-order subtlety (interview talking point): updating min_so_far BEFORE
# computing the candidate means a new-minimum day yields candidate == 0; computing
# the candidate against the OLD min first would yield a negative candidate on such
# a day. Neither is buggy: max_profit is initialized to 0 and only grows via max(),
# so the 0 floor absorbs both. Order is correctness-neutral here.
#
# Dead-code note on the trailing guard: because max_profit starts at 0 and only
# ever grows via max(), AND min is updated first (so candidate >= 0 always), the
# `if max_profit < 0` branch can never fire - the whole if/else reduces to
# `return max_profit`. Preserved verbatim as typed.

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_so_far = float("inf")
        max_profit = 0

        for price in prices:
            min_so_far = min(min_so_far, price)
            max_profit = max(max_profit, price - min_so_far)

        if max_profit < 0:
            return 0
        else:
            return max_profit


# ---------------------------------------------------------------------------
# Alternatives (commented; the verbatim accepted solution is active above)
# ---------------------------------------------------------------------------
#
# 1) Brute force - every (buy, sell) pair with buy before sell:
#    O(n^2) time, O(1) space. Correct but times out on large inputs.
#
# class Solution:
#     def maxProfit(self, prices: List[int]) -> int:
#         max_profit = 0
#         for i in range(len(prices)):
#             for j in range(i + 1, len(prices)):
#                 max_profit = max(max_profit, prices[j] - prices[i])
#         return max_profit
#
# 2) Micro-optimized one pass - same O(n) / O(1), smaller constant factor.
#    Replaces the two builtin min()/max() calls (a function call each, per
#    iteration) with plain comparisons. The elif is the trick: if price is a new
#    minimum, its profit-against-itself is 0 and can never beat max_profit, so the
#    second check is skipped on min-days. This is roughly what LeetCode's fastest
#    bucket does - a constant-factor win only, NOT an asymptotic one (everyone here
#    is O(n)). Chase this only for hot-path production code, never in an interview.
#
# class Solution:
#     def maxProfit(self, prices: List[int]) -> int:
#         min_so_far = float("inf")
#         max_profit = 0
#         for price in prices:
#             if price < min_so_far:
#                 min_so_far = price
#             elif price - min_so_far > max_profit:
#                 max_profit = price - min_so_far
#         return max_profit
