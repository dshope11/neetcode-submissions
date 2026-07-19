# Binary Tree Level Order Traversal - LC 102 - Medium - [Blind 75]
# Pattern: Trees. The canonical PER-LEVEL BFS. A queue does a normal
#          breadth-first walk, but each outer pass drains EXACTLY one level by
#          snapshotting the queue length before popping, so the output groups
#          node values by depth: [[level0], [level1], ...].
# Solved 2026-07-18 | outcome: solo
#
# Raw: Data Structures & Algorithms/level-order-traversal-of-binary-tree/submission-0.py
#
# Active code below is the CLEANED version (per the review): the only change from
# the accepted submission is cosmetic renaming (outer_list -> result,
# inner_list -> level) so the code narrates its intent. The algorithm is already
# the optimal shape - nothing to improve there. David's verbatim submission is
# preserved as Alt 1. Alt 2 is the recursive-DFS form (the "without a queue?"
# follow-up): O(n) time but O(h) call-stack space instead of the BFS queue.
#
# Optional / List are imported here so the file is honest/portable; on
# neetcode.io they are pre-imported, so the typed submission omitted them.
from collections import deque
from typing import List, Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:              # empty tree -> no levels -> [] (not [[]])
            return []
        q = deque([root])
        result = []
        while q:
            # Snapshot the width of the CURRENT level before we start popping.
            # range(len(q)) captures len(q) once, so the children we append below
            # (next level) don't bleed into this pass.
            level_size = len(q)
            level = []
            for _ in range(level_size):
                node = q.popleft()            # the dequeue IS the visit
                level.append(node.val)
                # Guarding on enqueue keeps None out of q, which is what makes
                # level_size an ACCURATE count (append unconditionally and you'd
                # over-count and need a None-check on every dequeue instead).
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            result.append(level)
        return result


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Algorithm identical - this is already the optimal BFS-by-level shape. Only
# naming changed for readability:
#   - outer_list -> result   (the thing we return)
#   - inner_list -> level    (reads as intent: "the nodes at this depth")
# No convention slips in the typed version: snake_case throughout, `is None`
# guard, deque (not list.pop(0)), PEP 8 clean.
# Complexity unchanged: O(n) time (each node enqueued/dequeued once); space is
# the queue peak = O(n) worst-case on a BALANCED tree (bottom level ~ n/2 nodes),
# O(1) on a fully skewed tree - the OPPOSITE worst-case shape from DFS. Plus the
# O(n) output list, which is unavoidable (it holds every value).


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(n) space - identical behavior to the active code.
# ---------------------------------------------------------------------------
# class Solution:
#     def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
#         if root is None:
#             return []
#         q = deque([root])
#         outer_list = []
#         while q:
#             level_size = len(q)
#             inner_list = []
#             for _ in range(level_size):
#                 node = q.popleft()
#                 inner_list.append(node.val)
#                 if node.left:
#                     q.append(node.left)
#                 if node.right:
#                     q.append(node.right)
#             outer_list.append(inner_list)
#         return outer_list


# ---------------------------------------------------------------------------
# Alt 2: recursive DFS with a depth index - O(n) time, O(h) space
#        The "can you do it WITHOUT a queue?" follow-up. A pre-order DFS still
#        produces level-order OUTPUT because each node is filed into result[depth]
#        by its depth, not by visit time. depth == len(result) means "first node
#        ever seen at this depth" -> start a fresh level list.
#
#        Space trade vs BFS: no queue, but the call stack is O(h) - O(log n)
#        balanced, O(n) on a skewed tree. So DFS and BFS swap which tree shape is
#        their worst case (skewed vs balanced); neither beats O(n) worst-case.
# ---------------------------------------------------------------------------
# class Solution:
#     def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
#         result = []
#
#         def dfs(node: Optional[TreeNode], depth: int) -> None:
#             if node is None:
#                 return
#             if depth == len(result):       # first node at this depth -> new level
#                 result.append([])
#             result[depth].append(node.val)
#             dfs(node.left, depth + 1)
#             dfs(node.right, depth + 1)
#
#         dfs(root, 0)
#         return result
