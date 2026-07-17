# Same Tree - LC 100 - Easy - [Blind 75]
# Pattern: Trees (recursive DFS, PARALLEL two-tree recursion). Walk BOTH trees in
#          lockstep from the roots down; at each step compare the two current
#          nodes, then recurse into the matching child pairs (left-with-left,
#          right-with-right). "Same" = structurally identical AND equal values.
# Solved 2026-07-16 | outcome: solo
#
# Raw: Data Structures & Algorithms/same-binary-tree/submission-0.py
#
# Active code below is the accepted submission VERBATIM: it was already correct,
# optimal, and clean - nothing to clean up. David's verbatim submission is
# therefore also Alt 1 (identical). Iterative BFS with a queue of node-pairs
# (the deep-skinny-tree follow-up reasoned in Phase 1) is Alt 2; iterative DFS
# with an explicit stack of node-pairs is Alt 3.
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
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:          # both fell off together -> match (base case)
            return True
        if not p or not q:           # exactly one fell off -> structure differs
            return False
        # current nodes match AND both subtree-pairs recurse to True.
        # short-circuit `and`: the value check runs FIRST, so a mismatch bails
        # before either recursive call fires (this is the early exit).
        return (p.val == q.val
                and self.isSameTree(p.left, q.left)
                and self.isSameTree(p.right, q.right))


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Nothing behavioral. The accepted submission was correct, optimal, and clean;
# the active code is that submission verbatim (only cosmetic: the return was
# wrapped onto three lines for readability, and `from typing import Optional`
# was added for portability outside the neetcode.io harness). Same algorithm,
# same complexity: O(n) time, O(h) space (recursion stack) - O(log n) balanced,
# O(n) worst-case skewed.
# No convention slips in the typed version: `isSameTree` is camelCase, but that
# is LeetCode's fixed method signature (the API), not a naming choice. And the
# `self.` on the recursive calls was present this time (the NameError gotcha
# from LC 104 did not recur).
#
# Base-case ORDER is a correctness dependency, not cosmetic:
#   `both None -> True` MUST come before `either None -> False`. If reversed, the
#   both-None case would satisfy the `either None` test first and wrongly return
#   False. The two guards only compose correctly in this order.
#
# Why `if not p` is safe here (unlike the leaf-value gotcha):
#   `not p` tests the NODE OBJECT, and a TreeNode instance is always truthy
#   regardless of its .val - so `not p` cleanly means "p is None". Contrast the
#   cheat-sheet trap `if not node.val`, which is buggy because a real 0-valued
#   node is falsy. Same-looking code, opposite safety. (`is None` is still the
#   clearer-intent form; both are correct in this spot.)
#
# Shape contrast worth banking - this is PARALLEL two-tree recursion, distinct
# from the single-tree Trees problems so far:
#   - 226 Invert / 104 MaxDepth: recurse over ONE tree.
#   - 100 Same Tree: recurse over TWO trees in lockstep, the SAME signature
#     isSameTree(p, q) already carrying both roots. 572 Subtree of Another Tree
#     builds directly on this (run isSameTree at every node of the big tree).
#
# The recursion crashes on a pathologically deep tree (~10^6 skewed nodes ->
# Python recursion-limit / C-stack overflow). Alt 2 (BFS) and Alt 3 (explicit
# stack) move the frames off the call stack onto the heap and survive it; BFS
# additionally INVERTS the space profile (O(1) on the skinny tree, O(n) on a
# balanced one) - the mirror of the recursion's worst case.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(h) space - identical to the active code above.
# ---------------------------------------------------------------------------
# class Solution:
#     def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
#         if not p and not q:
#             return True
#         if not p or not q:
#             return False
#         return p.val == q.val and self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


# ---------------------------------------------------------------------------
# Alt 2: iterative BFS, queue of node-pairs - O(n) time, O(w) space (w = width)
#        The "trees are very deep and skinny, don't blow the stack" follow-up.
#        Enqueue (p, q) pairs; for each pair: both-None is a local match (skip),
#        one-None or value-mismatch is an immediate False, else enqueue the two
#        child-pairs. Space is O(1) on a skewed tree (queue holds ~1 pair at a
#        time) - the MIRROR of the recursion's O(n) skewed worst case.
# ---------------------------------------------------------------------------
# from collections import deque
#
# class Solution:
#     def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
#         q_pairs = deque([(p, q)])
#         while q_pairs:
#             a, b = q_pairs.popleft()
#             if not a and not b:
#                 continue
#             if not a or not b or a.val != b.val:
#                 return False
#             q_pairs.append((a.left, b.left))
#             q_pairs.append((a.right, b.right))
#         return True


# ---------------------------------------------------------------------------
# Alt 3: iterative DFS, explicit stack of node-pairs - O(n) time, O(h) space
#        Same crash-proofing as Alt 2 but PRESERVES the O(h) profile (the
#        explicit stack replaces the call stack one-for-one). Only difference
#        from Alt 2 is stack.pop() (LIFO) vs deque.popleft() (FIFO); the pass/
#        fail logic is identical.
# ---------------------------------------------------------------------------
# class Solution:
#     def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
#         stack = [(p, q)]
#         while stack:
#             a, b = stack.pop()
#             if not a and not b:
#                 continue
#             if not a or not b or a.val != b.val:
#                 return False
#             stack.append((a.left, b.left))
#             stack.append((a.right, b.right))
#         return True
