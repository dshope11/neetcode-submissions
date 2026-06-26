# Product of Array Except Self (LC 238) | Arrays & Hashing | Blind 75
# Solved 2026-06-26 on neetcode.io | outcome: solo
# Raw: Data Structures & Algorithms/products-of-array-discluding-self/submission-0.py
# Style: clean (snake_case, no Unicode). Nits: redundant parens in
#        `[1] * (len(nums))` and `range((len(nums)))`; "postfix" is fine but
#        "suffix" is the more standard term. Left verbatim; not fixed here.
#
# Optimal active below: prefix/suffix products, O(n) time / O(1) extra space
# (the output array does not count as extra space).
#
# Key idea: answer[i] = (product of everything LEFT of i) * (product of
# everything RIGHT of i). No division, so a zero in the input needs no
# special-casing - at a zero's own index neither the prefix nor the suffix
# includes it, so you get the true product of the rest; at any other index the
# zero multiplies in naturally. (Division would compute 0/0 at the zero's
# position - the exact case it can't handle.)
#
# Two passes, output array reused as scratch:
#   Pass 1 (L->R): res[i] = running_prefix (ASSIGN), then running_prefix *= nums[i].
#   Pass 2 (R->L): res[i] *= running_suffix, then running_suffix *= nums[i].
#   Order in pass 2 matters: multiply BEFORE updating so nums[i] is never folded
#   into its own answer.
#
# Subtle: pass 1 ASSIGNS res[i] (not *=), so the [1]*n init value is irrelevant
# here - every slot is overwritten before pass 2 reads it. (A symmetric variant
# that does res[i] *= prefix in pass 1 WOULD depend on the 1-init.)

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # pass 1 - construct prefix array "in-place" in result
        res = [1] * (len(nums))

        running_prefix = 1
        for i in range((len(nums))):
            res[i] = running_prefix
            running_prefix *= nums[i]
        running_postfix = 1
        for i in range(len(nums) - 1, -1, -1):
            res[i] *= running_postfix
            running_postfix *= nums[i]
        return res

# Alternative - explicit prefix + suffix arrays: O(n) time, O(n) extra space.
# Clearer to read, but fails the O(1)-extra-space follow-up. The active version
# collapses the suffix array into a single running scalar.
# def productExceptSelf(self, nums):
#     n = len(nums)
#     prefix = [1] * n
#     suffix = [1] * n
#     for i in range(1, n):
#         prefix[i] = prefix[i - 1] * nums[i - 1]
#     for i in range(n - 2, -1, -1):
#         suffix[i] = suffix[i + 1] * nums[i + 1]
#     return [prefix[i] * suffix[i] for i in range(n)]
#
# Anti-pattern (DON'T use) - division: O(n) time, O(1) space, BUT the problem
# bans division precisely because zeros break it. total = product of all; then
# answer[i] = total // nums[i]. With one zero you get 0/0 at the zero's index
# (its answer should be the product of the rest); with two+ zeros all answers
# are 0. Requires counting zeros and branching - ugly, and forbidden here.
