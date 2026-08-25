"""
Combination Sum - LeetCode 39 (Medium)
Pattern: Backtracking (NeetCode section 10) - Shape B (start index + loop) with pruning
List: Blind 75
Solved 2026-08-24 | outcome: hint (design solo; two mechanical bugs located via questions,
                   and the complexity bound needed correcting)

Raw: Data Structures & Algorithms/combination-target-sum/submission-0.py

The ACTIVE code below is the CLEANED version - see "What changed" for every difference
from the accepted submission. David's verbatim accepted submission is preserved as Alt 1.

Style notes on the submission: trailing whitespace on the blank line inside the class;
one blank line before the top-level class where PEP 8 wants two. Both fixed in the active
code, both visible in Alt 1. Type hints were complete, including the nested dfs, unprompted.
combinationSum stays camelCase - LeetCode imposes that signature.
"""

from typing import List


class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        res: List[List[int]] = []
        subset: List[int] = []
        candidates = sorted(nums)              # ascending, so the break below is valid

        def dfs(start: int, total: int) -> None:
            if total == target:
                res.append(subset[:])          # record a COPY
                return                         # children can only overshoot

            for j in range(start, len(candidates)):
                if total + candidates[j] > target:
                    break                      # sorted -> every later j overshoots too
                subset.append(candidates[j])
                dfs(j, total + candidates[j])  # j, not j+1: reuse allowed
                subset.pop()

        dfs(0, 0)
        return res


# ---------------------------------------------------------------------------
# What changed from the accepted submission
# ---------------------------------------------------------------------------
# 1. RUNNING SUM MOVED INTO THE SIGNATURE. The submission recomputed
#    total = sum(subset) by loop at the top of every call - O(len(subset)) per
#    node. Now dfs(start, total) carries it and the call site passes
#    total + candidates[j]. Per-node work drops to O(1).
#
#    General rule: the accumulator holds the ANSWER; the signature holds the
#    DERIVED FACTS about the answer so far. Anything maintainable incrementally
#    belongs in the signature, not recomputed from the accumulator. (Same idea
#    reappears in N-Queens, where the derived facts are the occupied diagonals.)
#
#    Sibling idiom, equally good: pass remaining = target - total and test
#    against 0, which makes the prune read as "remaining < 0". Pick one.
#
# 2. RETURN AFTER RECORDING AN EXACT MATCH. The submission appended and then
#    fell through into the for loop, exploring children that could only
#    overshoot. Sound ONLY because candidates are strictly positive - see the
#    hidden-assumption note below.
#
# 3. SORT + BREAK PRUNE (new; the submission had none). With candidates
#    ascending, discovering that candidates[j] alone overshoots the remaining
#    budget proves the same for every later j, so break kills the whole
#    remaining ROW OF SIBLINGS instead of one branch. O(n log n) paid once,
#    dominated by the search.
#
#    break, NOT return. They happen to be equivalent here because nothing
#    follows the loop - that is an accident of this function's shape, not a
#    property of the technique. break is a claim about the loop; return is a
#    claim about the frame. Match the construct to the claim.
#
# 4. THE OVERSHOOT CHECK ON ARRIVAL DISAPPEARED. The submission's
#    "elif total > target: return" is now unreachable by construction: change 3
#    checks BEFORE descending, so no call is ever entered in an overshot state.
#    Check-before-descend subsumes check-on-arrival.
#
# 5. Dropped the trailing bare "return" at the end of dfs - implicit None.
#
# 6. sorted(nums) rather than nums.sort(). .sort() would mutate the CALLER's
#    list, a side effect the signature does not advertise. Costs O(n) space.
#
# 7. PEP 8: trailing whitespace removed, two blank lines before the class.
#
#
# ---------------------------------------------------------------------------
# The hidden assumption: every candidate is strictly positive
# ---------------------------------------------------------------------------
# LeetCode guarantees 2 <= nums[i] <= 40. Every prune here rests on it:
#
#   A 0 in nums     -> dfs(j) does not advance and appending 0 does not change
#                      total, so the recursion never terminates. Not a wrong
#                      answer - a stack overflow. Note this is specific to the
#                      REUSE variant; dfs(j+1) would be fine with zeros.
#   A negative      -> "total > target" stops being a proof of death, since a
#                      later negative could come back under. The prune silently
#                      DROPS valid answers.
#
# Worth saying out loud in an interview: "my pruning is only valid because all
# candidates are positive; with zeros this does not terminate and with
# negatives the prune is unsound."
#
#
# ---------------------------------------------------------------------------
# Why the bound is NOT 78's bound
# ---------------------------------------------------------------------------
# The code is nearly identical to Subsets, so the temptation is to reuse
# O(n * 2^n). It does not hold. Let d = target // min(nums).
#
#                        Subsets (78)        Combination Sum (39)
#   depth                n                   d
#   branching factor     2                   up to n
#   nodes                2^n                 n^d
#   recorded length      up to n             up to d
#
# The one line that causes the whole difference:
#
#     dfs(j + 1)  retires a candidate every step -> depth bounded by n
#     dfs(j)      does not advance               -> depth bounded by the TARGET,
#                                                   nothing about n bounds it
#
# COMPLEXITY, decomposed (count of nodes TIMES work per node - a product, never
# a sum; the sum form is the recurring error):
#
#     O(n^d)       visiting the tree
#     * O(d)       the subset[:] copies, length up to d
#     = O(d * n^d) time
#
#   Space: O(d) auxiliary - only one root-to-leaf path is alive at a time
#          (recursion depth d + the single subset list of size <= d), plus the
#          O(n) sorted copy. Output space is separate and unbounded by anything
#          the algorithm controls.
#
#   The prune does NOT improve this worst-case bound - it cannot, since the
#   output alone can be that large. It is a large constant-factor win on real
#   inputs, which is the usual situation for backtracking pruning.
#
#
# ---------------------------------------------------------------------------
# Alt 1: David's accepted submission, verbatim
#        O(d * n^d) time, O(d) auxiliary + O(output)
# ---------------------------------------------------------------------------
# Same asymptotic bound as the active code: the O(d) per-node recomputation
# replaces the O(d) copy cost rather than adding to it, and the missing prune
# costs a constant factor, not an exponent.
#
# from typing import List
#
# class Solution:
#     def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
#         res: List[List[int]] = []
#         subset: List[int] = []
#
#         def dfs(start: int) -> None:
#             total = 0
#             for num in subset:
#                 total += num
#             if total == target:
#                 res.append(subset[:])
#             elif total > target:
#                 return
#             for j in range(start, len(nums)):
#                 subset.append(nums[j])
#                 dfs(j)
#                 subset.pop()
#             return
#
#         dfs(0)
#         return res
#
# Two mechanical bugs preceded this accepted version, both worth remembering:
#
#   subset.pop      - valid Python. Attribute lookup returns a BOUND METHOD
#                     OBJECT; the line is an expression statement, so the result
#                     is evaluated and discarded. It never ran. Detected by
#                     ruff B018 / pylint pointless-statement. Same class as
#                     my_list.sort or f.close - no-ops that look like actions.
#
#   return inside   - a return as the last line of the for BODY caps the loop at
#   the loop body     one iteration. Combined with the dead pop, the search
#                     explored exactly one path (always candidates[0], never
#                     backtracking) and returned [] for any target that was not
#                     a multiple of nums[0].
#
#
# ---------------------------------------------------------------------------
# Alt 2: Shape A - binary take/skip with reuse (the NeetCode canonical form)
#        O(d * 2^(n+d)) time, O(n + d) auxiliary + O(output)
# ---------------------------------------------------------------------------
# Proof that Shape A CAN solve this - the take branch recurses on i instead of
# i+1, which is what buys unbounded reuse.
#
# class Solution:
#     def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
#         res: List[List[int]] = []
#         subset: List[int] = []
#
#         def dfs(i: int, total: int) -> None:
#             if total == target:
#                 res.append(subset[:])
#                 return
#             if i >= len(nums) or total > target:
#                 return
#
#             subset.append(nums[i])       # take nums[i] - and stay on i
#             dfs(i, total + nums[i])
#             subset.pop()                 # un-choose
#             dfs(i + 1, total)            # skip nums[i] permanently
#
#         dfs(0, 0)
#         return res
#
# WHY THE ACTIVE FORM IS STILL THE ONE TO DRILL. Shape A is Shape B collapsed to
# a branching factor of 2, not a peer of it. Here that collapse costs:
#
#   - A node has no SIBLING ROW, only a take-child and a skip-child. The sort +
#     break prune has nowhere to live; the best available is killing one branch
#     at a time. Same reason the equal-neighbour dedup of Combination Sum II
#     (40) and Subsets II (90) is only expressible in Shape B.
#   - The bound gets uglier: the tree is binary with depth up to n + d (at most
#     d takes, at most n skips), so O(2^(n+d)) nodes - a different-looking bound
#     for the same search.
#
# Shape A is fine when the question at a node genuinely is "in or out". The
# moment it becomes "which of several", it needs a loop.
