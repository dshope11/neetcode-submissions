# Diameter of Binary Tree - LC 543 - Easy - (NeetCode 150, non-Blind)
# Pattern: Trees (recursive DFS, POST-ORDER "aggregate up" + a side-channel).
#          The canonical "return one value UP the recursion while updating a
#          separate running best in the SAME post-order pass" shape. The height
#          helper returns the subtree height; the diameter rides along in
#          self.diameter, updated at every node. Pedagogical warm-up for LC 124
#          (Binary Tree Maximum Path Sum), which is the hard-tier form of this.
# Solved 2026-07-25 | outcome: hint
#
# Raw: Data Structures & Algorithms/binary-tree-diameter/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was correct and optimal, but used a "positive body inside `if`,
# fall through to a default return" base-case shape with a `node_height` scratch
# variable. The active code flips it to the canonical early-return guard
# (matching the LC 104 skeleton), dropping one indent level and the scratch var.
# David's verbatim submission is preserved as Alt 1; the `nonlocal res` closure
# variant (the NeetCode reference) is Alt 2; the O(n^2) brute force reasoned in
# Phase 1 is Alt 3.
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
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.diameter = 0

        def height(node):
            if node is None:                 # base case: missing child -> height 0
                return 0
            left_height = height(node.left)
            right_height = height(node.right)
            # side-channel: longest path BENDING at this node (edges) = the two
            # child heights summed. Update the running best on every node.
            self.diameter = max(self.diameter, left_height + right_height)
            # return value: THIS node's height, feeding the PARENT's computation.
            return 1 + max(left_height, right_height)

        height(root)
        return self.diameter


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Same algorithm, same complexity (O(n) time; O(h) space for the recursion
# stack - O(log n) balanced, O(n) worst-case skewed). Pure-style cleanup:
#   - Flipped the base case from `if node is not None: <body>` + fall-through
#     `return node_height` into an early-return guard `if node is None: return
#     0` with the body unindented. This is the canonical post-order shape (same
#     as LC 104), one less indent level.
#   - Dropped the `node_height = 0` scratch variable: with the early return, the
#     height is just the final `return 1 + max(...)` expression.
# No convention slips in the typed version: all snake_case, and `is not None`
# (explicit identity) was used - correctly dodging the node-value-0 truthiness
# trap that `if node:` would fall into.
#
# Bug that bit during the solve - SHADOWING the function name with a local:
#   The typed draft first assigned `height = 1 + max(...)` inside `def height`.
#   Any bare-name assignment makes that name local to the WHOLE function body,
#   so the recursive call `height(node.left)` above it no longer resolved to the
#   function -> `UnboundLocalError: cannot access local variable 'height' where
#   it is not associated with a value`. Same scope mechanism as the LC 230
#   counter trap: assignment anywhere in a scope rebinds the name for the entire
#   scope. Fix: name the computed height something other than the function
#   (`node_height`, or in the active code, no name at all - it's the return).
#
# Key insight - the two child heights are combined TWO WAYS in one pass:
#   - left_height + right_height  -> the turning-point path through THIS node
#     (in edges, under the node-count height convention) -> feeds self.diameter.
#   - 1 + max(left_height, right_height) -> THIS node's own height -> feeds the
#     PARENT's return. The return answers "how tall am I?"; the side-channel
#     answers "what's the best path bending at me?". Neither can be the sole
#     return value, which is exactly WHY the diameter needs a side-channel
#     (self.diameter / nonlocal) to survive across the recursion.
#
# Height convention - why there is NO "+2":
#   height(None) = 0, height(leaf) = 1 (node-count height). Under this
#   convention the diameter through a node is just left_height + right_height,
#   with the edges already absorbed: for a root with two leaf children,
#   1 + 1 = 2 edges. An edge-based convention (leaf = 0) would instead need
#   left + right + 2. Pick one and stay consistent; the node-count form is
#   cleaner because the `1 +` in the return does double duty.
#
# Why BFS is NOT the favorable-space alternative here (unlike level-order
# problems): the answer flows BOTTOM-UP (a parent needs both child heights
# first), which is inherently post-order DFS. The iterative escape from the
# recursion stack is an explicit-stack post-order DFS carrying a heights dict -
# and its stack still holds the current root-to-node path, so it is O(h) too,
# no win. A genuine leaves-upward BFS (Kahn-style: peel leaves, propagate
# heights via a parent map) would give O(width) space but is a curiosity, not
# the expected answer. Contrast level-order problems (right-side view, level
# lists), where the answer flows top-down and BFS is the natural fit.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(h) space
#        Correct and optimal; fall-through base case + node_height scratch var.
# ---------------------------------------------------------------------------
# class Solution:
#     def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
#         self.diameter = 0
#
#         def height(node):
#             node_height = 0
#             if node is not None:
#                 left_height = height(node.left)
#                 right_height = height(node.right)
#                 node_height = 1 + max(left_height, right_height)
#                 self.diameter = max(self.diameter, left_height + right_height)
#             return node_height
#
#         height(root)
#         return self.diameter


# ---------------------------------------------------------------------------
# Alt 2: nonlocal closure variant (the NeetCode reference) - O(n) / O(h)
#        Identical algorithm; the side-channel is a closed-over `res` reached
#        via `nonlocal` instead of a `self.` attribute. Both are valid ways to
#        let the best survive the recursion; `self.` is the common LeetCode
#        idiom, `nonlocal` keeps all state inside the method (nothing leaks onto
#        the instance).
# ---------------------------------------------------------------------------
# class Solution:
#     def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
#         res = 0
#
#         def dfs(node):
#             nonlocal res
#             if not node:
#                 return 0
#             left = dfs(node.left)
#             right = dfs(node.right)
#             res = max(res, left + right)
#             return 1 + max(left, right)
#
#         dfs(root)
#         return res


# ---------------------------------------------------------------------------
# Alt 3: brute force, fresh height() at every node - O(n^2) time, O(h) space
#        The naive baseline reasoned in Phase 1: for each node compute the path
#        bending there (its two subtree heights summed) with an INDEPENDENT
#        height() call, and take the max over all nodes. O(n^2) because each of
#        the n height() calls re-walks its whole subtree - the single-pass DFS
#        collapses this to O(n) by reusing the child heights it already has.
# ---------------------------------------------------------------------------
# class Solution:
#     def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
#         def height(node):
#             if node is None:
#                 return 0
#             return 1 + max(height(node.left), height(node.right))
#
#         def diameter(node):
#             if node is None:
#                 return 0
#             through_here = height(node.left) + height(node.right)
#             return max(through_here,
#                        diameter(node.left),
#                        diameter(node.right))
#
#         return diameter(root)
