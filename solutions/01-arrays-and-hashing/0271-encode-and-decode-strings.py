# Encode and Decode Strings (LC 271) | Arrays & Hashing | Blind 75
# Solved 2026-06-24 on neetcode.io | outcome: hint
# Raw: Data Structures & Algorithms/string-encode-and-decode/submission-0.py
# Style: clean (snake_case, PascalCase class, no Unicode); one nit - trailing
#        whitespace on the blank line after the decode loop (PEP 8 W293).
#        Left verbatim; not fixed here.
#
# Optimal active below (length-prefix framing, O(m + n) time / O(m + n) space
# for both calls; m = total chars across all strings, n = number of strings).
#
# Key idea: a single delimiter can NEVER be safe, because any byte can appear
# inside a string. So stop trying to *find* the boundary by content - *declare*
# it. Write each string as  len(s) + "#" + s . Decode reads the digits up to
# the "#" to get a length, then consumes EXACTLY that many chars - it never
# scans the payload, so a "#" (or digits, newlines, anything) inside a string
# is just counted data and can't fool the parser. The "#" is only ever scanned
# for inside the length prefix, which is digits-only, so it's unambiguous there.
#
# Why O(m + n) and not just O(m): the n term is per-string overhead (one length
# digit + "#" + one loop step each). It is NOT dominated by m once empty strings
# are allowed - encode(["", "", ...]) has m = 0 but still does O(n) work. Both
# terms survive.
#
# Robustness note (good interview talking point): decode's inner scan
# `while s[j] != '#'` has no bounds check - it trusts the stream is well-formed.
# Safe here because decode only ever sees encode's output; a hardened parser
# would bound the scan / validate.

class Solution:

    def encode(self, strs: List[str]) -> str:
        parts = []
        for s in strs:
            parts.append(str(len(s)) + "#" + s)
        return "".join(parts)

    def decode(self, s: str) -> List[str]:
        res = []
        i = 0

        while i < len(s):
            j = i
            while s[j] != '#':
                j += 1
            length = int(s[i:j])
            i = j + 1
            j = i + length
            res.append(s[i:j])
            i = j

        return res

# Alternative - non-digit delimiter without a length (escaping): pick a
# separator and escape any literal occurrence in the payload, e.g. replace
# "#" -> "##" on encode and split on a lone "#". O(m + n) time but fragile:
# you must escape the escape char, and the split/parse is error-prone. The
# length-prefix version is preferred precisely because it never inspects the
# payload. (Sketch only - not implemented.)
#
# Alternative - chr(257)-style "impossible" delimiter: relies on the alphabet
# being bounded (e.g. ASCII/extended-ASCII), so a code point above the max can
# never appear in the data and is a safe separator: "".join(s + chr(257) ...).
# O(m + n). Breaks the moment the input can contain arbitrary Unicode - same
# class of bug as any fixed-alphabet assumption. State the caveat if you use it.
