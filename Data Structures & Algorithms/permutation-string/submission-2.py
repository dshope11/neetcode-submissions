class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:

        if len(s1) > len(s2):
            return False

        s1_count = [0]*26
        window_count = [0]*26

        for c in s1:
            s1_count[ord(c) - ord('a')] += 1

        matches = s1_count.count(0)

        left = 0

        for right, c in enumerate(s2):
            c_match_prior = s1_count[ord(c) - ord('a')] == window_count[ord(c) - ord('a')]
            window_count[ord(c) - ord('a')] += 1
            if s1_count[ord(c) - ord('a')] == window_count[ord(c) - ord('a')] and not c_match_prior:
                matches += 1
            elif s1_count[ord(c) - ord('a')] != window_count[ord(c) - ord('a')] and c_match_prior:
                matches -= 1

            if right >= len(s1):
                left_match_prior = s1_count[ord(s2[left]) - ord('a')] == window_count[ord(s2[left]) - ord('a')]
                window_count[ord(s2[left]) - ord('a')] -= 1
                if s1_count[ord(s2[left]) - ord('a')] == window_count[ord(s2[left]) - ord('a')] and not left_match_prior:
                    matches += 1
                elif s1_count[ord(s2[left]) - ord('a')] != window_count[ord(s2[left]) - ord('a')] and left_match_prior:
                    matches -= 1

                left += 1

            if right >= len(s1) - 1 and matches == 26:
                return True
        
        return False

            