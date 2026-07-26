# Binary Tree Maximum Path Sum - LC 124 - Hard - (NeetCode 150, Blind 75)
# Pattern: Trees (recursive DFS, POST-ORDER "aggregate up" + a side-channel).
#          The hard-tier form of LC 543 (Diameter): return one value UP the
#          recursion while updating a separate running best in the SAME
#          post-order pass. Two twists over 543: (1) each child branch is
#          CLAMPED to 0 (max(gain, 0)) so a negative subtree is DROPPED rather
#          than subtracted; (2) the running best is seeded to float("-inf"),
#          not 0, because an all-negative tree's answer is a single negative
#          node (the path must be non-empty).
# Solved 2026-07-25 | outcome: hint
#
# Raw: Data Structures & Algorithms/binary-tree-maximum-path-sum/submission-1.py
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was correct and optimal; the only change is a RENAME of the helper
# from max_path_sum_subtree to max_gain, because what the helper RETURNS is the
# best downward gain (one branch), NOT the subtree's max path sum (that is what
# the side-channel records) - the old name described the side-channel's job, not
# the return value's, blurring the very two-things-one-pass split the problem is
# about. David's verbatim submission is preserved as Alt 1; the nonlocal-closure
# variant (the NeetCode reference shape) is Alt 2; the O(n^2) brute force
# reasoned in Phase 1 is Alt 3.
#
# Optional is imported here so the file is honest/portable; on neetcode.io it is
# pre-imported, so the typed submission omitted it.
from typing import Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_path_sum = float("-inf")

        def max_gain(node):
            if node is None:                    # base case: missing child -> 0 gain
                return 0
            # Clamp each child's gain to 0: a negative branch contributes nothing
            # (we drop it) rather than dragging the path down.
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)
            # side-channel: best path BENDING at this node = node.val + BOTH
            # branches. node.val is NOT clamped - the current node is always on
            # its own path, which is what makes the all-negative case work and
            # why the seed must be -inf, not 0.
            self.max_path_sum = max(self.max_path_sum,
                                    node.val + left_gain + right_gain)
            # return value: best gain EXTENDING UP through this node into the
            # parent = node.val + a SINGLE branch (a parent's path can't fork
            # through this node). Reuse the clamped gains - do NOT recurse again.
            return node.val + max(left_gain, right_gain)

        max_gain(root)
        return self.max_path_sum


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Same algorithm, same complexity (O(n) time; O(h) space for the recursion
# stack - O(log n) balanced, O(n) worst-case skewed). Pure-naming cleanup:
#   - Renamed the helper max_path_sum_subtree -> max_gain. The function returns
#     the best single-branch DOWNWARD GAIN from a node, not the subtree's max
#     path sum (that is the self.max_path_sum side-channel). The shorter name
#     also reads cleanly at the call sites: left_gain = max(max_gain(...), 0).
# No convention slips in the typed version: all snake_case, float("-inf") seed
# (correctly dodging the all-negative trap a `0` seed would fall into), and the
# children clamped while node.val stays unclamped.
#
# Bug that bit during the solve - RECOMPUTING the recursion in the return:
#   The typed draft first returned
#       node.val + max(max_path_sum_subtree(node.left),
#                      max_path_sum_subtree(node.right))
#   i.e. it called the helper AGAIN in the return line instead of reusing the
#   already-computed left_gain / right_gain. Two bugs in one line:
#     (1) CORRECTNESS - those fresh calls return the RAW (unclamped) gain, so a
#         negative branch was subtracted into the value handed up, not dropped.
#         On [-15,10,20,null,null,15,5,-5,-6] node 15 handed up 15 + (-5) = 10
#         instead of 15, so node 20 recorded 20 + 10 + 5 = 35 instead of 40.
#     (2) COMPLEXITY - each node then triggered its children's recursion twice
#         (once for the gain, once in the return), branching the call tree to
#         exponential time, not O(n).
#   Fix (both at once): return node.val + max(left_gain, right_gain) - reuse the
#   clamped values already in hand. General rule: if you named a subresult,
#   reuse the name; a second recursive call is both wrong and slow.
#
# Key insight - node.val is the ONLY thing never clamped:
#   You clamp the CHILDREN (max(child, 0)) = "I may take nothing from a child."
#   You never clamp the current node - you are always standing on it. So every
#   node contributes node.val + 0 + 0 as a valid one-node path candidate, which
#   is why "least-negative single node" needs zero special handling AND why the
#   seed must be -inf (a 0 seed would beat a legitimately-negative answer). The
#   -inf seed and the unclamped node.val are the same design decision seen from
#   two sides. This is the one hinge that separates 124 from 543, where every
#   height is non-negative so a 0 seed is fine.
#
# Two combinations, one pass (the shared 543/124 skeleton):
#   - node.val + left_gain + right_gain      -> path bending HERE (both branches)
#                                               -> the answer, into the side-channel
#   - node.val + max(left_gain, right_gain)  -> best gain extending UP (one branch)
#                                               -> the return, into the PARENT
#   Neither can be the sole return value - which is exactly why the answer needs
#   a side-channel (self.max_path_sum / a nonlocal) to survive the recursion.
#
# Why BFS is not the favorable-space alternative here: the answer flows
# BOTTOM-UP (a parent needs both child gains first), inherently post-order DFS -
# same argument as LC 543. The iterative escape is an explicit-stack post-order
# carrying a gains dict, still O(h). BFS wins space only on TOP-DOWN (level-order)
# problems, not this one.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(h) space
#        Correct and optimal; helper named max_path_sum_subtree (renamed to
#        max_gain in the active code - see "What changed").
# ---------------------------------------------------------------------------
# class Solution:
#     def maxPathSum(self, root: Optional[TreeNode]) -> int:
#         self.max_path_sum = float("-inf")
#
#         def max_path_sum_subtree(node):
#             if node is None:
#                 return 0
#             left_gain = max(max_path_sum_subtree(node.left), 0)
#             right_gain = max(max_path_sum_subtree(node.right), 0)
#             self.max_path_sum = max(self.max_path_sum,
#                                     node.val + left_gain + right_gain)
#             return node.val + max(left_gain, right_gain)
#
#         max_path_sum_subtree(root)
#         return self.max_path_sum


# ---------------------------------------------------------------------------
# Alt 2: nonlocal closure variant (the NeetCode reference shape) - O(n) / O(h)
#        Identical algorithm; the side-channel is a closed-over `res` reached
#        via `nonlocal` instead of a `self.` attribute. Both let the best
#        survive the recursion; `self.` is the common LeetCode idiom, `nonlocal`
#        keeps all state inside the method (nothing leaks onto the instance).
# ---------------------------------------------------------------------------
# class Solution:
#     def maxPathSum(self, root: Optional[TreeNode]) -> int:
#         res = float("-inf")
#
#         def dfs(node):
#             nonlocal res
#             if node is None:
#                 return 0
#             left = max(dfs(node.left), 0)
#             right = max(dfs(node.right), 0)
#             res = max(res, node.val + left + right)
#             return node.val + max(left, right)
#
#         dfs(root)
#         return res


# ---------------------------------------------------------------------------
# Alt 3: brute force, fresh max_gain() at every node - O(n^2) time, O(h) space
#        The naive baseline reasoned in Phase 1: for each node compute the path
#        bending there (node.val + its two clamped subtree gains) with an
#        INDEPENDENT max_gain() call, and take the max over all nodes. O(n^2)
#        because each of the n best_through() nodes re-walks its whole subtree
#        via max_gain - the single-pass DFS collapses this to O(n) by reusing
#        the child gains it already has. The None base case returns -inf so an
#        empty path never wins (the path must be non-empty).
# ---------------------------------------------------------------------------
# class Solution:
#     def maxPathSum(self, root: Optional[TreeNode]) -> int:
#         def max_gain(node):
#             if node is None:
#                 return 0
#             left = max(max_gain(node.left), 0)
#             right = max(max_gain(node.right), 0)
#             return node.val + max(left, right)
#
#         def best_through(node):
#             if node is None:
#                 return float("-inf")
#             left = max(max_gain(node.left), 0)
#             right = max(max_gain(node.right), 0)
#             through_here = node.val + left + right
#             return max(through_here,
#                        best_through(node.left),
#                        best_through(node.right))
#
#         return best_through(root)
