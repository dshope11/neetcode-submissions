class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Count-key: O(N*K) time, O(N*K) space.
        # Assumes a fixed 26-letter alphabet (lowercase a-z).
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
