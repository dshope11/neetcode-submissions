# Maximum Depth of Binary Tree - LC 104 - Easy - [Blind 75]
# Pattern: Trees (recursive DFS, POST-ORDER "aggregate up"). Each node's answer
#          needs BOTH children's answers first, so the work happens after the two
#          recursive calls: depth = 1 + max(left_depth, right_depth).
# Solved 2026-07-16 | outcome: solo
#
# Raw: Data Structures & Algorithms/depth-of-binary-tree/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was already correct and optimal; the only change is dropping the
# redundant parentheses around the return expression. David's verbatim
# submission is preserved as Alt 1; iterative DFS with an explicit stack is
# Alt 2; iterative BFS level-count (the follow-up reasoned in Phase 1) is Alt 3.
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
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:                 # empty tree / fell off a leaf's child -> 0
            return 0
        # post-order: both recursive calls resolve BEFORE this node aggregates
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Same algorithm, same complexity (O(n) time; O(h) space for the recursion
# stack - O(log n) balanced, O(n) worst-case skewed). One change, pure style:
#   - Dropped the redundant outer parens: `return (1 + max(...))` -> `return
#     1 + max(...)`. No behavioral difference; the parens weren't grouping
#     anything the operator precedence didn't already handle.
# No convention slips in the typed version: `maxDepth` is camelCase, but that is
# LeetCode's fixed method signature (the API), not a naming choice.
#
# Gotcha that bit during the solve - recursive INSTANCE-method calls need self.:
#   Inside `class Solution`, the recursive call must be `self.maxDepth(...)`, not
#   `maxDepth(...)`. A bare `maxDepth(root.left)` raises
#   `NameError: name 'maxDepth' is not defined` - the method lives in the class
#   namespace, not the module/global namespace, so it is only reachable through
#   the instance (self) or the class. This is the tax of LeetCode's method-on-a-
#   class harness; a module-level `def` (like Alt 2/3 helpers) is called bare.
#
# Key insight - the base case IS the leaf terminator:
#   No explicit "is this a leaf?" check is needed. A leaf's two None children
#   each hit `if root is None: return 0`, so the leaf returns 1 + max(0, 0) = 1.
#   The single top guard does all the boundary work.
#
# Contrast worth banking - this is the POST-ORDER "aggregate up" shape, distinct
# from LC 226's PRE-ORDER "transform in place":
#   - 226 Invert: do the work (swap) THEN recurse; helper returns nothing.
#   - 104 MaxDepth: recurse FIRST, then combine children's returns; the value
#     flows UP the call stack. This is the template the harder Trees problems
#     specialize (diameter/balanced add a `self.best` side-channel updated during
#     the same post-order pass; 104 is the clean baseline with no side-channel).
#
# Space, by tree shape (recursion stack depth = tree height h):
#   - balanced tree:  height ~ log2(n)  -> O(log n) stack.
#   - skewed tree:    height = n         -> O(n) stack (degenerate linked list).
#   BFS (Alt 3) is the MIRROR: O(n) on a balanced tree (bottom level ~ n/2 in
#   the queue at once), O(1) on a skewed one. Opposite worst-case shapes.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(h) space
#        Correct and optimal; only cosmetic difference is the redundant parens.
# ---------------------------------------------------------------------------
# class Solution:
#     def maxDepth(self, root: Optional[TreeNode]) -> int:
#         if root is None:
#             return 0
#         return (1 + max(self.maxDepth(root.left), self.maxDepth(root.right)))


# ---------------------------------------------------------------------------
# Alt 2: iterative DFS with an explicit stack of (node, depth) - O(n) / O(h)
#        The "do it without recursion" follow-up that PRESERVES the O(h) space
#        profile: the explicit stack replaces the call stack one-for-one. Push
#        each child paired with depth+1; track the running max as nodes pop.
# ---------------------------------------------------------------------------
# class Solution:
#     def maxDepth(self, root: Optional[TreeNode]) -> int:
#         if root is None:
#             return 0
#         stack = [(root, 1)]
#         best = 0
#         while stack:
#             node, depth = stack.pop()
#             best = max(best, depth)
#             if node.left:
#                 stack.append((node.left, depth + 1))
#             if node.right:
#                 stack.append((node.right, depth + 1))
#         return best


# ---------------------------------------------------------------------------
# Alt 3: iterative BFS, count levels - O(n) time, O(n) space (queue)
#        Drain one full level per outer pass (snapshot len(q) first), bumping a
#        level counter. The answer is the number of levels. Space is O(n) on a
#        balanced tree (bottom level dominates the queue) - the mirror of DFS.
# ---------------------------------------------------------------------------
# from collections import deque
#
# class Solution:
#     def maxDepth(self, root: Optional[TreeNode]) -> int:
#         if root is None:
#             return 0
#         q = deque([root])
#         levels = 0
#         while q:
#             for _ in range(len(q)):        # drain exactly one level
#                 node = q.popleft()
#                 if node.left:
#                     q.append(node.left)
#                 if node.right:
#                     q.append(node.right)
#             levels += 1
#         return levels
