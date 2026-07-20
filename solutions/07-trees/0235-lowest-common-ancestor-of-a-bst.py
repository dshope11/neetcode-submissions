# Lowest Common Ancestor of a BST - LC 235 - Medium - [Blind 75]
# Pattern: Trees / BST-ordering. The first problem that EXPLOITS the BST
#          invariant (left < node < right) rather than doing a generic traversal.
#          The LCA of p and q is the SPLIT POINT: descend from the root, and the
#          first node where p and q stop agreeing on direction (both-left / both-
#          right) is their lowest common ancestor. One directed walk, no paths.
# Solved 2026-07-19 | outcome: hint (approach fully solo; nudged onto the
#          if-vs-elif control-flow bug during implementation - see note below)
#
# Raw: Data Structures & Algorithms/lowest-common-ancestor-in-binary-search-tree/submission-2.py
#
# Active code below IS David's accepted submission, VERBATIM (his choice to keep
# the `break` form). No cleanup was applied - the code is already the optimal
# shape: O(h) time, O(1) space. The `while node:` guard is technically dead given
# the problem guarantees both p and q exist (the `else: break` always fires
# first), but it is kept deliberately as a DEFENSIVE exit - if the input were ever
# malformed (a node not in the tree), this returns None gracefully instead of
# crashing on None.val. Alt 1 is the recursive form; Alt 2 is the tighter
# `while True` / return-in-else variant (the public reference shape).


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        node = root
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left        # both smaller -> LCA is in the left subtree
            elif p.val > node.val and q.val > node.val:
                node = node.right       # both larger -> LCA is in the right subtree
            else:
                break                   # split (or one equals node) -> node is the LCA
        return node


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Nothing - active code is the verbatim accepted submission. The algorithm is
# already optimal (single directed walk, O(1) extra space); no logic or style
# changes warranted. snake_case (`node`), no Unicode, PEP 8 clean; the camelCase
# `lowestCommonAncestor`/`p`/`q` are LeetCode's fixed signature, not a slip.
#
# Implementation bug caught mid-solve (worth remembering): the first draft used
# two independent `if` statements instead of an `if/elif` chain -
#     if both-smaller:  node = node.left
#     if both-larger:   node = node.right   # <-- separate `if`, not elif
#     else:             break
# Because the second `if` is independent, when branch one moved the pointer left
# the second `if/else` then RE-JUDGED the NEW node in the SAME iteration, so the
# walk got one step ahead of itself. On root=[5,3,8,1,4,7,9,null,2], p=1, q=2 it
# descended 5 -> 3, then the else broke immediately and returned 3 instead of 1.
# Fix: chain the branches with `elif` so EXACTLY ONE fires per loop iteration.
#
# Complexity: O(h) time - one root-to-split-point path, h = tree height
# (O(log n) balanced, O(n) skewed - same shape-dependence as any BST find).
# O(1) space - no stack, no path lists; the split-point insight is what removes
# the two O(n) path arrays a naive "walk to p, walk to q, compare paths" would use.


# ---------------------------------------------------------------------------
# Alt 1: recursive form - O(h) time, O(h) space (call stack)
#        Same split-point logic, recursion instead of a loop. Reads cleanly but
#        pays O(h) call-stack space vs the iterative O(1) - so the iterative form
#        is strictly better here (nothing to unwind, no reason to recurse).
# ---------------------------------------------------------------------------
# class Solution:
#     def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
#         if p.val < root.val and q.val < root.val:
#             return self.lowestCommonAncestor(root.left, p, q)
#         if p.val > root.val and q.val > root.val:
#             return self.lowestCommonAncestor(root.right, p, q)
#         return root                  # split (or one equals root) -> LCA


# ---------------------------------------------------------------------------
# Alt 2: tighter iterative (the public reference shape) - O(h) time, O(1) space
#        `while True` + return directly from the else, mutating `root` in place.
#        One fewer line than the active version; drops the defensive `while node:`
#        guard (safe ONLY because p and q are guaranteed present).
# ---------------------------------------------------------------------------
# class Solution:
#     def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
#         while True:
#             if p.val < root.val and q.val < root.val:
#                 root = root.left
#             elif p.val > root.val and q.val > root.val:
#                 root = root.right
#             else:
#                 return root
