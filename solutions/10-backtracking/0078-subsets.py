"""
Subsets - LeetCode 78 (Medium)
Pattern: Backtracking (NeetCode section 10) - the bare choose / explore / un-choose skeleton
List: NeetCode 150 (not Blind 75)
Solved 2026-08-24 | outcome: looked-up (section opener - the skeleton was shown once,
                   deliberately, then transcribed; the design rep is Combination Sum / LC 39)

Raw: Data Structures & Algorithms/subsets/submission-0.py

The ACTIVE code below IS the verbatim accepted submission - nothing changed. It is
already fully type-annotated (including the nested dfs), imports List so it runs
standalone, and is ASCII / snake_case / PEP 8 clean. There is therefore no separate
"Alt 1 = verbatim submission" block below; duplicating the active code would add noise.
The alternatives are the two genuinely distinct approaches instead.

Style notes on the submission: none. First solve in the series with zero cleanups.
"""

from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []
        subset: List[int] = []

        def dfs(i: int) -> None:
            if i == len(nums):           # BASE CASE: decided about every element
                res.append(subset[:])    # record a COPY - see the aliasing note below
                return

            subset.append(nums[i])       # PRE:     choose nums[i]
            dfs(i + 1)                   # RECURSE: explore with it
            subset.pop()                 # POST:    un-choose
            dfs(i + 1)                   # RECURSE: explore without it

        dfs(0)
        return res


# ---------------------------------------------------------------------------
# What changed from the accepted submission
# ---------------------------------------------------------------------------
# Nothing. Only the explanatory comments above were added.
#
#
# ---------------------------------------------------------------------------
# Why it works
# ---------------------------------------------------------------------------
# Every subset is one root-to-leaf path in a binary decision tree: at each index
# you either take nums[i] or skip it, one level per element. n levels -> 2^n
# leaves -> 2^n subsets. The code never inspects a VALUE, only a position, so it
# is indifferent to what the numbers are (uniqueness is the only assumption, and
# only because duplicates would need dedup - that is Subsets II / LC 90).
#
#                              []
#                     /                  \
#               take 1                  skip 1
#                 [1]                     []
#               /     \                 /     \
#          take 2    skip 2        take 2    skip 2
#           [1,2]      [1]           [2]       []
#           /   \      /  \          /  \      /  \
#      [1,2,3][1,2] [1,3] [1]    [2,3] [2]  [3]   []
#
# TWO THINGS WORTH CARRYING FORWARD:
#
# 1. The pop does DOUBLE DUTY. In the maze-solver version of this skeleton
#    (see the recursion foundation page) path.pop() was pure cleanup on a dead
#    end. Here it is cleanup AND setup: once nums[i] is popped, subset is in
#    exactly the state the skip-branch needs. One line, two jobs.
#
# 2. THE COPY IS NOT OPTIONAL. res.append(subset) appends a REFERENCE to the one
#    shared list. All 2^n entries would alias the same object, and since subset
#    is empty when the recursion finishes, the answer would be 2^n empty lists.
#    subset[:] snapshots the contents. General rule: whenever a mutable
#    accumulator is recorded into a results list, copy it.
#
# COMPLEXITY, decomposed (the n does not come from where it looks like it does):
#
#     O(2^n)       visiting the tree - 2^(n+1)-1 nodes, O(1) work each
#     + O(n*2^n)   the subset[:] copies at the 2^n leaves, avg length n/2   <- dominant
#     = O(n * 2^n) time
#
#   Space: O(n) auxiliary (recursion depth n + the single subset list of size <= n).
#          O(n * 2^n) for the output, which is also the LOWER BOUND for any
#          solution - you cannot produce the answer faster than you can write it.
#
#
# ---------------------------------------------------------------------------
# Alt 1: iterative cascade - no recursion at all
#        O(n * 2^n) time, O(1) auxiliary + O(n * 2^n) output
# ---------------------------------------------------------------------------
# David's own approach, proposed cold before any recursion was discussed: start
# from the empty set and, for each new number, duplicate everything built so far
# with that number appended. Each pass doubles the result, so n passes -> 2^n.
#
# class Solution:
#     def subsets(self, nums: List[int]) -> List[List[int]]:
#         res: List[List[int]] = [[]]
#         for num in nums:
#             res += [curr + [num] for curr in res]
#         return res
#
# No special case is needed for the singleton {num} - it falls out as the empty
# set plus num.
#
# TRAP: this is safe ONLY because the list comprehension is fully evaluated
# BEFORE += extends res. The equivalent-looking
#
#     for curr in res:
#         res.append(curr + [num])
#
# is an infinite loop - it appends to the list it is iterating. The comprehension
# form is correct by evaluation order, not by anything visible in its shape.
#
#
# ---------------------------------------------------------------------------
# Alt 2: sibling recursive form - start index instead of binary take/skip
#        O(n * 2^n) time, O(n) auxiliary + O(n * 2^n) output
# ---------------------------------------------------------------------------
# This is the form that GENERALIZES to the rest of the section, so it is the one
# to have in muscle memory.
#
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []
        subset: List[int] = []

        def dfs(start: int) -> None:
            res.append(subset[:])              # EVERY node is an answer
            for j in range(start, len(nums)):
                subset.append(nums[j])
                dfs(j + 1)                     # j+1, never start+1
                subset.pop()

        dfs(0)
        return res
#
# Two differences from the active version, both of which matter later:
#
#   1. It records at EVERY node, not only at leaves - so there is no explicit
#      base case at all. The for-loop simply runs out of candidates and the call
#      returns. The base case is implicit in the exhausted range.
#
#   2. The loop REPLACES the skip branch. Instead of "take nums[i] or do not",
#      it asks "which of the remaining candidates do I take next". dfs(j + 1)
#      - not dfs(start + 1) - is what keeps this generating COMBINATIONS rather
#      than permutations; that off-by-one is the most common bug in this family.
#
# Where it extends to:
#   + a target and a running sum          -> Combination Sum (LC 39)
#   + reuse allowed: dfs(j) not dfs(j+1)  -> unbounded-reuse variants
#   + sort first, skip equal neighbours   -> Subsets II (LC 90)
