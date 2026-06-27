# Longest Consecutive Sequence (LC 128) | Arrays & Hashing | Blind 75
# Solved 2026-06-27 on neetcode.io | outcome: hint
# Raw: Data Structures & Algorithms/longest-consecutive-sequence/submission-0.py
# Style: clean (no Unicode, PEP 8 layout). Nit: `numSet` is camelCase;
#        PEP 8 wants `num_set`. Left verbatim; not fixed here.
#
# Optimal active below: hash-set + run-head scan, O(n) time / O(n) space.
#
# Key idea: dump everything into a set for O(1) membership, then only start
# counting a run from a number that has NO left neighbor (num - 1 not in set) -
# those are exactly the "heads" of runs. From a head, walk forward
# (num+1, num+2, ...) with O(1) lookups until the run ends.
#
# Why it's O(n) despite the nested loop: the inner while-walk touches each
# element at most once across the ENTIRE algorithm (each element belongs to
# exactly one run and is only walked when you start from that run's head). Add
# the outer loop's one visit per element -> ~2n work, amortized O(1) per element.
#
# Without the head-check it degrades to O(n^2): on [1,2,...,n] you'd re-walk the
# whole tail from every start (n + (n-1) + ... = O(n^2)). The head-check is the
# whole trick.
#
# Edge cases: empty list -> 0 (longest stays 0); single element -> 1; duplicates
# are free (the set dedups them); negatives are fine (just integer keys).

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numSet = set(nums)
        longest = 0

        for num in numSet:
            if (num - 1) not in numSet:
                length = 1
                while (num + length) in numSet:
                    length += 1
                longest = max(length, longest)
        return longest

# Alternative 1 - brute force (no set): O(n^3) time, O(1) extra space.
# For every element, build its run by repeatedly searching the array for the
# next consecutive value. The lookup is a LINEAR scan (O(n)), the run can grow
# up to n long, across n start elements -> n * n * n. The whole optimization is
# swapping that O(n) scan for an O(1) set lookup (and adding the head-check so we
# don't re-walk runs from the middle).
# def longestConsecutive(self, nums):
#     longest = 0
#     for num in nums:
#         length = 1
#         while (num + length) in nums:   # `in nums` on a list is O(n)!
#             length += 1
#         longest = max(longest, length)
#     return longest
#
# Alternative 2 - interval-merge boundary hashmap: O(n) time, O(n) space.
# One pass. mp[num] = length of the run containing num, but only kept ACCURATE
# at the two endpoints of each run; interior values go stale and are never read.
# Per new num: left = mp[num-1], right = mp[num+1] (both endpoints of adjacent
# runs); the merged length is left + right + 1; rewrite the two new outer
# boundaries (num - left) and (num + right) to that length. `if not mp[num]`
# guards duplicates. Correct because you only ever query num-1 / num+1, which
# are always boundary cells. Same complexity as the set version, but the
# correctness invariant ("only endpoints are trusted") is non-obvious and
# defaultdict(int) silently inserts spurious 0 keys on every neighbor read -
# less elegant, buys nothing. Kept as a "I also know the interval trick" variant.
# def longestConsecutive(self, nums):
#     mp = defaultdict(int)
#     res = 0
#     for num in nums:
#         if not mp[num]:
#             mp[num] = mp[num - 1] + mp[num + 1] + 1
#             mp[num - mp[num - 1]] = mp[num]
#             mp[num + mp[num + 1]] = mp[num]
#             res = max(res, mp[num])
#     return res
