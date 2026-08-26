"""
Combination Sum II - LeetCode 40 (Medium)
Pattern: Backtracking (NeetCode section 10) - Shape B (start index + loop) with pruning
         and sibling deduplication
List: -
Solved 2026-08-25 | outcome: hint (dedup rule derived from a two-frame comparison after the
                   subtree-subsumption argument was spelled out; complexity needed pushing
                   to combine the terms)

Raw: Data Structures & Algorithms/combination-target-sum-ii/submission-0.py

The ACTIVE code below is the CLEANED version - see "What changed" for every difference
from the accepted submission. David's verbatim accepted submission is preserved as Alt 1.

Style notes on the submission: trailing whitespace on two blank lines inside dfs; missing
spaces around the arithmetic in cands[j-1] and dfs(j+1, ...). Both fixed in the active code,
both visible in Alt 1. Type hints were complete, including the nested dfs, unprompted, and
the "from typing import List" line was written rather than leaning on neetcode.io's
pre-imports. combinationSum2 stays camelCase - LeetCode imposes that signature.
"""

from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        res: List[List[int]] = []
        path: List[int] = []
        cands = sorted(candidates)                 # REQUIRED, not an optimization - see below

        def dfs(start: int, total: int) -> None:
            if total == target:
                res.append(path[:])                # record a COPY
                return                             # children can only overshoot

            for j in range(start, len(cands)):
                new_total = total + cands[j]
                if new_total > target:
                    break                          # sorted -> every later j overshoots too
                if j > start and cands[j] == cands[j - 1]:
                    continue                       # equal SIBLING already tried this level
                path.append(cands[j])
                dfs(j + 1, new_total)              # j + 1: each element used at most once
                path.pop()

        dfs(0, 0)
        return res


# ---------------------------------------------------------------------------
# What changed from the accepted submission
# ---------------------------------------------------------------------------
# 1. subset -> path. "subset" was carried over from Subsets (78), but these are
#    combinations, not subsets. path also matches the skeleton name used on the
#    backtracking concept page, so the shape stays recognizable across the
#    section.
#
# 2. GUARD ORDER SWAPPED: the overshoot break now runs BEFORE the duplicate
#    continue. Both orders are correct - the conditions are independent and
#    neither can mask the other, because a duplicate that overshoots implies its
#    equal predecessor overshot too, so the row was already dead. But the break
#    kills the entire remaining SIBLING ROW while the continue kills a single
#    candidate, so testing the stronger claim first ends the row immediately
#    instead of falling through to the next distinct candidate to rediscover the
#    same fact. Cheapest, strongest kill first.
#
# 3. HOISTED new_total = total + cands[j]. The submission computed it twice (in
#    the prune test and again at the call site). Naming it makes the prune read
#    as a claim about the CHILD - "the node I am about to create is already
#    over" - rather than as arithmetic that happens to appear twice.
#
# 4. PEP 8: spaces around the arithmetic (cands[j - 1], dfs(j + 1, ...)),
#    trailing whitespace removed.
#
#
# ---------------------------------------------------------------------------
# The sort is a CORRECTNESS PRECONDITION here, not an optimization
# ---------------------------------------------------------------------------
# This is the one real difference in kind from 39, and it is the thing to say
# out loud in an interview.
#
#   In 39, sorting bought the break prune - a constant-factor win. Delete the
#   sort and the answer is still correct, just slower.
#
#   In 40, the dedup test is cands[j] == cands[j - 1], which only detects
#   duplicates because equal values are ADJACENT. Delete the sort and the
#   algorithm returns duplicate combinations - it is wrong, not slow.
#
# sorted(candidates) rather than candidates.sort(): .sort() would mutate the
# CALLER's list, a side effect the signature does not advertise. Costs O(n)
# space, which is already paid by the recursion depth anyway.
#
#
# ---------------------------------------------------------------------------
# The dedup rule: j > start, and why it is not just "skip equal neighbours"
# ---------------------------------------------------------------------------
# Two frames can both see cands[j] == cands[j - 1] with the SAME j, and they
# need opposite treatment. With cands = [1, 2, 2, 5], j = 2:
#
#   dfs(start=0), path=[]      -> the first 2 was tried at j=1 EARLIER IN THIS
#                                 SAME LOOP. The second 2 is its SIBLING.
#                                 SKIP.
#   dfs(start=2), path=[1, 2]  -> the first 2 was consumed by the PARENT frame
#                                 and is already in path. The second 2 is its
#                                 CHILD, stacking into [1, 2, 2].
#                                 KEEP.
#
# So j > start is asking: is cands[j - 1] a SIBLING I already tried at this
# level, or an ANCESTOR already sitting in my path? Deduplication is always a
# statement about siblings, never about the path. An unconditional
# "cands[j] == cands[j - 1] -> continue" makes every combination that uses a
# value twice unreachable: on the input above with target 5 it never emits
# [1, 2, 2].
#
# WHY SKIPPING THE SIBLING IS SOUND. At the root of [1, 2, 2, 5] the top-level
# loop's four iterations recurse with:
#
#     j=0  picks 1           dfs(1)  -> draws from [2, 2, 5]
#     j=1  picks 2 (first)   dfs(2)  -> draws from [2, 5]
#     j=2  picks 2 (second)  dfs(3)  -> draws from [5]
#     j=3  picks 5           dfs(4)  -> draws from []
#
# Rows j=1 and j=2 begin the combination with the same VALUE (combinations are
# multisets of values, not of indices), but [5] is a suffix of [2, 5]. So every
# combination the j=2 subtree can produce, the j=1 subtree can also produce -
# strictly subsumed, drawing from a strictly smaller pool. Generally: later
# occurrences of a value in a sibling row always get a smaller suffix, so their
# subtrees are always subsumed by the first occurrence's.
#
# Note the guard is NOT load-bearing as a bounds check on the j - 1 index.
# Reversing the conjuncts would evaluate cands[-1] at j = 0, but j > start is
# False there anyway, so the "and" short-circuits to the same answer. The order
# is stylistic; the two-frame distinction is the part that matters.
#
#
# ---------------------------------------------------------------------------
# The hidden assumption: every candidate is strictly positive
# ---------------------------------------------------------------------------
# LeetCode guarantees 1 <= candidates[i] <= 50. As in 39, both prunes rest on it:
#
#   A negative   -> "new_total > target" stops being a proof of death, since a
#                   later negative could come back under. The break silently
#                   DROPS valid answers.
#   A 0          -> the "return" after recording an exact match becomes wrong: a
#                   0 could extend an already-complete combination into another
#                   valid one. Unlike 39, there is no non-termination risk here,
#                   because dfs(j + 1) always advances.
#
#
# ---------------------------------------------------------------------------
# Complexity - derived, not transplanted from 39
# ---------------------------------------------------------------------------
# The two structural numbers, each traced to the line that causes it:
#
#     depth              n       <- dfs(j + 1) retires a candidate every step
#     nodes              2^n     <- see the bijection argument below
#     recorded length    up to n <- the path[:] copy
#
# WHY 2^n AND NOT n^n. The loop runs up to n times and the depth is up to n, so
# the naive read is n^n. That double-counts: the loop and the depth are not
# independent, because every iteration consumes index budget. Count the nodes by
# what they ARE instead of by the tree's shape - each node is reached by exactly
# one increasing sequence of indices, so nodes correspond ONE-TO-ONE with
# subsets of the indices. 2^n subsets, 2^n nodes.
#
# COMPLEXITY, decomposed (count of nodes TIMES work per node - a product, never
# a sum; the sum form is the recurring error):
#
#     O(2^n)       visiting the tree
#     * O(n)       the path[:] copies
#     = O(n * 2^n) time, with the O(n log n) sort dominated
#
#   Space: O(n) auxiliary - recursion depth n plus the single path list of size
#          <= n, plus the O(n) sorted copy.
#
#   Output: O(n * R) where R = the number of valid combinations, R <= 2^n.
#
# THE OUTPUT IS NOT A LOWER BOUND HERE - the contrast with Subsets (78) is the
# sharp beat. In 78, R = 2^n exactly, so O(n * 2^n) was unbeatable: you cannot
# produce the answer faster than you can write it down. In 40, R is
# data-dependent and usually tiny relative to 2^n - for candidates = [1] * 100
# with target 3, R = 1. That gap between 2^n explored and R emitted is exactly
# the space the prune and the dedup live in.
#
# Both bounds are worst-case and neither prune improves them; they are large
# constant-factor wins on real inputs, which is the usual situation for
# backtracking pruning.
#
#
# ---------------------------------------------------------------------------
# Alt 1: David's accepted submission, verbatim
#        O(n * 2^n) time, O(n) auxiliary + O(n * R) output
# ---------------------------------------------------------------------------
# Same asymptotic bound as the active code; every change above is a readability
# or constant-factor improvement.
#
# from typing import List
#
# class Solution:
#     def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
#         res: List[List[int]] = []
#         subset: List[int] = []
#         cands = sorted(candidates)
#
#         def dfs(start: int, total: int) -> None:
#             if total == target:
#                 res.append(subset[:])
#                 return
#
#             for j in range(start, len(cands)):
#                 if j > start and cands[j] == cands[j-1]:
#                     continue
#                 if total + cands[j] > target:
#                     break
#                 subset.append(cands[j])
#                 dfs(j+1, total + cands[j])
#                 subset.pop()
#
#         dfs(0, 0)
#         return res
#
#
# ---------------------------------------------------------------------------
# Alt 2: brute force - port 39, then dedup the OUTPUT
#        O(n * 2^n) search + O(R * n log n) dedup time, O(n * R) space
# ---------------------------------------------------------------------------
# The naive path reasoned through in the interview, and the one worth naming and
# then rejecting out loud. Take the 39 solution, change dfs(j) to dfs(j + 1) for
# the use-once rule, collect everything, then collapse equal multisets. Because
# the candidates are sorted, each emitted combination is already non-decreasing,
# so the tuple() alone canonicalizes it - the per-combination sort is free.
#
# class Solution:
#     def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
#         res: List[List[int]] = []
#         path: List[int] = []
#         cands = sorted(candidates)
#
#         def dfs(start: int, total: int) -> None:
#             if total == target:
#                 res.append(path[:])
#                 return
#             for j in range(start, len(cands)):
#                 if total + cands[j] > target:
#                     break
#                 path.append(cands[j])
#                 dfs(j + 1, total + cands[j])
#                 path.pop()
#
#         dfs(0, 0)
#         return [list(t) for t in {tuple(c) for c in res}]
#
# WHY IT IS REJECTED, and it is not the dedup's O(R * n log n). It is that the
# duplicate BRANCHES were still walked. candidates = [1] * 100, target = 3: the
# correct answer holds one combination, [1, 1, 1], and this explores every
# 3-element index subset of 100 to find it - C(100, 3) = 161,700 root-to-leaf
# paths, then throws 161,699 away. The fix has to prevent the branch from being
# taken, not filter the output. Same lesson as the break prune in 39: kill it in
# the tree.
#
#
# ---------------------------------------------------------------------------
# Alt 3: the same sibling rule, encoded by VALUE instead of by index
#        O(n * 2^n) time, O(n) auxiliary + O(n * R) output
# ---------------------------------------------------------------------------
# NeetCode's own reference form. Instead of asking "is my left neighbour a
# sibling I already tried" (index-based, j > start), it remembers the last value
# actually tried at this level and skips anything equal to it (value-based).
# Identical behaviour; prev is local to the frame, so it resets automatically at
# every level, which is what makes it equivalent to the j > start test.
#
# Worth seeing both, because the index form does not survive into problems where
# the candidate list is not what is being indexed - Permutations (46) with a
# used[] array, for instance - while the value form usually does.
#
# class Solution:
#     def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
#         res: List[List[int]] = []
#         path: List[int] = []
#         cands = sorted(candidates)
#
#         def dfs(start: int, total: int) -> None:
#             if total == target:
#                 res.append(path[:])
#                 return
#
#             prev = -1                       # no candidate equals -1: all are >= 1
#             for j in range(start, len(cands)):
#                 if total + cands[j] > target:
#                     break
#                 if cands[j] == prev:
#                     continue
#                 path.append(cands[j])
#                 dfs(j + 1, total + cands[j])
#                 path.pop()
#                 prev = cands[j]
#
#         dfs(0, 0)
#         return res
#
# The sentinel is the one wart: prev = -1 silently assumes no candidate is -1.
# Fine under 1 <= candidates[i] <= 50, but prev: Optional[int] = None is the
# honest version if the constraint is not guaranteed. The index form has no
# sentinel to get wrong.
