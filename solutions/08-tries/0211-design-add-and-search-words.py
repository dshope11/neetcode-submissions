# Design Add and Search Words Data Structure - LC 211 - Medium - (NeetCode 150, Blind 75)
# Pattern: Tries. The SECOND problem of the Tries section and its real
#          algorithmic step: LC 208's structure unchanged, but search() gains a
#          '.' wildcard that matches any single letter. That turns the
#          straight-line walk-down into a BRANCHING search - at a '.' every
#          existing child is a candidate, so one search path becomes up to 26.
#          The trie's node model, insert, and the "path exists != word exists"
#          base case all carry over verbatim from 208; only the walk changes
#          shape.
# Solved 2026-07-29 | outcome: hint
#
# Raw: Data Structures & Algorithms/design-word-search-data-structure/submission-0.py
#
# Note on the class name: neetcode.io files this under the slug
# design-word-search-data-structure; both LeetCode and neetcode.io name the
# class WordDictionary with methods addWord / search. The camelCase addWord is
# PLATFORM-MANDATED - matching a given signature is correct, not a style slip.
#
# Active code below is the CLEANED version (see "What changed"). The accepted
# submission was correct and optimal; the changes are one idiom swap
# (or-accumulator -> any()), one flattening (dropping a dead else), and PEP 8.
# Alt 1 = David's verbatim accepted submission. Alt 2 = the iterative
# frontier-set (BFS-style) reformulation - same time, different space profile.
# Alt 3 = length-bucketed tries, the mitigation for the adversarial worst case.
# Alt 4 = the naive flat-list baseline, for the complexity comparison.
#
# No typing imports needed: the active code uses the built-in generic
# dict[str, "TrieNode"] (Python 3.9+). On 3.8 or earlier this would need Dict
# from typing. Alt 3's roots.get() returns an Optional[TrieNode] and would want
# `from typing import Optional` to annotate.


class TrieNode:
    def __init__(self) -> None:
        # Instance state, NOT class-body attributes: a class-body `children = {}`
        # is created once at class-definition time and SHARED by every node.
        # (Carried over from LC 208 - same node, unchanged.)
        self.children: dict[str, "TrieNode"] = {}
        self.is_word: bool = False               # "a word ENDS here"


class WordDictionary:

    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()         # root holds no character

    def addWord(self, word: str) -> None:
        # Identical to LC 208's insert. addWord never contains '.' (per the
        # constraints), so the insert side needs no wildcard handling at all -
        # the asymmetry between add and search is the whole problem.
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()   # missing child -> CREATE
            curr = curr.children[ch]
        curr.is_word = True                      # mark AFTER the loop

    def search(self, word: str) -> bool:

        def dfs(i: int, node: TrieNode) -> bool:
            # i indexes into word; node is where we are in the trie. Passing an
            # INDEX rather than a slice matters: word[i + 1:] would copy the
            # remaining characters on every level, multiplying the whole
            # traversal by O(L). Same trap as building a string with `s += ch`.
            if i == len(word):
                return node.is_word              # path exists != word exists
            ch = word[i]
            if ch == ".":
                # Branch over the children that ACTUALLY EXIST - which is why
                # the branch factor is "at most 26", not 26. A node with no
                # children makes the generator empty and any() returns False,
                # so the empty case needs no special handling.
                return any(dfs(i + 1, child) for child in node.children.values())
            if ch not in node.children:
                return False                     # missing child -> BAIL
            return dfs(i + 1, node.children[ch])

        return dfs(0, self.root)


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Same algorithm, same complexity. Three substantive edits plus PEP 8:
#   - The '.' branch's or-accumulator collapsed into any(). The submitted form
#     was `found = False` then `found = found or dfs(i + 1, child)` in a loop,
#     then `return found`. That is CORRECT, and Python's `or` does short-circuit
#     the recursive CALL once found is True - but the LOOP keeps iterating,
#     spinning through the remaining siblings doing nothing but the or-test.
#     any() over a generator short-circuits AND stops iterating (exhausting the
#     generator halts on the first True), so it is strictly better: same
#     semantics, no accumulator, and it reads as the question being asked
#     ("does any branch match") rather than "accumulate every branch's result".
#     Free asymptotically either way - up to 25 wasted loop steps per dot level.
#   - Dropped the `else:` and inverted to guard-clause style. The submitted
#     shape was `if ch != '.': ... else: ...`, but the if-branch ALWAYS returns,
#     so the else bought a nesting level for nothing. Testing the positive
#     condition (`if ch == "."`) puts the special case first and flattens the
#     body to three straight-line returns.
#   - `match` (the accumulator) deleted by the any() swap. Worth naming anyway:
#     `match` is a SOFT KEYWORD in Python 3.10+ (structural pattern matching).
#     Legal as an identifier, but shadowing one is a smell some linters flag,
#     and `found` would have said what it meant.
#   - PEP 8: spaces around the binary operator (`i+1` -> `i + 1`); two blank
#     lines between the top-level classes (one in the submission - the same
#     slip as in LC 208).
# Type hints were already complete in the submission, INCLUDING the nested
# dfs helper - the standing convention met without a reminder. Naming was clean
# otherwise; no Unicode.
#
# Not changed (deliberately): the recursive shape. The frontier-set iterative
# form (Alt 2) is equally valid but has a worse space profile, and the
# length-bucketing (Alt 3) is a design change, not a cleanup.
#
# ---------------------------------------------------------------------------
# The sharp point - why no visited set is needed, and why that IS the bound
# ---------------------------------------------------------------------------
# This is a branching search with up to 26^d live paths, no memoization and no
# visited set. In a general graph that would be a bug. Here it is provably
# unnecessary, for a reason worth stating precisely:
#
#   i is a pure function of recursion depth. Every call at depth d has i == d,
#   so `node` always sits at trie depth exactly i. And a trie is a TREE: each
#   node has exactly one root path. Therefore the pair (i, node) can be
#   generated AT MOST ONCE per search - reaching node requires having matched
#   the unique character path to it, and each call descends exactly one level.
#
# That is not just tidiness - it is what makes the N side of the
# min(26^d, N) bound VALID. 26^d counts paths in a hypothetically complete
# trie; total work is also ceilinged by the node count only because no node is
# ever re-expanded. Break the tree property - e.g. minimize the trie into a
# DAWG (Directed Acyclic Word Graph / DAFSA), which shares SUFFIXES as well as
# prefixes by merging identical subtrees - and a node becomes reachable by many
# paths, so a wildcard search would re-explore it and would genuinely need
# memoization on (i, node). The trie's redundancy is what buys the
# no-visited-set property. (Tradeoff: a DAWG is far smaller - it is the classic
# Scrabble engine structure, Appel & Jacobson 1988 - but a node no longer
# corresponds to a unique prefix, so you cannot hang per-word data on it.)
#
# The depth-synchronization also explains why Alt 2 works at all: all live
# nodes are always at one uniform level, so "everything reachable at index i"
# is a well-defined frontier you can expand level by level.
#
# ---------------------------------------------------------------------------
# Complexity
# ---------------------------------------------------------------------------
# L = length of the argument string, N = total nodes in the trie,
# W = number of stored words, d = number of '.' characters in the query.
#
#   addWord   O(L) time, O(L) new nodes worst case
#   search    O(min(26^d, N)) time, O(L) AUXILIARY space
#   structure O(total characters stored) worst case; shared prefixes only help
#
# On the min(): with L <= 25 and <= 10^4 calls, 26^d is astronomically larger
# than any trie those calls can build, so N is the REAL bound and 26^d is
# quoted only to show the branching is understood. The honest headline is that
# an all-dots search degenerates to a FULL TRAVERSAL of the trie.
#
# On the space: O(L) auxiliary, driven by recursion DEPTH, which is bounded by
# len(word) (each call consumes exactly one character) - NOT by the size of the
# trie and NOT by the branching. The 26-way fan-out costs nothing in space
# because DFS explores one path at a time and unwinds; only one root-to-current
# chain is ever live. Alt 2 trades exactly this away.
#
# Why a trie rather than a hash set (the anti-trigger, extended from 208):
#   In 208 the set MATCHED the trie on insert and exact search (string hashing
#   reads every character, so both are O(L)) and lost only on startsWith,
#   O(W * L) vs O(L). Here the wildcard breaks the tie decisively: a flat set
#   or list cannot use the structure at all and must scan every stored word,
#   O(W * L) per search (Alt 4). The trie's advantage is that a matched prefix
#   is shared work and a missing child DEAD-ENDS a whole subtree of candidates.
#
# Edge cases - all handled with NO special-casing:
#   - Query longer than anything stored: bails at the first missing child (or
#     the first dot with no children).
#   - Query shorter than a stored word: lands on a real node with
#     is_word == False -> correctly False. Path existence is not word existence.
#   - A dot at a node with no children: empty generator, any() -> False.
#   - Query that is all dots: full traversal down to depth L; matches iff some
#     stored word has length exactly L.
#   - Duplicate addWord: same O(L) walk, sets an already-True flag. Harmless.
#   - search on a fresh dictionary: root has no children, bails immediately.
#   - The constraints guarantee length >= 1, but a "" query would still work:
#     zero iterations, returns root.is_word.
#
# ---------------------------------------------------------------------------
# The follow-up: an adversary makes one search maximally expensive
# ---------------------------------------------------------------------------
# Given the O(min(26^d, N)) bound, an adversary adds many long words and then
# queries a long all-dots string, forcing a full traversal.
#
# Mitigation - bucket by length (Alt 3): a '.' matches EXACTLY ONE letter,
# never zero and never two, so a length-L query can only match length-L words.
# Length is therefore a free, EXACT partition key, and partitioning costs O(1)
# per operation.
#
# The honest accounting (the part worth more than the trick): the win scales
# with L, because the recursion depth is ALREADY capped at len(word).
#   - Query "b.." - the walk only descends 3 levels either way, so bucketing
#     prunes only BREADTH at those shallow depths (the depth-<=3 prefixes of
#     the wrong-length words). A modest, roughly constant-factor win.
#   - Query of 25 dots - a single trie traverses EVERYTHING; the bucketed
#     version touches only the length-25 words. Potentially a huge win.
# So the mitigation is nearly worthless for a short query and substantial for
# the true worst case. Asking "the depth is already capped, so what is this
# pruning actually buying me?" is the reasoning that separates naming an
# optimization from knowing its value.


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(L) add, O(min(26^d, N)) search, O(L) auxiliary space
#        Correct and optimal. Differences from the active code: the '.' branch
#        uses an or-accumulator instead of any() (short-circuits the recursive
#        call but keeps iterating the loop), an unnecessary else after an
#        always-returning if, `match` shadowing a soft keyword, `i+1` spacing,
#        one blank line between the classes.
# ---------------------------------------------------------------------------
# class TrieNode:
#     def __init__(self) -> None:
#         self.children: dict[str, "TrieNode"] = {}
#         self.is_word: bool = False
#
# class WordDictionary:
#
#     def __init__(self) -> None:
#         self.root: TrieNode = TrieNode()
#
#     def addWord(self, word: str) -> None:
#         curr = self.root
#         for ch in word:
#             if ch not in curr.children:
#                 curr.children[ch] = TrieNode()
#             curr = curr.children[ch]
#         curr.is_word = True
#
#     def search(self, word: str) -> bool:
#
#         def dfs(i: int, node: TrieNode) -> bool:
#             if i == len(word):
#                 return node.is_word
#             ch = word[i]
#             if ch != '.':
#                 if ch not in node.children:
#                     return False
#                 return dfs(i+1, node.children[ch])
#             else:
#                 match = False
#                 for child in node.children.values():
#                     match = match or dfs(i+1, child)
#                 return match
#
#         return dfs(0, self.root)


# ---------------------------------------------------------------------------
# Alt 2: iterative frontier set (BFS-style) - O(min(26^d, N)) time,
#        O(frontier width) space, up to O(26^d)
#        Same work, different space profile. Instead of recursing one path at a
#        time, hold ALL nodes reachable at index i and expand them together.
#        This is only well-defined because of the depth-synchronization noted
#        above: every live node is always at exactly depth i.
#
#        The trade: no recursion stack (no depth limit to worry about), but the
#        frontier itself can grow to the full branching width, so space goes
#        from O(L) to O(26^d) worst case. Strictly worse space for identical
#        time - DFS is the right default here. Worth knowing as the "can you do
#        it iteratively" answer, and note the `if not nxt: return False` early
#        bail, which the recursive form gets for free.
#
#        No dedup needed on the frontier: each trie node has exactly one
#        parent, so no node can be appended twice.
# ---------------------------------------------------------------------------
# def search(self, word: str) -> bool:
#     frontier: list[TrieNode] = [self.root]
#     for ch in word:
#         nxt: list[TrieNode] = []
#         for node in frontier:
#             if ch == ".":
#                 nxt.extend(node.children.values())
#             elif ch in node.children:
#                 nxt.append(node.children[ch])
#         if not nxt:
#             return False
#         frontier = nxt
#     return any(node.is_word for node in frontier)


# ---------------------------------------------------------------------------
# Alt 3: length-bucketed tries - O(L) add, O(min(26^d, N_L)) search
#        One trie per word length, since a '.' matches exactly one letter. N_L
#        counts only the nodes belonging to words of length L. See the
#        follow-up discussion above for when this actually pays (long queries)
#        and when it barely does (short ones).
#
#        A pleasing consequence: inside bucket L every stored word has length
#        exactly L, so a node at depth L exists ONLY because a length-L word
#        ended there. is_word becomes REDUNDANT - the base case can just
#        return True. That is the same flavour of invariant as 208's
#        startsWith: reaching the node is itself the answer. It is kept below
#        anyway, because deleting a field to save a bool is a bad trade against
#        a structure that can no longer answer "does a word end here" if the
#        design ever loosens.
# ---------------------------------------------------------------------------
# class WordDictionary:
#     def __init__(self) -> None:
#         self.roots: dict[int, TrieNode] = {}
#
#     def addWord(self, word: str) -> None:
#         curr = self.roots.setdefault(len(word), TrieNode())
#         for ch in word:
#             if ch not in curr.children:
#                 curr.children[ch] = TrieNode()
#             curr = curr.children[ch]
#         curr.is_word = True
#
#     def search(self, word: str) -> bool:
#         root = self.roots.get(len(word))
#         if root is None:
#             return False        # no stored word of this length can match
#
#         def dfs(i: int, node: TrieNode) -> bool:
#             if i == len(word):
#                 return node.is_word
#             ch = word[i]
#             if ch == ".":
#                 return any(dfs(i + 1, child) for child in node.children.values())
#             if ch not in node.children:
#                 return False
#             return dfs(i + 1, node.children[ch])
#
#         return dfs(0, root)


# ---------------------------------------------------------------------------
# Alt 4: naive flat list (the baseline that justifies the trie)
#        O(1) amortized add, O(W * L) search
#        No structure at all: keep the words and pattern-match each one. The
#        length check is the cheap early bail that kills most candidates before
#        any character comparison. Correct, trivial, and the thing to state
#        FIRST in an interview before optimizing.
#
#        Why the trie beats it: here a matched prefix is SHARED work across
#        every word that has it, and a missing child dead-ends an entire
#        subtree of candidates at once. The flat list re-walks the same prefix
#        once per word and can prune nothing.
# ---------------------------------------------------------------------------
# class WordDictionary:
#     def __init__(self) -> None:
#         self.words: list[str] = []
#
#     def addWord(self, word: str) -> None:
#         self.words.append(word)
#
#     def search(self, word: str) -> bool:
#         return any(
#             len(stored) == len(word)
#             and all(q == "." or q == s for q, s in zip(word, stored))
#             for stored in self.words
#         )
