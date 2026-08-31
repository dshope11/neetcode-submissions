"""
Clone Graph - LeetCode 133 (Medium)
Pattern: Graphs (NeetCode section 11) - DFS over an EXPLICIT node-object graph, where the
         `visited` structure is a dict old_node -> new_node rather than a boolean. The map
         does two jobs at once: it is the cycle guard AND the old-to-new lookup table, and
         that dual role is the whole problem.
List: Blind 75
Solved 2026-08-30 | outcome: hint (implementation clean and unassisted; the design
                    discussion needed pushes - see the solve log on wiki/concepts/bfs-dfs.md)

Raw: Data Structures & Algorithms/clone-graph/submission-0.py

The ACTIVE code below is the CLEANED version - see "What changed" for every difference
from the accepted submission. David's verbatim accepted submission is preserved as Alt 1.

Style notes on the submission: the local `copy` shadows the stdlib `copy` MODULE (the third
shadowing category already documented in wiki/topics/coding-interview-prep.md - harmless
here only because nothing in this file imports it, which is exactly why that category is
the dangerous one: the breakage is invisible in the file where you did it). The nested
`def dfs(node)` shadows cloneGraph's own `node` parameter - a fourth category, which never
breaks but forces the reader to prove `return dfs(node)` resolves to the outer name. Both
renamed in the active code, both visible in Alt 1.

THE TYPE HINT THAT LIED. The submission annotates the helper `def dfs(node) -> Optional['Node']`.
Inside `dfs`, `node` can never be None: the outer guard catches the only None entry point,
and a neighbor list never contains None. So the helper always returns a real Node, and the
Optional is over-wide. This is not harmless caution - it is what manufactured the
`if neighbor_copy is not None:` branch that sat in the draft before submission. An
over-permissive annotation does not make code safer; it invents dead branches to satisfy a
case that cannot occur. The active code narrows it to `(current: "Node") -> "Node"`; only
the outer cloneGraph is genuinely Optional.

WHY THE RECURSIVE FORM IS SAFE HERE, unlike LC 200. Node count is capped at 100, so the
recursion is at most 100 deep against CPython's default limit of 1000. The stack-overflow
trap that makes the recursive LC 200 solution dishonest at its stated bound (m, n <= 300 ->
~90000 deep) simply does not apply. Worth checking the constraint and saying so out loud,
rather than assuming either way.
"""

# Optional is imported here so the file is honest/portable; on neetcode.io it is
# pre-imported, so the typed submission omitted it. `deque` is for Alt 3.
from collections import deque
from typing import Optional


# Definition for a Node.
# class Node:
#     def __init__(self, val = 0, neighbors = None):
#         self.val = val
#         self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        # Guard before allocating - the empty-graph case (adjList = [], an
        # explicit test case) should not build a dict and discard it.
        if node is None:
            return None

        # original node -> its clone. This single dict answers BOTH questions:
        # "have I been here?" (membership) and "what is this node's copy?"
        # (value). LC 200's `seen` only had to answer the first, which is why a
        # bare boolean grid sufficed there and does not suffice here.
        seen = {}

        def dfs(current: "Node") -> "Node":
            """Return the clone of `current`, building it if this is the first visit.

            The early return below is the cycle guard and the lookup at once -
            which is why the neighbor loop needs no `if neighbor not in seen`
            test of its own. Both iterative forms (Alts 2 and 3) DO need that
            test inline, because they have no recursive call to fold it into.
            """
            if current in seen:
                return seen[current]

            clone = Node(current.val)
            # Registered BEFORE recursing. This ordering is the entire reason
            # the walk terminates on a cycle: by the time any neighbor looks
            # back at `current`, it is already in the map and returns instantly.
            # Register on DISCOVERY, never on processing.
            seen[current] = clone

            # Each clone's neighbor list is built from ITS OWN original list.
            # The undirected symmetry is already encoded in the input (an edge
            # appears in both endpoints' lists), so it reproduces for free -
            # manually wiring the reverse edge would double-count it.
            for neighbor in current.neighbors:
                clone.neighbors.append(dfs(neighbor))

            return clone

        return dfs(node)


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code above)
# ---------------------------------------------------------------------------
# 1. Local `copy` -> `clone`. `copy` is a stdlib module name (the documented
#    third shadowing category, alongside `enum`, `heapq`, `queue`, `math`).
# 2. Nested helper parameter `node` -> `current`, so it no longer shadows
#    cloneGraph's own `node`. Fourth shadowing category: an enclosing-scope
#    name. Never breaks; costs the reader a proof.
# 3. `def dfs(node) -> Optional['Node']` -> `def dfs(current: "Node") -> "Node"`.
#    Added the missing parameter annotation AND dropped the false Optional on
#    the return - see the header note on the type hint that lied.
# 4. `seen = {}` moved BELOW the None guard (it was allocated and discarded on
#    the empty-graph path).
# 5. Added `from typing import Optional` and `from collections import deque`
#    (the latter for Alt 3), which neetcode.io supplies implicitly.
# 6. Added the docstring on `dfs` naming why the neighbor loop needs no
#    membership test, and the header notes on recursion depth and the type hint.
# No logic changed.
#
# Complexity of the active code:
#   Time  O(V + E). Every vertex's body runs exactly once - the early return
#         makes every later arrival O(1) - and at each vertex you iterate only
#         THAT vertex's neighbor list, deg(v), not all E edges. Summed over all
#         vertices, sum_v deg(v) = 2E on an undirected graph, so the edge work
#         is O(E) in total. This is the "counting loops lies" trap from the
#         Dijkstra analysis: the inner loop sits inside the vertex walk but does
#         NOT multiply by V, because the edges are PARTITIONED across the
#         vertices rather than re-walked at each one. O(V*E) is the wrong answer.
#   Space O(V + E), three contributors: the `seen` map is O(V), the recursion
#         stack is O(V) worst case (a path-shaped graph), and the returned graph
#         itself is O(V + E) - which dominates. Note the output is not "extra"
#         space you could optimize away; it is the deliverable.


# ---------------------------------------------------------------------------
# Alt 1: David's accepted submission, verbatim. O(V + E) time, O(V + E) space.
# ---------------------------------------------------------------------------
# class Solution:
#     def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
#         seen = {}
#         if node is None:
#             return None
#
#         def dfs(node) -> Optional['Node']:
#             if node in seen:
#                 return seen[node]
#             copy = Node(node.val)
#             seen[node] = copy
#             for neighbor in node.neighbors:
#                 copy.neighbors.append(dfs(neighbor))
#             return copy
#
#         return dfs(node)


# ---------------------------------------------------------------------------
# Alt 2: iterative DFS with an explicit stack. O(V + E) time, O(V + E) space.
#
# The recursion unrolled: the stack holds nodes whose clones EXIST but whose
# neighbor lists are not yet filled. Two structural differences from the
# recursive form, both consequences of losing the recursive call:
#
#   (a) The membership test moves INTO the loop. The recursive version folds it
#       into `if current in seen: return seen[current]`; here you must ask
#       `if neighbor not in clones` explicitly before creating and pushing.
#   (b) The seed is a two-part move - create the entry node's clone AND push the
#       entry node - because the loop body only ever creates clones for
#       NEIGHBORS. Nothing else would ever create the first one.
#
# The load-bearing line is `clones[neighbor] = Node(...)` sitting immediately
# above `stack.append(neighbor)`: register at discovery, in the same breath as
# the push. Defer it to pop time and clones[neighbor] would not exist on the
# line below, where it is needed to fill the current node's neighbor list.
# ---------------------------------------------------------------------------
# class Solution:
#     def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
#         if node is None:
#             return None
#
#         clones = {node: Node(node.val)}       # seed: clone the entry node
#         stack = [node]
#         while stack:
#             current = stack.pop()             # pop() = stack = DFS order
#             for neighbor in current.neighbors:
#                 if neighbor not in clones:
#                     clones[neighbor] = Node(neighbor.val)   # register at
#                     stack.append(neighbor)                  # DISCOVERY
#                 clones[current].neighbors.append(clones[neighbor])
#         return clones[node]


# ---------------------------------------------------------------------------
# Alt 3: iterative BFS with a deque. O(V + E) time, O(V + E) space.
#
# Identical to Alt 2 with `popleft()` in place of `pop()` - the one-character
# difference between DFS and BFS once the recursion is gone (stack vs queue,
# the only structural difference between the two traversals). Traversal ORDER
# is irrelevant to this problem: every node is cloned and every edge is copied
# either way, so unlike a shortest-path problem there is nothing to choose
# between them on correctness. Pick either; say why it does not matter.
#
# THE MARKING INSTANT IS THE SAME RULE AS LC 200's BFS: register on enqueue,
# never on dequeue. Mark-on-dequeue breaks this problem harder than it broke
# 200 - there it merely inflated the queue (a node with k unvisited neighbours
# gets pushed k times); here it is an outright correctness failure, because
# `clones[neighbor]` on the next line would not yet exist when the current
# node's neighbor list is being built.
# ---------------------------------------------------------------------------
# class Solution:
#     def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
#         if node is None:
#             return None
#
#         clones = {node: Node(node.val)}
#         queue = deque([node])
#         while queue:
#             current = queue.popleft()         # popleft() = queue = BFS order
#             for neighbor in current.neighbors:
#                 if neighbor not in clones:
#                     clones[neighbor] = Node(neighbor.val)   # register on
#                     queue.append(neighbor)                  # ENQUEUE
#                 clones[current].neighbors.append(clones[neighbor])
#         return clones[node]
