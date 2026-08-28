"""
Permutations - LeetCode 46 (Medium)
Pattern: Backtracking (NeetCode section 10) - the start index is REPLACED by a used array,
         because order matters
List: -
Solved 2026-08-27 | outcome: solo (no reference; accepted, no mechanical bugs)

Raw: Data Structures & Algorithms/permutations/submission-0.py

The ACTIVE code below is the CLEANED version - see "What changed" for every difference
from the accepted submission. David's verbatim accepted submission is preserved as Alt 1.

Style notes on the submission: the nested dfs had a typed parameter but no return
annotation. Fixed in the active code, visible in Alt 1. permute stays camelCase-free by
luck - LeetCode's signature happens to be a single lowercase word.
"""

from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []
        perm: List[int] = []
        used: List[bool] = [False] * len(nums)     # dense index keys -> array beats a set

        def dfs() -> None:
            if len(perm) == len(nums):             # depth tracked by perm, not by used
                res.append(perm[:])                # record a COPY
                return
            for i in range(len(nums)):
                if used[i]:
                    continue                       # already consumed on THIS path
                perm.append(nums[i])
                used[i] = True
                dfs()
                perm.pop()                         # un-choose, both halves
                used[i] = False

        dfs()
        return res


# ---------------------------------------------------------------------------
# What changed from the accepted submission
# ---------------------------------------------------------------------------
# 1. used: List[int] (a list of consumed indices) -> List[bool] of length n.
#    This is the only ALGORITHMIC change, and it is a real asymptotic one.
#    "if i in used" is a linear scan of a Python list: O(k) at depth k. The
#    loop body runs n times per node and paid that cost every time, so a node
#    at depth ~n did O(n^2) work and the submission ran in O(n^2 * n!). Direct
#    indexing makes the test O(1) and restores the intended O(n * n!).
#
#    A set would also be O(1), but the keys here are exactly the integers
#    0..n-1 - a dense range - so the index IS the hash. The array wins on
#    constants: no hashing, no resize/rehash, no allocation churn, better
#    cache behavior. General rule: when the keys are a dense integer range,
#    an array is a set, and a faster one. Reach for set() when the keys are
#    sparse or not integers.
#
# 2. def dfs(used): -> def dfs():  (parameter dropped; used comes from the closure)
#    The parameter SHADOWED the enclosing used, and every call passed the same
#    list object - so it looked like per-frame state while being one shared
#    object, correct only because of the matching used.pop(). Two costs: it
#    hides that fact from a reader, and it invites the "fix" dfs(used[:]),
#    which is O(n) per node for no benefit. Every other solve in this section
#    used a bare closure; this one now matches.
#
# 3. Base case len(used) == len(nums) -> len(perm) == len(nums).
#    FORCED by change 1, not cosmetic. used and perm were two encodings of the
#    same information - used the SET of chosen indices, perm the SEQUENCE of
#    chosen values - so their lengths were always equal and either could track
#    depth. Once used is a fixed-length boolean array its length is n at every
#    node, and only perm still tracks depth.
#
# 4. Added the -> None return annotation on the nested dfs.
#
#
# ---------------------------------------------------------------------------
# Why the start index had to go (the structural point)
# ---------------------------------------------------------------------------
# Every earlier problem in this section carried availability as ONE INTEGER,
# start. Test it here: keep start and dfs(j + 1), and move the record into a
# base case "if len(path) == len(nums)" so every answer has full length. On
# [1,2,3] that returns exactly ONE result, [1,2,3].
#
# start forces the indices along any root-to-leaf path to be strictly
# INCREASING, so each index set is reachable by exactly one path - order is
# quotiented out by construction. That is precisely what makes Shape B a
# combinations engine, and it is unfixable by choosing a smarter start:
#
#     Shape B (combinations)         Permutations
#     ----------------------         ------------
#     start: one integer             used: n booleans
#     the consumed set is a          the consumed set is an
#     PREFIX, describable            ARBITRARY SUBSET (consume
#     by one number                  index 5 while 2 is free)
#
# The state grows from O(1) to O(n), and that growth IS the price of order
# mattering. Not an implementation detail - a structural consequence.
#
#
# ---------------------------------------------------------------------------
# Complexity
# ---------------------------------------------------------------------------
# Depth              n            the base case len(perm) == len(nums)
# Branching factor   n - k        the for line, AFTER the continue filters it
# Leaves             n!           n * (n-1) * (n-2) * ... = n!
# Nodes              ~e * n!      sum over levels of n!/(n-k)! = n! * sum 1/j!
#                                 -> converges to e * n!, i.e. Theta(n!)
# Per-record cost    O(n)         the perm[:] copy at each of the n! leaves
#
#     Time   O(n * n!)   = n! leaves * O(n) copy   (nodes are Theta(n!), so
#                          the traversal itself is dominated by the copies)
#     Aux    O(n)        recursion depth n + perm (<= n) + used (exactly n)
#     Output O(n * n!)   also the LOWER BOUND - you cannot emit the answer
#                        faster than you can write it down
#
# The for line does DOUBLE DUTY and the two numbers differ: it runs n times
# (the per-node cost factor) but only n - k iterations survive the continue
# (the branching factor). The filter is the wedge between them, and it is what
# turns n^n into n!. Attributing "n!" to the base case alone is wrong - the
# base case only sets the depth.
#
# The submitted version (Alt 1) is O(n^2 * n!): same tree, but each of the n
# loop iterations paid an O(k) list scan. Quote the bound your code earns,
# then the bound the problem allows.
#
#
# ---------------------------------------------------------------------------
# Edge case: nums = []
# ---------------------------------------------------------------------------
# The constraints say 1 <= len(nums), but the empty input is the interesting
# trace: len(perm) == len(nums) is 0 == 0, so the base case fires on the FIRST
# call, records [], and returns. Result [[]], not [] - and [[]] is correct,
# since there is exactly one permutation of the empty sequence. The general
# lesson: when the base case is a length equality, always check whether it is
# already satisfied at the root.
#
#
# ===========================================================================
# Alt 1 - David's accepted submission, VERBATIM. O(n^2 * n!) time, O(n) aux.
# ===========================================================================
# The extra factor of n is the "i in used" linear scan; see change 1 above.
#
# from typing import List
#
# class Solution:
#     def permute(self, nums: List[int]) -> List[List[int]]:
#         res: List[List[int]] = []
#         used: List[int] = []
#         perm: List[int] = []
#
#         def dfs(used: List[int]):
#             if len(used) == len(nums):
#                 res.append(perm[:])
#                 return
#             for i in range(len(nums)):
#                 if i in used:
#                     continue
#                 perm.append(nums[i])
#                 used.append(i)
#                 dfs(used)
#                 perm.pop()
#                 used.pop()
#
#         dfs(used)
#         return res
#
#
# ===========================================================================
# Alt 2 - in-place swap: no perm, no used at all. O(n * n!) time, O(n) aux.
# ===========================================================================
# The standard interview follow-up: "can you do it without the used array?"
#
# Drop the requirement that nums stay pristine and let the INPUT ARRAY be the
# accumulator. At depth k, nums[:k] is the permutation so far and nums[k:] is
# exactly the pool of unused values - so "which values are still available" is
# carried by the array's own layout and needs no separate structure. Choosing
# candidate i for slot k is one swap; the un-choose is the same swap again.
#
# class Solution:
#     def permute(self, nums: List[int]) -> List[List[int]]:
#         res: List[List[int]] = []
#         n = len(nums)
#
#         def dfs(k: int) -> None:
#             if k == n:
#                 res.append(nums[:])          # copy: nums is about to be un-swapped
#                 return
#             for i in range(k, n):
#                 nums[k], nums[i] = nums[i], nums[k]
#                 dfs(k + 1)
#                 nums[k], nums[i] = nums[i], nums[k]   # restore
#
#         dfs(0)
#         return res
#
# Auxiliary space is the recursion stack alone - no perm, no used. Two caveats
# worth saying out loud rather than pretending they are free:
#
#   - It MUTATES the caller's list. Fully restored by the time dfs(0) returns,
#     but not visible in the signature.
#   - It DESTROYS sorted order as it goes, so it does not extend to the
#     duplicate case (Permutations II, 47), whose dedup rule depends on equal
#     values staying adjacent. The used-array form does extend. Two correct
#     algorithms with different futures - pick on where the section is going,
#     not on the space constant.
#
#
# ===========================================================================
# Alt 3 - iterative insertion cascade. O(n * n!) time, O(n * n!) space.
# ===========================================================================
# The non-recursive analogue, and the sibling of the take/skip cascade used for
# Subsets (78). Absorb one value at a time: every permutation of the first k
# values yields k + 1 permutations of the first k + 1, by inserting the new
# value at each position.
#
# class Solution:
#     def permute(self, nums: List[int]) -> List[List[int]]:
#         res: List[List[int]] = [[]]
#         for num in nums:
#             nxt: List[List[int]] = []
#             for perm in res:
#                 for i in range(len(perm) + 1):
#                     nxt.append(perm[:i] + [num] + perm[i:])
#             res = nxt
#         return res
#
# The level sizes go 1, 2, 6, 24, ... = k! exactly, which makes the n! fall
# out of the loop structure with no tree to reason about. Note it rebinds res
# to a fresh list each round rather than appending to the list being iterated -
# the same evaluation-order trap flagged in the Subsets file, sidestepped here
# by building into nxt instead.
