# Valid Parentheses (LC 20) | Stack | Blind 75
# Solved 2026-07-05 on neetcode.io | outcome: hint (data structure + dict-lookup
#   idea reasoned solo; needed one nudge on the loop control flow - the first-pass
#   mental model was "once you see a closing bracket, every later char must also be
#   a closing bracket," which wrongly rejects "()[]"; fixed by deciding per char
#   independently: opener -> push, closer -> pop-and-match)
# Raw: Data Structures & Algorithms/validate-parentheses/submission-0.py
# Style: clean - snake_case throughout, PascalCase class, no PEP 8 slips.
#        isValid/s are LeetCode's fixed method signature.
#
# ACTIVE CODE BELOW is the CLEANED version (agreed style-only improvements over the
# typed submission), per the /neetcode workflow. The verbatim accepted submission
# is preserved untouched as Alt 1 so the practice record stays honest. The
# algorithm is identical - the cleanups are purely surface.
#
# Single left-to-right pass with a stack. O(n) time - each char is pushed and
# popped at most once, and the dict lookup / append / pop are all O(1). O(n) space
# for the stack (grows to ~n/2 in the all-openers worst case); the bracket_pairs
# dict is a constant 3 entries.
#
# Key idea: a stack of the still-open brackets. Walk s; decide per char:
#   * opener (a KEY in bracket_pairs) -> push it.
#   * closer -> the top of the stack must be its matching opener. Guard the empty
#     stack first (a closer with nothing open -> invalid, e.g. ")"), then pop and
#     compare bracket_pairs[popped] against the current closer.
# After the loop, the string is valid IFF the stack is empty (leftover openers mean
# unclosed brackets, e.g. "(").
#
# Design note (the dict direction): this keys the dict OPENER -> closer, so
# `c in bracket_pairs` reads as "is this an opener." The other common idiom keys it
# CLOSER -> opener so the membership test detects closers. Both are correct here.
# Follow-up talking point: if s could contain stray non-bracket chars (letters),
# NEITHER naive version handles it - this one would route a letter into the closer
# branch and wrongly pop; the flipped one would push the letter as a phantom opener.
# The follow-up forces an explicit "is this even a bracket?" check regardless.

class Solution:
    def isValid(self, s: str) -> bool:
        bracket_pairs = {'(': ')', '{': '}', '[': ']'}
        stack = []

        for c in s:
            if c in bracket_pairs:
                stack.append(c)
            else:
                if not stack:
                    return False
                opening_bracket = stack.pop()
                if c != bracket_pairs[opening_bracket]:
                    return False

        return not stack


# ---------------------------------------------------------------------------
# What changed from the typed submission (Alt 1) -> the active cleaned version
# ---------------------------------------------------------------------------
#  1. Built bracket_pairs as a dict LITERAL ({'(': ')', '{': '}', '[': ']'}) in one
#     line, replacing three separate `bracket_pairs[...] = ...` assignments.
#  2. Dropped the `else:` after `return False` on the empty-stack guard - the return
#     already exits, so the else was dead nesting. The pop/compare now sit at the
#     same indent, one less level deep.
#  Kept the named `opening_bracket` temp (inlining `bracket_pairs[stack.pop()]`
#  would be a wash on readability). Same algorithm, same O(n) / O(n).
#
# ---------------------------------------------------------------------------
# Alternatives (commented; the active code above is the cleaned optimal)
# ---------------------------------------------------------------------------
#
# Alt 1) The accepted submission, VERBATIM as typed (the honest practice record).
#   Same stack algorithm and same O(n) / O(n). Differences vs the cleaned active
#   code are only the two style cleanups listed above: three-line dict construction
#   and the redundant else after the empty-stack return.
#
# class Solution:
#     def isValid(self, s: str) -> bool:
#         stack = []
#         bracket_pairs = {}
#         bracket_pairs['('] = ')'
#         bracket_pairs['{'] = '}'
#         bracket_pairs['['] = ']'
#
#         for c in s:
#             if c in bracket_pairs:
#                 stack.append(c)
#             else:
#                 if not stack:
#                     return False
#                 else:
#                     opening_bracket = stack.pop()
#                     if c != bracket_pairs[opening_bracket]:
#                         return False
#         return not stack
#
# Alt 2) Brute force - the "collapse adjacent matched pairs" method reasoned in
#   Phase 1. A valid string is exactly one you can fully erase by repeatedly
#   deleting any adjacent "()", "[]", or "{}"; valid IFF you reach "". Each replace
#   pass is O(n) and you may need up to O(n) passes (each removes at least one pair)
#   -> O(n^2) time, O(n) space for the rebuilt strings. The stack is this same idea
#   made incremental: instead of rescanning the whole string per removal, the stack
#   remembers the still-open brackets so each pair is matched in O(1) - collapsing
#   O(n^2) to O(n).
#
# class Solution:
#     def isValid(self, s: str) -> bool:
#         while '()' in s or '[]' in s or '{}' in s:
#             s = s.replace('()', '').replace('[]', '').replace('{}', '')
#         return s == ''
