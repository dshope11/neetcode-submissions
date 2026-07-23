# ===========================================================================
# *** REVISIT / DRILL COLD ***  (flagged by David, 2026-07-22)
#   Solved WITH help - approach reached ~90% Socratically, but the child-bound
#   arithmetic (counts vs indices) and the single-pointer left-before-right
#   ordering were supplied, and the final IndexError (len vs len-1 on the top
#   call) needed a nudge. Come back and run this from a blank editor: be able to
#   derive the four bounds and explain WHY left-before-right is load-bearing
#   without looking. This is not yet muscle memory.
# ===========================================================================
#
# Construct Binary Tree from Preorder and Inorder Traversal - LC 105 - Medium - [Blind 75]
# Pattern: Trees / divide-and-conquer reconstruction from traversal orders.
#   Key facts:
#     * preorder[0] is always the ROOT (pre-order visits node before subtrees).
#     * In INORDER, the root splits the array: values left of it are the entire
#       left subtree, values right of it are the entire right subtree.
#     * preorder is laid out [ root | whole LEFT subtree | whole RIGHT subtree ],
#       so once you know the left subtree's SIZE you know exactly where preorder
#       switches from left to right. Recurse on each half. A single traversal
#       alone is ambiguous (preorder [1,2]: 2 could be either child) - inorder is
#       what disambiguates, which is why the problem hands you both.
# Solved 2026-07-22 | outcome: hint (see REVISIT banner above)
#
# Raw: Data Structures & Algorithms/binary-tree-from-preorder-and-inorder-traversal/submission-0.py
#
# Active code below is the accepted submission with a tiny style tidy only
# (index_map built with a comprehension, above the helper). No logic changed -
# the typed version was already correct and O(n). Alt 1 is the verbatim submission.


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # value -> its index in inorder. Built ONCE over the original array so the
        # indices stay valid forever (no slicing -> no shifting indices). This is
        # what turns the O(n) "find the root in inorder" scan into an O(1) lookup.
        index_map = {val: i for i, val in enumerate(inorder)}
        self.pre_idx = 0  # monotonic pointer into preorder; shared across all calls

        def build(in_lo, in_hi):
            if in_lo > in_hi:            # empty inorder window -> no subtree
                return None              # (in_lo == in_hi is a valid single node)
            root_val = preorder[self.pre_idx]
            self.pre_idx += 1            # consume this root; next preorder value is
            root = TreeNode(root_val)    # the LEFT subtree's root (see ordering note)
            mid = index_map[root_val]    # root's position in inorder
            root.left  = build(in_lo, mid - 1)   # left window: strictly before root
            root.right = build(mid + 1, in_hi)   # right window: strictly after root
            return root

        return build(0, len(inorder) - 1)


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# STYLE only (no logic change - the typed code was already correct and O(n)):
#   - index_map is built with a dict comprehension and placed ABOVE `def build`,
#     so the file reads top-to-bottom (map ready before the helper that uses it).
#     The submission built it with a for-loop AFTER the def but before the call,
#     which also works (populated before the first build() runs) - just reads
#     less naturally.
#   - The submission's original `root.right` comment was a copy-paste of the left
#     one ("everything before root"); corrected here to "after root".
#
# WHY LEFT-BEFORE-RIGHT IS LOAD-BEARING (the one subtlety - drill this):
#   self.pre_idx walks preorder strictly left to right, one step per node, and
#   preorder is [ root | whole LEFT subtree | whole RIGHT subtree ]. So the very
#   next preorder value after a root is the root of its LEFT subtree. You must
#   fully consume the left subtree (advancing the pointer through all of it)
#   BEFORE the right recursion runs - i.e. `root.left = build(...)` must execute
#   before `root.right = build(...)`. Recurse right first and you'd feed the
#   left subtree's preorder values into the right subtree: every node on the
#   wrong side. With a single shared pointer, recursion ORDER is the correctness
#   condition. (The explicit-bounds Alt 2 doesn't have this dependency, because
#   each call is told its exact preorder range instead of trusting the pointer.)
#
# THE BUG THAT BIT (top-level call): the base case treats in_hi as an INCLUSIVE
#   index (in_lo > in_hi = empty). The first draft called build(0, len(inorder)),
#   one past the last valid index -> the right spine recursed one level too deep,
#   pre_idx marched off the end of preorder -> IndexError. Fix: len(inorder) - 1.
#   General trap this problem sets: mixing COUNTS and INDICES. k = mid - in_lo is
#   a count (left-subtree size); the inorder bounds mid-1 / mid+1 are indices.
#   Don't cross them.
#
# Complexity: O(n) time - each node built exactly once, and every per-node op
#   (preorder read, map lookup, pointer bump) is O(1). O(n) space - the index_map
#   holds all n values; plus O(h) recursion stack (h = tree height).


# ---------------------------------------------------------------------------
# Alt 1: David's accepted submission, VERBATIM (the honest practice record)
# ---------------------------------------------------------------------------
# class Solution:
#     def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
#         self.pre_idx = 0
#         index_map = {}
#
#         def build(in_lo, in_hi):
#             if in_lo > in_hi:
#                 return None
#             root_val = preorder[self.pre_idx]
#             self.pre_idx += 1
#             root = TreeNode(root_val)
#             mid = index_map[root_val] # position of root in inorder
#             root.left  = build(in_lo, mid - 1) # left window: everything before root
#             root.right = build(mid + 1, in_hi) # right window: everything after root
#             return root
#
#         for idx, val in enumerate(inorder):
#             index_map[val] = idx
#
#         root = build(0, len(inorder)-1)
#         return root


# ---------------------------------------------------------------------------
# Alt 2: EXPLICIT preorder+inorder bounds, no shared pointer - O(n) / O(n)
#        The version reasoned first in the interview. Each call is handed its
#        exact preorder AND inorder range, so it does NOT depend on left-before-
#        right ordering (the ranges are self-contained). Costs an extra pair of
#        parameters and the count/index arithmetic that the pointer version hides.
#          k = mid - in_lo  is the LEFT subtree size (a count). The left subtree
#          occupies the next k preorder slots: [pre_lo+1, pre_lo+k]. The right
#          subtree is the rest: [pre_lo+k+1, pre_hi]. Note the preorder hi must be
#          anchored at pre_lo (+k), NOT at 0 - the slip to avoid.
# ---------------------------------------------------------------------------
# class Solution:
#     def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
#         index_map = {val: i for i, val in enumerate(inorder)}
#
#         def build(pre_lo, pre_hi, in_lo, in_hi):
#             if pre_lo > pre_hi:
#                 return None
#             root_val = preorder[pre_lo]
#             root = TreeNode(root_val)
#             mid = index_map[root_val]
#             k = mid - in_lo                                  # left subtree size
#             root.left  = build(pre_lo + 1, pre_lo + k, in_lo, mid - 1)
#             root.right = build(pre_lo + k + 1, pre_hi, mid + 1, in_hi)
#             return root
#
#         return build(0, len(preorder) - 1, 0, len(inorder) - 1)


# ---------------------------------------------------------------------------
# Alt 3: NAIVE slicing + linear search - O(n^2) time, O(n^2) space (the brute)
#        The most readable version, and the one to be able to reject on cost.
#        Two hidden O(n)-per-node costs: inorder.index(...) is a linear scan, and
#        every slice COPIES its elements (a Python slice is NOT O(1)). Across n
#        nodes on a skewed tree that compounds to O(n^2). The Alt-1/Alt-2 fixes
#        are exactly: (a) a value->index map kills the scan, (b) passing index
#        bounds instead of slices kills the copying.
# ---------------------------------------------------------------------------
# class Solution:
#     def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
#         if not preorder:
#             return None
#         root_val = preorder[0]
#         root = TreeNode(root_val)
#         mid = inorder.index(root_val)                        # O(n) scan
#         root.left  = self.buildTree(preorder[1:mid + 1], inorder[:mid])    # slices copy
#         root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:]) # -> O(n) each
#         return root
