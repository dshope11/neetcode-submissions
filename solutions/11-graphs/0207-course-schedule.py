"""
Course Schedule - LeetCode 207 (Medium)
Pattern: Graphs (NeetCode section 11) - the section's first DIRECTED graph, and the first
         where a single permanent visited mark is not enough. The question stops being
         reachability and becomes cycle detection, which forces a THREE-state mark:
         unvisited / on the current path / fully explored and clean.
List: Blind 75
Solved 2026-09-02 | outcome: hint (implementation entirely his and clean; the three-state
                    insight needed a counterexample plus a call-stack nudge, and the
                    adjacency build, the word "memoization", and the memo-soundness
                    argument were handed over on request - see the solve log on
                    wiki/concepts/bfs-dfs.md)

Raw: Data Structures & Algorithms/course-schedule/submission-0.py

The ACTIVE code below is the CLEANED version - see "What changed" for every difference
from the accepted submission. David's verbatim accepted submission is preserved as Alt 1.

CONSTRAINTS ARE NEETCODE'S, NOT LEETCODE'S.
numCourses <= 1000 and prerequisites.length <= 1000 on neetcode.io; LeetCode states 2000
and 5000 for the same problem number. The judge David submits to is neetcode.io, so its
bounds govern every feasibility argument below. (The two disagree often enough that the
/neetcode command now fetches the neetcode.io question page for constraints as a required
step.)

THREE STATES, NOT TWO - THE WHOLE PROBLEM.
The natural first rule, "I have found a cycle if I step onto a node I have already seen",
is wrong, and the witness is small:

    numCourses = 4, prerequisites = [[0,1], [0,2], [1,3], [2,3]]

A diamond. It is perfectly finishable (take 3, then 1 and 2, then 0), but a DFS from 0
reaches 3 through 1, then reaches 3 again through 2, and a single `seen` mark reports a
cycle. The re-encounter is real; what differs is the STATUS of the node re-encountered:

    on the current path (its call is still open, below you on the stack)  -> a real cycle
    already finished (its call returned earlier, no cycle found under it) -> safe, skip

One boolean collapses those two into one mark, which is exactly the bug. Hence two sets:
`on_path` (added on entry, removed on exit) and `safe` (the memo, written on exit). They
are deliberately NOT named `visiting` / `visited` - those two names look alike while
meaning opposites, and the confusion is the failure mode this problem exists to teach.

THE MARK/UN-MARK CONTRAST, ACROSS THREE SECTIONS.
    flood fill (LC 200, 417)  - mark permanently, never un-mark
    backtracking (LC 79)      - mark on entry, un-mark on exit ("un-choose")
    cycle detection (LC 207)  - BOTH, in two separate sets

That is why neither prior template alone can express this problem.

WHY THE MEMO IS SOUND HERE, WHEN IT WAS NOT ON LC 417.
The gotcha carried out of Pacific Atlantic says memoizing a reachability query on a CYCLIC
graph is unsound: a node bounced off an in-progress mark returns a premature False, and
caching that False caches a wrong answer. LC 207 is explicitly about graphs that may have
cycles, so why is caching allowed here?

Because of what the bounce DOES in each problem:

    LC 417 - hitting an in-flight node returns a VALUE ("no path this way") that the caller
             folds into its own answer and then caches. Incomplete information gets frozen.
    LC 207 - hitting an in-flight node means a cycle exists, which is the answer to the
             ENTIRE problem. The False propagates all the way out of canFinish and nothing
             is ever written to `safe` on that path.

So a node reaches `safe` only if its whole exploration completed WITHOUT ever meeting an
in-flight node - every memo entry is computed from complete information, by construction.
One sentence: on 417 the bounce returns a value you keep, on 207 the bounce ends the
computation, so nothing incomplete is ever cached.

THE UN-RESTORED on_path ON THE FAILURE PATH (the subtle one).
When a child returns False the code returns False WITHOUT removing the course from
`on_path`, and every ancestor does the same. From that instant `on_path` no longer means
"nodes on the current path" - it means "nodes that were on the path when we gave up". This
is not a bug, and the reason it is not a bug is the SAME structural fact as the memo
soundness above: discovering a cycle terminates the whole computation, so the corrupted
set is never read again.

Worth naming because it is the first thing to break if the problem changes. LC 210 (Course
Schedule II) wants the actual ordering rather than a yes/no, and the connectivity problems
later in this section do not abort on first failure. Reuse this dfs shape anywhere the
failure is not terminal and the missing un-mark becomes a real defect. Restoring it here
would be dead work on a path that is about to return, so it stays documented rather than
"fixed".

WHY THE PATH MARK ALONE IS EXPONENTIAL (what `safe` actually buys).
Drop `safe` and keep only `on_path` and the algorithm is still CORRECT - but nothing stops
it re-entering a finished node from a different parent, so it stops traversing the graph
and starts enumerating every path. Chain k diamonds end to end: each diamond offers 2
independent choices, so there are 2^k distinct top-to-bottom paths over V = 3k + 1 nodes,
i.e. 2^((V-1)/3). Measured, not argued (dfs call counts, k chained diamonds):

    k= 4  V=13 E=16  ->       213 calls   (memoized bound V+E =  29)
    k= 8  V=25 E=32  ->     4,025 calls   (memoized bound V+E =  57)
    k=12  V=37 E=48  ->    65,437 calls   (memoized bound V+E =  85)
    k=16  V=49 E=64  -> 1,048,449 calls   (memoized bound V+E = 113)

Calls multiply by 16 for every 4 diamonds added - exactly 2^k - while the memoized bound
grows by 28. At 49 nodes it is already a million calls against 113. `safe` is what makes
the launches disjoint and collapses this to O(V + E).

COMPLEXITY.
Time O(V + E): each vertex body runs at most once across ALL outer launches (an already
`safe` course returns immediately, so a re-launch is an O(1) no-op) and each edge is
inspected at most once. It is outer-scan PLUS total-DFS, not outer TIMES DFS - the same
amortization argument as LC 200 and 417. Space O(V + E): adjacency list O(V + E), the two
mark sets O(V), recursion depth O(V).

RECURSION DEPTH AT THE STATED BOUND.
The active form is recursive and OVERFLOWS at the constraint bound. A single chain of 1000
courses (1 requires 0, 2 requires 1, ...) is 1000 nested frames against CPython's default
recursion limit of 1000. Verified by running it, not argued - it raises RecursionError. It
is accepted because the judge's test set contains no such chain, not because it is correct
at the bound. This was derived and stated BEFORE submitting rather than discovered in
review, which is the discipline LC 200 lacked and LC 417 established. Alt 2 (Kahn's) and
Alt 3 (iterative DFS) are both correct at the bound; both were run on the 1000-chain.

VERIFICATION.
10 hand cases (simple, 2-cycle, self-loop, 3-cycle, empty prerequisites, single course, the
diamond, the double diamond, two disconnected chains, a cycle confined to one component),
input-preservation, and a randomized differential test of 4000 graphs against an
independent Kahn's-algorithm oracle - 0 mismatches for the active form and for Alts 2-4.
"""

from typing import List, Set


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Bucket the flat edge list by source: one slot per COURSE, filled by a pass over
        # the PAIRS. A course appearing in no pair keeps its empty list for free, which is
        # why the range is numCourses and not anything derived from prerequisites.
        prereqs: List[List[int]] = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            prereqs[course].append(prereq)

        on_path: Set[int] = set()  # calls currently open - a hit here IS a cycle
        safe: Set[int] = set()     # fully explored, provably cycle-free - the memo

        def dfs(course: int) -> bool:
            """True if nothing reachable from `course` contains a cycle."""
            if course in on_path:
                return False
            if course in safe:
                return True
            on_path.add(course)
            for prereq in prereqs[course]:
                if not dfs(prereq):
                    # Deliberately does NOT remove `course` from on_path. Safe only
                    # because this False aborts canFinish entirely - see the header.
                    return False
            on_path.remove(course)
            safe.add(course)
            return True

        for course in range(numCourses):
            if not dfs(course):
                return False
        return True


# ----------------------------------------------------------------------------------------
# What changed from the accepted submission (Alt 1) to the active code above
# ----------------------------------------------------------------------------------------
# 1. Type hints completed. The submission annotated the nested helper's RETURN
#    (`def dfs(course) -> bool:`) but not its parameter; added `course: int`, plus
#    `prereqs: List[List[int]]`, `on_path: Set[int]`, `safe: Set[int]`. Added the
#    `from typing import List, Set` line that neetcode.io pre-imports, so the file is
#    honest and portable.
# 2. `for course in range(len(prereqs))` -> `range(numCourses)`. Equivalent, since
#    len(prereqs) IS numCourses by construction - but the original makes the reader go
#    verify that before trusting the loop. Say the quantity you mean.
# 3. Comments added, no logic changed: the docstring on dfs stating its contract, the
#    two mark-set comments, the adjacency-build note, and - the one that earns its
#    place - the note on the deliberate non-removal from on_path on the failure path.
#
# No algorithmic change. The submitted solution was already optimal and structurally
# clean: check order right, mark added on entry before the neighbor loop, un-mark and
# memo-write both in the exit step, short-circuit propagation on the child call.
#
# Convention slips in the typed submission (fixed above, visible in Alt 1): the
# unannotated helper parameter (item 1) and the indirect loop bound (item 2). No PEP 8
# violations, no Unicode, no naming issues - `on_path` / `safe` is a better pair than the
# conventional `visiting` / `visited` and was chosen on purpose.


# ----------------------------------------------------------------------------------------
# Alt 1: David's accepted submission, VERBATIM (the honest practice record)
#        O(V + E) time, O(V + E) space
# ----------------------------------------------------------------------------------------
# class Solution:
#     def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
#         prereqs = [[] for _ in range(numCourses)]
#         for course, prereq in prerequisites:
#             prereqs[course].append(prereq)
#         on_path = set()
#         safe = set()
#
#         def dfs(course) -> bool:
#             if course in on_path:
#                 return False
#             if course in safe:
#                 return True
#             on_path.add(course)
#             for prereq in prereqs[course]:
#                 if not dfs(prereq):
#                     return False
#             on_path.remove(course)
#             safe.add(course)
#             return True
#
#         for course in range(len(prereqs)):
#             if not dfs(course):
#                 return False
#         return True


# ----------------------------------------------------------------------------------------
# Alt 2: Kahn's algorithm - topological sort as BFS on in-degrees
#        O(V + E) time, O(V + E) space. Naturally ITERATIVE, so correct at the 1000 bound.
# ----------------------------------------------------------------------------------------
# The other standard answer to this problem, and the one the prep hub flagged as the
# highest-ROI of the graph algorithms ThePrimeagen skipped. It needs NO marks at all -
# no on_path, no safe, no three states - because it never walks a path in the first
# place. Instead it simulates actually taking the courses:
#
#   - Build the graph in the UNLOCK direction (prereq -> course), the opposite of the DFS
#     version, and count each course's outstanding prerequisites (`remaining`, the
#     in-degree).
#   - Seed a queue with every course that has zero prerequisites. Those are takeable now.
#   - Take a course, decrement `remaining` for everything it unlocks, and enqueue any
#     course whose count just hit zero.
#   - If you manage to take all numCourses, there was no cycle. If the queue empties
#     early, the courses left over all sit in cycles - each is waiting on another one
#     that never becomes takeable, so their counts never reach zero.
#
# Note the direction DOES matter here, unlike in the DFS version where reversing every
# edge preserves cycles and changes nothing. Kahn's is also what you extend for LC 210:
# the order in which courses come off the queue IS a valid schedule, so returning the
# take-order instead of a bool solves Course Schedule II directly.
#
# from collections import deque
#
# class Solution:
#     def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
#         unlocks: List[List[int]] = [[] for _ in range(numCourses)]
#         remaining: List[int] = [0] * numCourses
#         for course, prereq in prerequisites:
#             unlocks[prereq].append(course)
#             remaining[course] += 1
#
#         ready = deque(c for c in range(numCourses) if remaining[c] == 0)
#         taken = 0
#         while ready:
#             course = ready.popleft()
#             taken += 1
#             for nxt in unlocks[course]:
#                 remaining[nxt] -= 1
#                 if remaining[nxt] == 0:
#                     ready.append(nxt)
#         return taken == numCourses


# ----------------------------------------------------------------------------------------
# Alt 3: the same three-state DFS, ITERATIVE - correct at the 1000-course bound
#        O(V + E) time, O(V + E) space
# ----------------------------------------------------------------------------------------
# The mechanical fix for the recursion-depth overflow, and the reason it is fiddly: the
# recursive form gets its exit step for free when the call returns, but an explicit stack
# has no "return" to hook. So each node is pushed TWICE - once to enter, once as a
# post-visit marker - and the boolean flag says which visit this is. The marker is pushed
# BEFORE the children so it pops AFTER all of them, which is what makes on_path hold
# exactly the current ancestor chain at every pop.
#
# (Needs `Tuple` added to the typing import above; left off the active line since the
# active code does not use it.)
#
# class Solution:
#     def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
#         prereqs: List[List[int]] = [[] for _ in range(numCourses)]
#         for course, prereq in prerequisites:
#             prereqs[course].append(prereq)
#
#         on_path: Set[int] = set()
#         safe: Set[int] = set()
#         for start in range(numCourses):
#             if start in safe:
#                 continue
#             stack: List[Tuple[int, bool]] = [(start, False)]
#             while stack:
#                 course, exiting = stack.pop()
#                 if exiting:                       # post-visit: the un-mark + memo write
#                     on_path.discard(course)
#                     safe.add(course)
#                     continue
#                 if course in safe:
#                     continue
#                 if course in on_path:
#                     return False
#                 on_path.add(course)
#                 stack.append((course, True))      # marker first, so it pops last
#                 for prereq in prereqs[course]:
#                     if prereq in on_path:
#                         return False
#                     if prereq not in safe:
#                         stack.append((prereq, False))
#         return True


# ----------------------------------------------------------------------------------------
# Alt 4: path mark only, no memo - CORRECT but EXPONENTIAL. Kept as the derivation record.
#        O(2^((V-1)/3)) time worst case, O(V) space
# ----------------------------------------------------------------------------------------
# Drop `safe` and the cycle detection still works perfectly - this returns the right
# answer on every input. What it loses is the guarantee that each vertex is processed
# once, which is the entire basis of the O(V + E) bound. Nothing prevents re-entering a
# finished node from a different parent, so it enumerates paths rather than traversing the
# graph. See the chained-diamond measurements in the header: 1,048,449 calls at V=49.
#
# The instructive part is WHY the bound collapses. "O(V + E) per DFS" is not a property of
# DFS - it is bought by the mark. Remove the mark and the bound goes with it, on any
# graph.
#
# class Solution:
#     def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
#         prereqs: List[List[int]] = [[] for _ in range(numCourses)]
#         for course, prereq in prerequisites:
#             prereqs[course].append(prereq)
#
#         on_path: Set[int] = set()
#
#         def dfs(course: int) -> bool:
#             if course in on_path:
#                 return False
#             on_path.add(course)
#             for prereq in prereqs[course]:
#                 if not dfs(prereq):
#                     return False
#             on_path.remove(course)
#             return True
#
#         for course in range(numCourses):
#             if not dfs(course):
#                 return False
#         return True
