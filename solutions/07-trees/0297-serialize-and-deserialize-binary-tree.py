# Serialize and Deserialize Binary Tree - LC 297 - Hard - (NeetCode 150, Blind 75)
# Pattern: Trees (recursive DFS). A NEW Trees sub-pattern vs the aggregate-up /
#          side-channel work (543/124): full-tree ENCODE <-> DECODE round-trip.
#          serialize = pre-order DFS emitting str(val) or "N" for a missing child,
#          comma-joined into one string. deserialize = split on commas, then a
#          pre-order DFS that consumes tokens left-to-right via a self-advancing
#          pointer, rebuilding the exact tree. The "N" null markers are what let
#          a SINGLE pre-order pass reconstruct unambiguously.
# Solved 2026-07-26 | outcome: solo
#
# Raw: Data Structures & Algorithms/serialize-and-deserialize-binary-tree/submission-0.py
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was correct and optimal. Cleanups are style-only - drop a redundant
# parameter, rename a fossil variable, drop a dead return, tidy the token-advance,
# and add type hints (incl. on the nested helpers, per David's habit-building
# choice to type his own methods). The token consumer stays the self.i index that
# David actually wrote. Alt 1 = his verbatim accepted submission; Alt 2 = the
# local iter()+next() consumer (no instance state, nothing to reset); Alt 3 = the
# deque+popleft() consumer (the concrete "why not list.pop(0)" contrast). All
# three consumers were reasoned in Phase 1.
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


class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        result = []

        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                result.append("N")          # null marker: encodes the structure
                return
            result.append(str(node.val))    # bare token; ",".join owns delimiters
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(result)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        self.i = 0                          # reset per call: safe to reuse Codec
        tokens = data.split(",")

        def dfs() -> Optional[TreeNode]:
            val = tokens[self.i]
            self.i += 1                     # advance ONCE, right after reading
            if val == "N":                  # null marker IS the base case -
                return None                 # a well-formed stream never overruns
            node = TreeNode(int(val))       # tokens are strings -> int()
            node.left = dfs()               # pre-order: left subtree consumes its
            node.right = dfs()              # own tokens before right pointer reads
            return node

        return dfs()


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Same algorithm, same complexity: O(n) time and O(n) space BOTH directions.
# Time - each node + each null marker is emitted/consumed exactly once, and the
# self.i index makes every consume O(1) (contrast list.pop(0), which is O(n) ->
# O(n^2) overall; see Alt 3). Space - the output string / token list is O(n) and
# dominates the O(h) recursion stack (h = O(log n) balanced, O(n) skewed).
# Style-only cleanups:
#   - deserialize's helper took `data_list` as a PARAMETER it didn't need: the
#     nested dfs already closes over `tokens` from the enclosing scope (exactly
#     as serialize's dfs reads `result` without it being passed). Dropped the
#     parameter so both halves are consistent.
#   - Renamed `c` -> `val`. `c` was a fossil from an earlier draft that indexed
#     single CHARACTERS off the raw string (data[self.i]); it holds a full token
#     now, so `c` misled.
#   - Hoisted `self.i += 1` to fire ONCE right after the read, instead of a
#     duplicated increment inside each branch.
#   - Dropped a dead trailing `return` after serialize's two recursive calls
#     (the function falls off the end there anyway; the None-branch return stays,
#     it is load-bearing).
#   - Added type hints, including on the nested helpers (dfs(node) -> None and
#     dfs() -> Optional[TreeNode]).
# No convention slips in the typed version: all snake_case, "N" markers, and the
# self.i = 0 reset was already at the TOP of deserialize (which is what makes the
# Codec safe to call twice - see the insight below).
#
# Bugs that bit during the solve (all caught + fixed before submission):
#   - str has no .append(): the first serialize draft did self.string = "" then
#     self.string.append(...). Fixed by switching to the list accumulator
#     (result = []; result.append(...); ",".join(result)) - the O(n) way. A
#     string accumulator (s += ...) would be O(n^2) since each += copies.
#   - Indexed the raw string, not the tokens: deserialize split into data_list
#     but then read data[self.i] (a single CHARACTER) instead of
#     data_list[self.i] (a whole token) - so "10" would read as "1". Fixed to
#     index the token list.
#   - Re-split every call: data.split(",") was inside the recursion (O(n) per
#     call -> O(n^2)). Hoisted the split to the outer method so it runs once.
#   - `is` vs `==`: used `if c is "N"` (identity) instead of `== "N"` (value).
#     Works by accident when Python interns the literal, but wrong - fixed to ==.
#
# Key insight - why ONE traversal suffices here, when LC 105 needed TWO:
#   On LC 105 (Construct from Preorder + Inorder) a bare pre-order sequence is
#   AMBIGUOUS - you can't tell where the left subtree ends, so you need inorder
#   to locate the split. Here you rebuild from a SINGLE pre-order pass because the
#   "N" null markers write the structure INTO the stream: every "N" says exactly
#   where a subtree terminates, so the recursion always knows when to pop back up.
#   The trade: pay O(n) extra tokens (the nulls) to buy an unambiguous one-pass
#   decode. 105 had to INFER the boundary; 297 ENCODES it.
#
# Why the base case is the null marker, not a bounds check:
#   For a well-formed pre-order-with-nulls string, every subtree consumes exactly
#   its own tokens and each branch terminates at an "N". The recursion structure
#   guarantees the top-level call consumes all len(tokens) tokens and stops -
#   self.i never runs past the end, so no `if self.i >= len(tokens)` guard is
#   needed. The `val == "N": return None` branch IS the base case.
#
# Why self.i = 0 lives at the TOP of deserialize (not the class body):
#   At CLASS-BODY scope there is no `self` yet (no instance exists during class
#   definition) - `self.i = 0` there is a NameError; a bare `i = 0` would make a
#   class attribute. Putting `self.i = 0` at the top of deserialize resets it per
#   call, so calling deserialize twice on the SAME Codec works. (LeetCode's driver
#   uses fresh instances, so even an unreset self.i would pass there - but the
#   reset is the robust habit.) The iter() consumer in Alt 2 sidesteps this
#   entirely: no instance state to reset.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(n) time, O(n) space
#        Correct and optimal. Differences from the active code are all style:
#        helper takes an unused data_list param, variable named `c`, self.i
#        incremented inside each branch, no type hints on the nested helper.
# ---------------------------------------------------------------------------
# class Codec:
#     def serialize(self, root: Optional[TreeNode]) -> str:
#         result = []
#         def dfs_serialize(node):
#             if node is None:
#                 result.append("N")
#                 return
#             result.append(str(node.val))
#             dfs_serialize(node.left)
#             dfs_serialize(node.right)
#             return
#         dfs_serialize(root)
#         return ",".join(result)
#
#     def deserialize(self, data: str) -> Optional[TreeNode]:
#         self.i = 0
#         data_list = data.split(",")
#         def dfs_deserialize(data_list):
#             c = data_list[self.i]
#             if c == "N":
#                 node = None
#                 self.i += 1
#             else:
#                 node = TreeNode(int(c))
#                 self.i += 1
#                 node.left = dfs_deserialize(data_list)
#                 node.right = dfs_deserialize(data_list)
#             return node
#         return dfs_deserialize(data_list)


# ---------------------------------------------------------------------------
# Alt 2: local iter() + next() consumer - O(n) time, O(n) space
#        The cleanest deserialize: wrap the tokens in an ITERATOR and pull with
#        next(). The iterator is self-advancing, so there is no index and NO
#        instance state to reset - the "deserialize twice on one Codec" footgun
#        disappears by construction. next() is O(1). serialize is unchanged.
# ---------------------------------------------------------------------------
# class Codec:
#     def deserialize(self, data: str) -> Optional[TreeNode]:
#         it = iter(data.split(","))
#
#         def dfs() -> Optional[TreeNode]:
#             val = next(it)
#             if val == "N":
#                 return None
#             node = TreeNode(int(val))
#             node.left = dfs()
#             node.right = dfs()
#             return node
#
#         return dfs()


# ---------------------------------------------------------------------------
# Alt 3: deque + popleft() consumer - O(n) time, O(n) space
#        Makes the "why not list.pop(0)" point concrete. list.pop(0) is O(n) (a
#        Python list is a contiguous array, so front-removal shifts every element
#        down one) -> O(n^2) over n tokens. collections.deque.popleft() is O(1),
#        so this stays O(n). Functionally identical to Alt 2; use whichever reads
#        clearest. serialize is unchanged.
# ---------------------------------------------------------------------------
# from collections import deque
#
# class Codec:
#     def deserialize(self, data: str) -> Optional[TreeNode]:
#         tokens = deque(data.split(","))
#
#         def dfs() -> Optional[TreeNode]:
#             val = tokens.popleft()
#             if val == "N":
#                 return None
#             node = TreeNode(int(val))
#             node.left = dfs()
#             node.right = dfs()
#             return node
#
#         return dfs()
