# from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # return Counter(s) == Counter(t)
        if len(s) != len(t):
            return False
        Counter_s = {}
        for letter in s:
            if letter not in Counter_s:
                Counter_s[letter] = 1
            else: Counter_s[letter] += 1
        Counter_t = {}
        for letter in t:
            if letter not in Counter_t:
                Counter_t[letter] = 1
            else: Counter_t[letter] += 1
        
        for k in Counter_s:
            if k not in Counter_t:
                return False
            elif Counter_t[k] != Counter_s[k]:
                return False
        return True

        # # More concisely:

        # for i in range(len(s)):
        #     count_S[s[i]] = 1 + count_S.get(s[i], 0)
        #     count_T[t[i]] = 1 + count_T.get(t[i], 0)
        # return count_S == count_T
