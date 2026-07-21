# Validate Binary Search Tree - LC 98 - Medium - [Blind 75]
# Pattern: Trees / BST-ordering. The sibling of LC 235: where 235 EXPLOITS the
#          BST invariant (left < node < right) to navigate, 98 VERIFIES it holds
#          globally. The trap this problem is built to catch: checking only the
#          parent-child relationship is NOT enough - a node is constrained by its
#          whole ancestor chain, not just its parent. Carry a (low, high) value
#          window down the recursion; each node must satisfy low < val < high, and
#          the window tightens on descent (left -> shrink high, right -> raise low).
# Solved 2026-07-21 | outcome: hint (approach fully solo; nudged on a forgot-to-
#          return-the-recursive-result bug caught in review before submit - below)
#
# Raw: Data Structures & Algorithms/valid-binary-search-tree/submission-0.py
#
# Active code below is the CLEANED version (per the /neetcode Phase-3 review).
# David's verbatim accepted submission is preserved as Alt 1. Only naming changed
# from the typed submission - the algorithm is identical and already optimal.


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


def is_valid_bst_subtree(node: Optional[TreeNode], low: float, high: float) -> bool:
    if node is None:                        # empty subtree is a valid BST
        return True
    if not low < node.val < high:           # strict: no duplicates allowed
        return False
    # tighten the window on the way down: left child capped by node.val (new high),
    # right child floored by node.val (new low). Both subtrees must be valid.
    return (is_valid_bst_subtree(node.left, low, node.val)
            and is_valid_bst_subtree(node.right, node.val, high))


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        return is_valid_bst_subtree(root, float("-inf"), float("inf"))


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Logic: unchanged - the recursive bounds approach is already optimal
#   (O(n) time, O(h) space). Two naming cleanups only:
#   1. helper `isValidBSTSubtree` -> `is_valid_bst_subtree` (snake_case; this is
#      David's own function, so PEP 8 applies - unlike the fixed LeetCode method
#      `isValidBST`, which must stay camelCase).
#   2. bound params `left`/`right` -> `low`/`high`. In a tree, `left`/`right`
#      read as CHILD POINTERS; these are value BOUNDS. `low`/`high` also makes
#      the `low < node.val < high` line read like the math.
#   Also folded the one-use `left`/`right` locals in `isValidBST` straight into
#   the call. (The typed submission's real bug - a missing `return` on the two
#   recursive calls, which returned None instead of propagating the child results
#   - was fixed during Phase 1 before acceptance; the accepted code was correct.)
#
# Why float("-inf")/float("inf") and not INT_MIN/INT_MAX: LC 98's values span
# [-2^31, 2^31 - 1], EXACTLY the 32-bit int range. Seeding the bounds with
# INT_MIN/INT_MAX (the C++/Java reflex) breaks on a root whose value equals the
# sentinel, because the comparison is strict. No int equals infinity, so the
# float sentinels are always safe. Python has no int infinity anyway (ints are
# arbitrary-precision), so this is the idiomatic choice.
#
# No shared mutable state: fresh `low`/`high` are passed down each call, so each
# subtree gets its own tightened copy - nothing to undo on the way back up
# (contrast with backtracking, which mutates-then-restores).
#
# Complexity: O(n) time - certifying validity requires visiting every node
# (early-exit on the first violation, but the valid case is a full visit).
# O(h) space - recursion stack, O(log n) balanced down to O(n) skewed.


# ---------------------------------------------------------------------------
# Alt 1: David's accepted submission, VERBATIM - O(n) time, O(h) space
#        Same algorithm; pre-cleanup naming (camelCase helper, left/right bounds).
# ---------------------------------------------------------------------------
# def isValidBSTSubtree(node: Optional[TreeNode], left: float, right: float) -> bool:
#     if node is None:
#         return True
#     if not left < node.val < right:
#         return False
#     return isValidBSTSubtree(node.left, left, node.val) and isValidBSTSubtree(node.right, node.val, right)
#
# class Solution:
#     def isValidBST(self, root: Optional[TreeNode]) -> bool:
#         left = float("-inf")
#         right = float("inf")
#         return isValidBSTSubtree(root, left, right)


# ---------------------------------------------------------------------------
# Alt 2: in-order traversal - O(n) time, O(h) space
#        The OTHER canonical solution. An in-order walk of a BST (left, node,
#        right) emits values in SORTED order, so validity <=> the sequence is
#        STRICTLY increasing. Track the previous value; if the current node is
#        <= prev, it's invalid. This is intrinsically a DFS trick - it depends on
#        left-root-right ordering (see the note on Alt 3 for why BFS can't do it).
# ---------------------------------------------------------------------------
# class Solution:
#     def isValidBST(self, root: Optional[TreeNode]) -> bool:
#         self.prev = float("-inf")
#         def inorder(node):
#             if node is None:
#                 return True
#             if not inorder(node.left):
#                 return False
#             if node.val <= self.prev:      # strict increase required
#                 return False
#             self.prev = node.val
#             return inorder(node.right)
#         return inorder(root)


# ---------------------------------------------------------------------------
# Alt 3: BFS with bounds carried in the queue - O(n) time, O(w) space
#        The bounds approach is TRAVERSAL-AGNOSTIC: each node's (low, high) window
#        depends only on its ancestor path, never on siblings or visit order, so
#        it works breadth-first too - just carry (node, low, high) in the queue.
#        Space is now O(w) (max tree WIDTH, the queue) instead of O(h) (height);
#        for a balanced tree the bottom level is ~n/2 nodes, so BFS is actually
#        WORSE on space here (O(n) vs O(log n)).
#        Interview note: the in-order approach (Alt 2) does NOT port to BFS - it
#        needs DFS's left-root-right ordering to produce a sorted sequence, which
#        level-order traversal doesn't give. "Which approach is order-dependent"
#        is the sharp point if an interviewer asks "can you do it breadth-first?"
# ---------------------------------------------------------------------------
# from collections import deque
#
# class Solution:
#     def isValidBST(self, root: Optional[TreeNode]) -> bool:
#         queue = deque([(root, float("-inf"), float("inf"))])
#         while queue:
#             node, low, high = queue.popleft()
#             if node is None:
#                 continue
#             if not low < node.val < high:
#                 return False
#             queue.append((node.left, low, node.val))
#             queue.append((node.right, node.val, high))
#         return True
