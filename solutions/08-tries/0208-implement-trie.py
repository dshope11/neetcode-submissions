# Implement Trie (Prefix Tree) - LC 208 - Medium - (NeetCode 150, Blind 75)
# Pattern: Tries. The FIRST problem of the Tries section - it builds the
#          structure the rest of the section (211 wildcard search, 212 grid-DFS
#          pruning) is layered on. A trie is a PREFIX INDEX: a tree keyed by the
#          characters of a string, where shared prefixes share a path. Every
#          operation is the same move - walk character by character from the root
#          - and they differ only in (a) what happens when a child is MISSING and
#          (b) what you check when the loop ENDS.
# Solved 2026-07-27 | outcome: solo
#
# Raw: Data Structures & Algorithms/implement-prefix-tree/submission-0.py
#
# Note on the class name: neetcode.io calls the class PrefixTree; LeetCode 208
# calls it Trie. Same spec, same three methods (insert / search / startsWith).
# The name below matches the accepted submission.
#
# Active code below is the CLEANED version (see "What changed"): the accepted
# submission was correct and optimal. The one substantive cleanup is a DEAD
# check (`return curr is not None`, which can never be False in the inlined
# form); the rest is whitespace/PEP 8. The structure stays David's - three
# inlined walks, no shared helper. Alt 1 = his verbatim accepted submission;
# Alt 2 = the factored _walk helper (which is where `is not None` becomes
# load-bearing again); Alt 3 = the [None] * 26 array-children node, the
# trade-off reasoned in Phase 1.
#
# No typing imports needed: the active code uses the built-in generic
# dict[str, "TrieNode"] (Python 3.9+). On 3.8 or earlier this would need
# Dict from typing. Alt 2's helper returns Optional[TrieNode] and would need
# `from typing import Optional`.


class TrieNode:
    def __init__(self) -> None:
        # BOTH attributes must be assigned in __init__, not in the class body.
        # A class-body `children = {}` is created ONCE at class-definition time
        # and SHARED by every node - one insert would write into all of them.
        # (is_word = False in the class body happens to be harmless, since
        # `self.is_word = True` rebinds on the instance rather than mutating,
        # but there is no reason to split the rule.)
        self.children: dict[str, "TrieNode"] = {}   # quoted: forward reference
        self.is_word: bool = False                  # "a word ENDS here"


class PrefixTree:

    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()            # root holds no character

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()      # missing child -> CREATE
            curr = curr.children[ch]
        curr.is_word = True                         # mark AFTER the loop, on the
                                                    # final node only

    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return False                        # missing child -> BAIL
            curr = curr.children[ch]
        return curr.is_word                         # path exists != word exists

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return False                        # missing child -> BAIL
            curr = curr.children[ch]
        return True                                 # reaching here IS the answer
                                                    # (see the invariant below)


# ---------------------------------------------------------------------------
# What changed (typed submission -> active code)
# ---------------------------------------------------------------------------
# Same algorithm, same complexity: O(L) time for all three methods (L = length
# of the string argument), O(L) space per insert, O(total characters stored)
# for the whole structure.
#   - startsWith's final `return curr is not None` -> `return True`. The check
#     was DEAD: curr starts as self.root (a real node) and is only ever
#     reassigned to curr.children[ch] (also a real TrieNode), so the expression
#     is unconditionally True. See the insight below for where it came from and
#     why it is load-bearing in Alt 2 but noise here.
#   - Stripped trailing whitespace after `curr.is_word = True`.
#   - Two blank lines between the top-level classes (PEP 8).
# Type hints were already complete in the submission - every method annotated
# including the __init__ -> None returns and `self.root: TrieNode`. Naming was
# clean snake_case throughout (startsWith is camelCase because the PLATFORM
# defines that method name; matching the given signature is correct).
#
# The sharp point - a dead check that is a fossil of a design not written:
#   During the discussion the invariant was phrased as "landing on a non-None
#   node is sufficient". That None was the return channel of a HELPER: a _walk
#   returning Optional[TrieNode], signalling failure with None (Alt 2). The
#   submitted code INLINED the walk, which moved the failure signal to the early
#   `return False` - but the `is not None` test came along without its meaning.
#   Correct by accident. Worth fixing rather than shrugging at: it tells a
#   reader "curr might be None here", so a maintainer has to re-derive that it
#   cannot be. The SAME LINE is load-bearing in Alt 2 and noise here - which is
#   the actual lesson about where a check belongs.
#
# Why startsWith needs no check at all (the invariant):
#   Every node exists only because some insert() created it, and nodes are only
#   created while walking the characters of a word being inserted. So every node
#   lies on the path of at least one stored word => any prefix you can walk to
#   is, by construction, a real prefix of a stored word. No is_word test, no
#   has-children test.
#   This invariant is exactly what a LAZY delete would break: flipping
#   is_word = False without pruning leaves ghost paths, so startsWith would
#   return True for a deleted word. That is why a real delete prunes on the way
#   back up (post-order), removing a node only when it is the last link left.
#
# Why a trie at all - the honest comparison (the anti-trigger):
#   Naive design = a flat set of the inserted words.
#     insert(word)      O(L)     - hashing a string READS every character; the
#     search(word)      O(L)       reflex "hash lookup is O(1)" is wrong for
#                                  string keys, and the trie does NOT beat it
#     startsWith(pfx)   O(N * L) - no choice but to scan all N stored words and
#                                  prefix-compare each one
#   So a hash set MATCHES the trie on two of the three operations and loses
#   catastrophically only on the third. At N = 30,000 that is the entire
#   justification for the structure. Stating it this way is the difference
#   between "I memorized a trie" and "I know when one pays" - a trie trades
#   memory and constant factors for prefix queries a hash cannot answer at all.
#
# Edge cases - all handled with NO special-casing:
#   - insert("") flips is_word on the root; search("") reads it; startsWith("")
#     is always True (zero loop iterations, fall through to return True).
#   - Duplicate insert: same O(L) walk, sets an already-True flag. Harmless.
#   - search(word) longer than anything stored: bails at the first missing char.
#   - search/startsWith on a fresh trie: root has no children, bails immediately.
#   Optional micro-optimisation (not implemented - it is an early-bail, not a
#   change to the structure): track the longest word length inserted and return
#   False from search immediately when len(word) exceeds it.
#
# The natural follow-up - autocomplete(prefix) -> all words with that prefix:
#   Walk to the prefix node (O(L)), then PRE-ORDER DFS its subtree collecting
#   every is_word node. Visiting children in a..z order emits the results
#   alphabetically for free. Time O(L + nodes in that subtree). Space: O(h)
#   AUXILIARY for the recursion stack, PLUS O(total characters returned) for the
#   output - worth naming which one you are quoting, since output space is
#   normally reported separately (you cannot avoid materialising the answer).
#   Accumulate the current path in a LIST and "".join it at each is_word node;
#   building it with `s += ch` copies the whole string each time -> O(n^2).


# ---------------------------------------------------------------------------
# Alt 1: accepted submission, verbatim (the honest practice record)
#        O(L) time per operation, O(total characters stored) space
#        Correct and optimal. Differences from the active code: the dead
#        `return curr is not None` in startsWith, trailing whitespace, one
#        blank line between the classes.
# ---------------------------------------------------------------------------
# class TrieNode:
#     def __init__(self) -> None:
#         self.children: dict[str, "TrieNode"] = {}
#         self.is_word: bool = False
#
# class PrefixTree:
#
#     def __init__(self) -> None:
#         self.root: TrieNode = TrieNode()
#
#     def insert(self, word: str) -> None:
#         curr = self.root
#         for ch in word:
#             if ch not in curr.children:
#                 curr.children[ch] = TrieNode()
#             curr = curr.children[ch]
#         curr.is_word = True
#
#     def search(self, word: str) -> bool:
#         curr = self.root
#         for ch in word:
#             if ch not in curr.children:
#                 return False
#             curr = curr.children[ch]
#         return curr.is_word
#
#     def startsWith(self, prefix: str) -> bool:
#         curr = self.root
#         for ch in prefix:
#             if ch not in curr.children:
#                 return False
#             curr = curr.children[ch]
#         return curr is not None


# ---------------------------------------------------------------------------
# Alt 2: factored _walk helper - O(L) time, O(total characters stored) space
#        search and startsWith are the SAME walk; the entire difference is that
#        one reads is_word and the other does not. Factoring the walk out makes
#        that explicit and kills the duplication - and it is here that
#        `is not None` becomes load-bearing, because None is now a real return
#        value signalling "the path does not exist".
#
#        Why insert stays separate: it MUTATES (creates missing nodes), so it
#        cannot share a read-only walk. Threading a `create: bool` flag through
#        _walk to unify all three would be worse - a boolean-trap parameter that
#        makes the function do two different things depending on a call-site
#        argument, for no gain over five duplicated lines.
# ---------------------------------------------------------------------------
# from typing import Optional
#
# class PrefixTree:
#     def __init__(self) -> None:
#         self.root: TrieNode = TrieNode()
#
#     def _walk(self, prefix: str) -> Optional[TrieNode]:
#         """Return the node reached by prefix, or None if the path breaks."""
#         curr = self.root
#         for ch in prefix:
#             if ch not in curr.children:
#                 return None
#             curr = curr.children[ch]
#         return curr
#
#     def insert(self, word: str) -> None:
#         curr = self.root
#         for ch in word:
#             curr = curr.children.setdefault(ch, TrieNode())
#         curr.is_word = True
#
#     def search(self, word: str) -> bool:
#         node = self._walk(word)
#         return node is not None and node.is_word
#
#     def startsWith(self, prefix: str) -> bool:
#         return self._walk(prefix) is not None
#
# (insert above also shows dict.setdefault, which collapses the
#  "if missing: create; then descend" pair into one call - it returns the
#  existing value if the key is present, otherwise inserts the default and
#  returns that. Note the TrieNode() is constructed on EVERY iteration even
#  when the child already exists, then discarded; at this scale that is fine,
#  but the explicit `if ch not in ...` form avoids the wasted allocation and
#  reads more plainly. Not a clear win either way.)


# ---------------------------------------------------------------------------
# Alt 3: array children - O(L) time, O(26 * nodes) space
#        The fixed-alphabet node: 26 slots indexed by ord(ch) - ord('a')
#        instead of a dict. Drops hashing for direct array indexing, and is
#        what you would write in C++. The trade-off: every node pays for 26
#        slots whether or not it uses them, so a sparse trie wastes a lot of
#        memory - which is why the dict version is the Pythonic default. Only
#        works when the alphabet is fixed, small, and known up front.
# ---------------------------------------------------------------------------
# class TrieNode:
#     def __init__(self) -> None:
#         self.children: list[Optional["TrieNode"]] = [None] * 26
#         self.is_word: bool = False
#
# class PrefixTree:
#     def __init__(self) -> None:
#         self.root: TrieNode = TrieNode()
#
#     def insert(self, word: str) -> None:
#         curr = self.root
#         for ch in word:
#             i = ord(ch) - ord("a")
#             if curr.children[i] is None:
#                 curr.children[i] = TrieNode()
#             curr = curr.children[i]
#         curr.is_word = True
#
#     def search(self, word: str) -> bool:
#         curr = self.root
#         for ch in word:
#             i = ord(ch) - ord("a")
#             if curr.children[i] is None:
#                 return False
#             curr = curr.children[i]
#         return curr.is_word
#
#     def startsWith(self, prefix: str) -> bool:
#         curr = self.root
#         for ch in prefix:
#             i = ord(ch) - ord("a")
#             if curr.children[i] is None:
#                 return False
#             curr = curr.children[i]
#         return True
