"""
Subsets II - LeetCode 90 (Medium)
Pattern: Backtracking (NeetCode section 10) - Shape B (start index + loop) with sibling
         deduplication, recording at every node
List: -
Solved 2026-08-26 | outcome: solo (40's skeleton recalled from memory and adapted without
                   a reference; accepted first try, no mechanical bugs)

Raw: Data Structures & Algorithms/subsets-ii/submission-0.py

The ACTIVE code below is the CLEANED version - see "What changed" for every difference
from the accepted submission. David's verbatim accepted submission is preserved as Alt 1.

Style notes on the submission: trailing whitespace on the blank line before dfs(0). That is
the whole list - the second consecutive clean first-accepted submission in this section.
Type hints were complete including the nested dfs, and sorted() was used over .sort()
unprompted, carried forward from the 39 gotcha. subsetsWithDup stays camelCase - LeetCode
imposes that signature.
"""

from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []
        subset: List[int] = []
        nums_sorted = sorted(nums)                 # REQUIRED, not an optimization - see below

        def dfs(start: int) -> None:
            res.append(subset[:])                  # record at EVERY node, copy not reference
            for j in range(start, len(nums_sorted)):
                if j > start and nums_sorted[j] == nums_sorted[j - 1]:
                    continue                       # equal SIBLING already tried this level
                subset.append(nums_sorted[j])
                dfs(j + 1)                         # j + 1: each element used at most once
                subset.pop()

        dfs(0)
        return res


# ---------------------------------------------------------------------------
# What changed from the accepted submission
# ---------------------------------------------------------------------------
# 1. candidates -> nums_sorted. "candidates" was vocabulary carried over from 39
#    and 40, where the array genuinely was a candidate pool being measured
#    against a target. Here there is no target and no admission test - it is
#    just the input, sorted. The new name says the one thing about the array
#    that the algorithm actually depends on.
#
# 2. PEP 8: trailing whitespace removed from the blank line before dfs(0).
#
# Nothing else. The logic was already the intended solution; there is no
# algorithmic cleanup to make, which is why this file's "what changed" block is
# two lines instead of four.
#
#
# ---------------------------------------------------------------------------
# What 90 is, in terms of the two problems before it
# ---------------------------------------------------------------------------
# 90 = 78's SHAPE (record at every node, no admission test) + 40's DEDUP RULE.
# It is the first problem in the section that is a composition of two earlier
# ones rather than a variation on one, and that is what makes it a real check:
# the skip decision and the record decision now sit directly on top of each
# other at the head of the loop body, where in 40 they were separated by the
# base case.
#
#   from 78:  res.append(subset[:]) at the top of dfs, no target, no base case
#   from 40:  sorted input + "if j > start and a[j] == a[j - 1]: continue"
#   dropped:  the running total in the signature, the overshoot break, the
#             early return after an exact match
#
# The dropped items all go together: they were the machinery of an ADMISSION
# TEST. With no test to pass, there is nothing to be early about.
#
#
# ---------------------------------------------------------------------------
# The sort is a CORRECTNESS PRECONDITION, and here it has exactly one job
# ---------------------------------------------------------------------------
# The cleanest case in the family, because the sort is doing one thing:
#
#   39 -> sort buys the overshoot break.       Delete it: correct, just slower.
#   40 -> sort buys the break AND adjacency.   Delete it: WRONG (dup output).
#   90 -> sort buys adjacency, nothing else.   Delete it: WRONG (dup output).
#
# The dedup test is nums_sorted[j] == nums_sorted[j - 1], which only detects a
# duplicate because equal values are ADJACENT. On [2, 1, 2] unsorted, the two
# 2s are never neighbours, no skip ever fires, and [2] comes back twice.
#
# sorted(nums) rather than nums.sort(): .sort() would mutate the CALLER's list,
# a side effect the signature does not advertise. The O(n) copy is already paid
# for by the recursion depth.
#
# A second consequence of sorting, worth saying out loud: it also normalizes the
# ORDER WITHIN each emitted subset to non-decreasing. That is what makes "equal
# multiset" and "equal list" the same test here, which is what lets a
# sibling-level skip stand in for a global uniqueness check.
#
#
# ---------------------------------------------------------------------------
# j > start still separates SIBLING from ANCESTOR - and now it also gates a record
# ---------------------------------------------------------------------------
# Same rule as 40, same reasoning: the guard asks whether the equal left
# neighbour is a sibling already tried in THIS loop, or an ancestor already
# sitting in subset. On nums_sorted = [1, 2, 2] with j = 2:
#
#   dfs(start=0), subset=[]      -> the first 2 was tried at j=1 EARLIER IN THIS
#                                   SAME LOOP. Sibling. SKIP.
#   dfs(start=2), subset=[1, 2]  -> the first 2 was consumed by the PARENT and is
#                                   already in subset. Ancestor. KEEP, so that
#                                   [1, 2, 2] is reachable.
#
# WHAT IS NEW IN 90: in 40 a "continue" skipped a subtree of CANDIDATE
# combinations, most of which would have failed the target test anyway. Here
# every node emits, so the continue is skipping a subtree of ACTUAL OUTPUT ROWS
# - including the skipped child's own record at the top of its frame. Dropping
# the guard and skipping every equal neighbour therefore does not just lose
# [1, 2, 2]; it loses [2, 2] as well, because the node that would have recorded
# it is never entered. The failure is quietly incomplete output in both cases,
# but here it is one line of blast radius wider.
#
#
# ---------------------------------------------------------------------------
# Complexity - and this is where 90 differs most from 40
# ---------------------------------------------------------------------------
# The two structural numbers, each traced to the line that causes it:
#
#     depth              n       <- dfs(j + 1) retires a candidate every step
#     nodes              R       <- see the bijection below; R <= 2^n
#     recorded length    up to n <- the subset[:] copy
#
# THE BIJECTION. In 78 each node was reached by exactly one increasing sequence
# of indices, so nodes matched subsets of the INDICES one-to-one: 2^n. Run the
# same argument with the continue in place. Every path is non-decreasing in
# VALUE, and the dedup makes each distinct multiset reachable by exactly one
# path, so the surviving nodes match distinct SUB-MULTISETS one-to-one:
#
#     nodes = R = product over distinct values v of (count(v) + 1)
#
# with equality to 2^n only when every value is distinct - i.e. when the problem
# degenerates back into 78. Concretely, [1] * 6 visits 7 nodes, not 64.
#
# COMPLEXITY, decomposed (count of nodes TIMES work per node - a product, never
# a sum):
#
#     O(R)         visiting the tree
#     * O(n)       the subset[:] copies
#     = O(n * R) time, with the O(n log n) sort dominated
#
#   Space: O(n) auxiliary - recursion depth n plus the single subset list of
#          size <= n, plus the O(n) sorted copy.
#
#   Output: O(n * R) - the same quantity.
#
# THE OUTPUT IS A LOWER BOUND AGAIN HERE, which is the beat worth having ready.
# Every node visited emits exactly one distinct row, so explored and emitted are
# the SAME NUMBER and the algorithm is output-optimal - you cannot beat it,
# because you cannot produce the answer faster than you can write it down. Set
# the three problems side by side:
#
#     78   nodes = 2^n   R = 2^n            no gap - every node is an answer
#     40   nodes <= 2^n  R data-dependent   ENORMOUS gap: [1]*100, target 3
#                                           explores 2^100-worth to emit R = 1
#     90   nodes = R     R = prod(c_v + 1)  no gap - every node is an answer
#
# That gap is the whole reason 40 has a prune and 90 does not, and it is a
# sharper statement of it than "90 has no target to check against". There is
# nothing to prune here because there is no wasted work to cut. Quoting
# O(n * 2^n) for 90 is not wrong as a worst case, but it is the loose bound; it
# is only tight on all-distinct input.
#
#
# ---------------------------------------------------------------------------
# Alt 1: David's accepted submission, verbatim
#        O(n * R) time, O(n) auxiliary + O(n * R) output
# ---------------------------------------------------------------------------
# Identical asymptotics; both changes above are naming and whitespace.
#
# from typing import List
#
# class Solution:
#     def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
#         res: List[List[int]] = []
#         subset: List[int] = []
#         candidates = sorted(nums)
#
#         def dfs(start: int) -> None:
#             res.append(subset[:])
#             for j in range(start, len(candidates)):
#                 if j > start and candidates[j] == candidates[j - 1]:
#                     continue
#                 subset.append(candidates[j])
#                 dfs(j + 1)
#                 subset.pop()
#
#         dfs(0)
#         return res
#
#
# ---------------------------------------------------------------------------
# Alt 2: Shape A - binary take/skip, dedup by jumping the whole run
#        O(n * R) time, O(n) auxiliary + O(n * R) output
# ---------------------------------------------------------------------------
# This is NeetCode's own reference for 90, and it is the interesting alternative
# because Shape A has NO SIBLING ROW - only a take-child and a skip-child. The
# concept page claims dedup is always a statement about siblings, so this looks
# like a counterexample. It is not: the while loop is MANUFACTURING the sibling
# row by hand. Shape B gets the run of equal candidates for free as j, j+1, j+2
# and collapses it with one continue; Shape A has to walk the run explicitly to
# make the same claim. Same statement, different price.
#
# THE RULE IT ENCODES: if you decline a value, you must decline EVERY copy of
# it. Otherwise "skip copy 1, take copy 2" and "take copy 1, skip copy 2"
# produce the same multiset by two different paths. The canonical form the
# algorithm enforces is that copies of a value are always taken as a PREFIX of
# the run.
#
# Note it records only at the leaves (i == len), so unlike the active code the
# node count and the output count are not the same number - but the LEAF count
# is still exactly R.
#
# Rebinding the parameter i inside the frame is what makes the skip branch work
# and is easy to misread as a bug; it is safe, since i is local to the call.
#
# from typing import List
#
# class Solution:
#     def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
#         res: List[List[int]] = []
#         subset: List[int] = []
#         a = sorted(nums)
#
#         def dfs(i: int) -> None:
#             if i == len(a):
#                 res.append(subset[:])
#                 return
#
#             subset.append(a[i])                  # TAKE a[i]
#             dfs(i + 1)
#             subset.pop()
#
#             while i + 1 < len(a) and a[i] == a[i + 1]:
#                 i += 1                           # SKIP a[i] means skip the whole run
#             dfs(i + 1)
#
#         dfs(0)
#         return res
#
#
# ---------------------------------------------------------------------------
# Alt 3: iterative cascade with a repeat-value window
#        O(n * R) time, O(n * R) space (the result itself)
# ---------------------------------------------------------------------------
# The dedup-aware version of the cascade reached solo on 78: for each new value,
# extend the existing subsets by it, doubling the count each round. Duplicates
# break it, and the repair is the same idea as the sibling skip, expressed over
# the results list instead of over a loop range.
#
# WHEN THE VALUE REPEATS, extend only the subsets created in the PREVIOUS round
# - those are exactly the ones that already end in this value, so appending
# another copy stacks the run. Extending an older subset instead would
# re-derive a subset that a previous round already emitted.
#
# Trace on [1, 2, 2]:
#   1        start=0  res = [[], [1]]
#   2        start=0  res = [[], [1], [2], [1,2]]
#   2 (dup)  start=2  res = [[], [1], [2], [1,2], [2,2], [1,2,2]]
#                     -> only [2] and [1,2], last round's additions, got extended
#
# The inner loop appends to res while iterating a range over it, which is safe
# only because range(start, len(res)) freezes len(res) at loop setup. Written as
# "for s in res: res.append(...)" it never terminates - the same evaluation-order
# subtlety as the 78 cascade.
#
# from typing import List
#
# class Solution:
#     def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
#         a = sorted(nums)
#         res: List[List[int]] = [[]]
#         prev_added = 0
#
#         for i, num in enumerate(a):
#             start = len(res) - prev_added if i > 0 and num == a[i - 1] else 0
#             prev_added = len(res) - start
#             for j in range(start, len(res)):
#                 res.append(res[j] + [num])
#
#         return res
#
#
# ---------------------------------------------------------------------------
# Alt 4: brute force - full power set, then dedup on tuples (REJECTED)
#        O(n * 2^n) time, O(n * 2^n) space
# ---------------------------------------------------------------------------
# Enumerate all 2^n index subsets, sort each one, and collapse with a set. It is
# correct, and the objection is NOT the hashing cost - it is that every
# duplicate BRANCH was still walked. Same objection as in 40, but the numbers
# are cleaner here because R is knowable in closed form:
#
#     nums = [1] * 20   ->   2^20 = 1,048,576 subsets enumerated
#                            R = 21 distinct subsets kept
#                            99.998% of the work discarded
#
# The active code visits 21 nodes on that input. This is the concrete meaning of
# "kill it in the tree, not in the output".
#
# from itertools import combinations
# from typing import List
#
# class Solution:
#     def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
#         a = sorted(nums)
#         seen = {
#             combo
#             for size in range(len(a) + 1)
#             for combo in combinations(a, size)
#         }
#         return [list(combo) for combo in seen]
