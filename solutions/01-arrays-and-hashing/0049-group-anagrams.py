# Group Anagrams (LC 49) | Arrays & Hashing | Blind 75
# Solved 2026-06-22 on neetcode.io | outcome: hint
# Style: clean (snake_case, PEP 8 OK)
#
# Optimal active below (count-key, O(N*K) time / O(N*K) space, assumes a fixed
# a-z alphabet); alternative commented at the bottom.

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord('a')] += 1
            res[tuple(count)].append(s)
        return list(res.values())

        # Alternative - sorted-key: O(N*K log K) time, O(N*K) space.
        # Alphabet-agnostic: works for any characters, not just a-z.
        # res = defaultdict(list)
        # for s in strs:
        #     res[tuple(sorted(s))].append(s)
        # return list(res.values())
