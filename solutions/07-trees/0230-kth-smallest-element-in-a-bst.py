# Kth Smallest Element in a BST - LC 230 - Medium - [Blind 75]
# Pattern: Trees / BST in-order. The payoff of the in-order property met on LC 98:
#          an in-order DFS of a BST (left, node, right) visits values in SORTED
#          order, so the k-th node visited is the k-th smallest. Walk in-order with
#          a running counter; stop the instant the counter hits k. No sorting.
# Solved 2026-07-21 | outcome: hint (algorithm fully solo; taught the Python
#          closure/scoping fix for shared recursion state - see the write-up below)
#
# Raw: Data Structures & Algorithms/kth-smallest-integer-in-bst/submission-0.py
#
# Active code below is the CLEANED version (per the /neetcode Phase-3 review).
# David's verbatim accepted submission is preserved as Alt 1. The change is a real
# LOGIC fix, not just naming: the submitted early-exit guard was silently defeated
# (see "What changed"), so the accepted code returned the right answer but ran in
# O(n), not O(h + k). The active version restores the true early exit.


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        self.count = 0
        self.result = None

        def inorder(node):
            if node is None or self.result is not None:  # found -> stop descending
                return
            inorder(node.left)
            if self.result is not None:      # found in the LEFT subtree -> bail before
                return                       # incrementing (would overshoot the counter)
            self.count += 1
            if self.count == k:
                self.result = node.val
                return
            inorder(node.right)

        inorder(root)
        return self.result


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# LOGIC (the important one): the early-exit guard was fixed.
#   The submission guarded on the COUNTER:  `if self.count == k: return`.
#   That answer is correct, but the guard is SILENTLY DEFEATED and the walk
#   degrades to O(n). Trace: let X be the node that records the answer, and say
#   X is the LEFT child of its parent P. X sets result with count == k and
#   returns. Control resumes in P *right after* its `inorder(node.left)` call -
#   at `self.count += 1` - so P bumps the counter to k+1. From then on the guard
#   `self.count == k` compares against k+1, k+2, ... and NEVER matches again, so
#   it stops short-circuiting: P goes on to walk its entire right subtree. For
#   [2,1,3], k=1 this visits all 3 nodes (count ends at 3) instead of stopping.
#   Fix: guard on the MONOTONE "found" flag `self.result is not None` instead of
#   the counter - once set it stays set, so it can't be overshot. Also add a
#   check immediately AFTER `inorder(node.left)` so ancestors don't do the
#   spurious `+= 1` or descend right. Now it is genuinely O(h + k).
#
#   General lesson: an `== target` early-exit guard is fragile whenever a mutation
#   happens AFTER the recursive call returns (here the parent's post-left `+= 1`
#   steps the counter past the target). Guard on a monotone found-flag / value
#   sentinel, not on an exact-equality counter check.
#
# STYLE: none needed - snake_case throughout, clean structure. `Optional[TreeNode]`
#   relies on LeetCode's ambient typing import; kept as-is to match the platform.
#
# Complexity: O(h + k) time - descend h nodes to reach the smallest, then visit k
# in-order before stopping (h << n balanced, so far better than O(n) for small k;
# worst case k = n gives O(n)). O(h) space - recursion stack.


# ===========================================================================
# SHARED RECURSION STATE IN PYTHON - the scoping trap and its four fixes
# ===========================================================================
# This problem needs a counter (and a result) that SURVIVES across sibling
# recursive calls: the count from the left subtree must be visible when the
# current node and the right subtree run. Two plain-int reflexes both FAIL:
#
#   (a) Pass it as a parameter - `inorder(node.left, count)`. Each call gets its
#       OWN local `count`; `count += 1` rebinds that local only. int is immutable,
#       so the caller never sees it. Params flow DOWN, not back UP - the left
#       subtree's increments are lost on return.
#
#   (b) Close over an outer int - define `count = 0` outside, do `count += 1` in
#       the nested helper. `count += 1` is an ASSIGNMENT, and any bare-name
#       assignment inside a function makes that name LOCAL for the whole body, so
#       the `+ 1` reads it before it's locally bound -> UnboundLocalError. (Pure
#       READS of an outer variable are fine - that's why `k` needs no ceremony.)
#
# The four standard fixes (Alt 2/3/4 below demonstrate three of them):
#   1. self. attribute (ACTIVE) - `self.count += 1` mutates an attribute, not a
#      bare name, so the scoping rule never fires. Most common LeetCode idiom.
#   2. nonlocal (Alt 2) - `nonlocal count` says "assignments target the enclosing
#      function's variable." Clean; keeps everything in one function.
#   3. mutable container (Alt 3) - `count = [0]; count[0] += 1` mutates the list's
#      contents rather than rebinding the name. Works, slightly uglier.
#   4. return-threading - each call returns the updated count and you thread it:
#      `count = inorder(node.left, count)`. No shared state (LC-98 flavor), but
#      clunky for this left-node-right shape; not shown.
#   The iterative Alt 4 sidesteps ALL of this - the counter is an ordinary loop
#   local, no nested function, so there's no scoping question at all.


# ---------------------------------------------------------------------------
# Alt 1: David's accepted submission, VERBATIM - correct answer, but O(n)
#        The early-exit guard is on the counter (`self.count == k`), which is
#        defeated by the parent's post-left `+= 1` (see "What changed"), so it
#        walks the whole tree. Preserved as the honest practice record.
# ---------------------------------------------------------------------------
# class Solution:
#     def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
#         self.count = 0
#         self.result = None
#
#         def inorder(node):
#             if self.count == k:
#                 return
#             if node is None:
#                 return
#             inorder(node.left)
#             self.count += 1
#             if self.count == k:
#                 self.result = node.val
#                 return
#             inorder(node.right)
#
#         inorder(root)
#         return self.result


# ---------------------------------------------------------------------------
# Alt 2: nonlocal instead of self. - O(h + k) time, O(h) space
#        Same algorithm, shared state via `nonlocal` rather than instance attrs.
# ---------------------------------------------------------------------------
# class Solution:
#     def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
#         count = 0
#         result = None
#
#         def inorder(node):
#             nonlocal count, result
#             if node is None or result is not None:
#                 return
#             inorder(node.left)
#             if result is not None:
#                 return
#             count += 1
#             if count == k:
#                 result = node.val
#                 return
#             inorder(node.right)
#
#         inorder(root)
#         return result


# ---------------------------------------------------------------------------
# Alt 3: mutable-container state - O(h + k) time, O(h) space
#        Shared state via a 1-element list; `state[0]` is the counter. Mutating
#        the list's contents avoids the bare-name rebinding that needs nonlocal.
# ---------------------------------------------------------------------------
# class Solution:
#     def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
#         count = [0]
#         result = [None]
#
#         def inorder(node):
#             if node is None or result[0] is not None:
#                 return
#             inorder(node.left)
#             if result[0] is not None:
#                 return
#             count[0] += 1
#             if count[0] == k:
#                 result[0] = node.val
#                 return
#             inorder(node.right)
#
#         inorder(root)
#         return result[0]


# ---------------------------------------------------------------------------
# Alt 4: iterative in-order with an explicit stack - O(h + k) time, O(h) space
#        The interview follow-up form. No recursion -> no shared-state scoping
#        question (the counter is a plain loop local) and early-exit is a plain
#        `return` out of the loop. Push all the way left, pop = visit in sorted
#        order, decrement k, stop when k hits 0.
# ---------------------------------------------------------------------------
# class Solution:
#     def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
#         stack = []
#         node = root
#         while stack or node:
#             while node:                 # dive to the leftmost unvisited node
#                 stack.append(node)
#                 node = node.left
#             node = stack.pop()          # visit in sorted order
#             k -= 1
#             if k == 0:
#                 return node.val
#             node = node.right           # then explore the right subtree
