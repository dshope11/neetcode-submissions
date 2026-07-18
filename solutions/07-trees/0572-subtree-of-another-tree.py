# Subtree of Another Tree - LC 572 - Easy - [Blind 75]
# Pattern: Trees. NESTED search: an outer single-tree DFS over `root` tries every
#          node as a candidate start, and at each one runs the inner PARALLEL
#          two-tree comparison (isSameTree, from LC 100) to test a full match
#          from that node down. "Subtree" = a node of root plus ALL its
#          descendants matches subRoot exactly (structure + values), to the leaves
#          - not a partial chunk in the middle.
# Solved 2026-07-18 | outcome: solo
#
# Raw: Data Structures & Algorithms/subtree-of-a-binary-tree/submission-0.py
#
# Active code below is the CLEANED version (per the review): the accepted
# submission put isSameTree at MODULE level (correct and clean); the active
# version instead nests it as a local helper inside isSubtree - best-practice for
# a pure sub-routine that no other method needs (scopes it, adds zero class
# surface). David's verbatim submission is preserved as Alt 1. Alt 2 is the
# serialize-to-string O(n+m) approach (the "can you beat O(n*m)?" follow-up).
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
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        # Inner helper: strict lockstep compare of two trees (LC 100). Pure - no
        # instance state - so it lives as a nested local, not a self-method.
        def is_same(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
            if not p and not q:          # both fell off together -> match
                return True
            if not p or not q:           # exactly one fell off -> structure differs
                return False
            return (p.val == q.val
                    and is_same(p.left, q.left)
                    and is_same(p.right, q.right))

        # Outer search: None root -> nowhere left to match -> False (base case).
        # Otherwise try THIS node as the match, else keep searching both children.
        # The children calls must be isSubtree (keep searching deeper), NOT
        # is_same (which would demand an exact match starting at the child) -
        # a match can be buried arbitrarily deep in root.
        if root is None:
            return False
        return (is_same(root, subRoot)
                or self.isSubtree(root.left, subRoot)
                or self.isSubtree(root.right, subRoot))


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Behavior identical; only the ORGANIZATION of the helper changed.
#   - Typed version: isSameTree defined at MODULE level (a standalone pure
#     function), called bare. Correct and clean - a pure function has no reason
#     to be a self-method (that would claim instance state it never uses).
#   - Active version: same logic nested as a LOCAL helper `is_same` inside
#     isSubtree. For a helper no other method needs, this is the cleanest form:
#     it scopes the name to where it's used and keeps the class surface minimal.
#   - Renamed isSameTree -> is_same in the active code: it is now our own local,
#     so snake_case applies (PEP 8). isSubtree stays camelCase - that is
#     LeetCode's fixed method signature (the API), not a naming choice.
#   - Stripped trailing whitespace after `class Solution:` (PEP 8 nit in the
#     typed file).
# Same algorithm, same complexity: O(n*m) time, O(n) space worst-case (skewed
# root, n = |root|, m = |subRoot|), O(log n) balanced.
#
# Design fork (worth banking) - where should the reused LC-100 comparator live?
#   1. Nested local helper (active choice) - best when nothing else needs it.
#   2. Module-level pure function (typed submission) - also clean/testable.
#   3. @staticmethod on Solution - use THIS if it must live in the class, since
#      it touches no self; call it self.is_same(...) and get ~1-to-1 paste reuse
#      from LC 100 WITH correct semantics.
#   4. Plain self-method - the only one to AVOID: it advertises instance state
#      the function never uses. Its sole upside is copy-paste convenience, which
#      is not an engineering reason (@staticmethod gives that + honesty).
#
# The redundant-guard insight (reasoned in Phase 1): an explicit
# `if node.val == subRoot.val` gate before calling is_same buys NOTHING - the
# very first thing is_same does (after its two None base cases) is compare
# node.val == subRoot.val and short-circuit. The guard duplicates that check.
#
# subRoot is None: mathematically the empty tree is a subtree of EVERY tree
# (-> True), but LeetCode constraints guarantee both trees have >= 1 node, so
# this case never fires and needs no special-casing. (Say so out loud in an
# interview - it shows you read the constraints.)


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n*m) time, O(n) space - identical behavior to the active code.
#        isSameTree lives at MODULE level here; the recursive isSubtree calls
#        use self. (they ARE methods) while isSameTree is called bare.
# ---------------------------------------------------------------------------
# def isSameTree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
#     if not p and not q:
#         return True
#     if not p or not q:
#         return False
#     return (p.val == q.val
#             and isSameTree(p.left, q.left)
#             and isSameTree(p.right, q.right))
#
# class Solution:
#     def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
#         if root is None:
#             return False
#         return isSameTree(root, subRoot) or self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)


# ---------------------------------------------------------------------------
# Alt 2: serialize-to-string + substring - O(n + m) time, O(n + m) space
#        The "can you beat O(n*m)?" follow-up. Flatten each tree to a pre-order
#        string with (a) a null marker so structure is captured and (b) a
#        per-node delimiter so VALUE boundaries can't be spoofed, then subRoot is
#        a subtree iff its serialization is a SUBSTRING of root's.
#
#        Two gotchas the markers defend against, both false-positive matches:
#          - No null marker: [1,2] and [1,2,None,3] serialize the same.
#          - No value delimiter: subRoot value 2 would match INSIDE root value 12
#            ("...12..." contains "2"). The leading "^" per node forces the match
#            to start on a node boundary. (Rock-solid alt: KMP the substring, or
#            hash each subtree - but plain `in` is the interview-legible form.)
# ---------------------------------------------------------------------------
# class Solution:
#     def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
#         def serialize(node: Optional[TreeNode]) -> str:
#             if node is None:
#                 return "#"                       # null marker: fixes structure
#             # "^" delimits each node -> value boundaries can't be spoofed
#             return f"^{node.val} {serialize(node.left)} {serialize(node.right)}"
#
#         return serialize(subRoot) in serialize(root)
