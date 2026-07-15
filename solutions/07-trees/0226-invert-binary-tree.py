# Invert Binary Tree - LC 226 - Easy - [Blind 75]
# Pattern: Trees (recursive DFS - visit every node, swap its two children).
#          The whole problem is "at each node, swap left and right"; recursion
#          delivers you to every node and the swap is the O(1) per-node work.
# Solved 2026-07-15 | outcome: solo
#
# Raw: Data Structures & Algorithms/invert-a-binary-tree/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was already correct and clean (single `if node is None` guard,
# swap, recurse both, outer returns root). The only change is the three-line
# temp swap collapsed to Python's one-line tuple swap. David's verbatim
# submission is preserved as Alt 1; the no-helper self-recursive form is Alt 2;
# the iterative BFS form (the follow-up reasoned in Phase 1) is Alt 3.
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


def invert_node(node: Optional[TreeNode]) -> None:
    if node is None:                                 # only base case needed:
        return                                       # None children bounce off here
    node.left, node.right = node.right, node.left    # tuple swap - RHS built first
    invert_node(node.left)
    invert_node(node.right)


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        invert_node(root)
        return root


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Same algorithm, same complexity (O(n) time; O(h) space for the recursion
# stack - O(log n) balanced, O(n) worst-case skewed). One change, pure style:
#   - Collapsed the three-line temp swap
#         tmp = node.left
#         node.left = node.right
#         node.right = tmp
#     into the idiomatic one-liner `node.left, node.right = node.right, node.left`.
#     Python evaluates the entire right-hand side into a tuple BEFORE any
#     assignment, so there is no clobber and no temp needed.
#   - Added `from typing import Optional` (see header) - portability only.
# No convention slips in the typed version: `invert_node` was already snake_case
# (only the outer `invertTree` is camelCase, which is LeetCode's fixed API).
#
# Key insight - the single guard is the ENTIRE base case:
#   `if node is None: return` at the top makes the per-child None checks
#   unnecessary. Recurse into children unconditionally; a None child just hits
#   the top guard and returns. A leaf's swap of (None, None) is a harmless no-op.
#   Over-guarding with "if both children None" adds nothing.
#
# Insight worth banking - DFS and BFS have OPPOSITE worst-case space:
#   - recursive/stack DFS: O(n) on a SKEWED tree (height n), O(log n) balanced.
#   - queue BFS:           O(n) on a BALANCED tree (bottom level ~ n/2 nodes),
#                          O(1)-O(2) on a skewed tree (~1 node per level).
#   Neither beats O(n) worst case; they just fail on opposite tree shapes.
#   Correctness is identical - both visit every node and swap.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(h) space
#        Correct and clean; three-line temp swap instead of the tuple swap.
# ---------------------------------------------------------------------------
# def invert_node(node: Optional[TreeNode]) -> None:
#     if node is None:
#         return
#     tmp = node.left
#     node.left = node.right
#     node.right = tmp
#     invert_node(node.left)
#     invert_node(node.right)
#
# class Solution:
#     def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
#         invert_node(root)
#         return root


# ---------------------------------------------------------------------------
# Alt 2: no helper - fold the recursion into invertTree itself - O(n) / O(h)
#        Works because invertTree returns root, so it doubles as the recursive
#        call. Swap the two RECURSED subtrees in one assignment. Terser, but the
#        helper form reads a hair clearer (swap-then-descend vs. swap-of-descents).
# ---------------------------------------------------------------------------
# class Solution:
#     def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
#         if root is None:
#             return None
#         root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
#         return root


# ---------------------------------------------------------------------------
# Alt 3: iterative BFS with a queue - O(n) time, O(n) space (queue)
#        The no-recursion follow-up. Dequeue a node, swap its children, enqueue
#        the (non-None) children. Stack instead of queue would be an iterative
#        DFS - either is correct here; only the space profile differs by shape.
# ---------------------------------------------------------------------------
# from collections import deque
#
# class Solution:
#     def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
#         if root is None:
#             return None
#         q = deque([root])
#         while q:
#             node = q.popleft()
#             node.left, node.right = node.right, node.left
#             if node.left:
#                 q.append(node.left)
#             if node.right:
#                 q.append(node.right)
#         return root
