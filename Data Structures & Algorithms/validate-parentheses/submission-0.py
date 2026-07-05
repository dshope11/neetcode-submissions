class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        bracket_pairs = {}
        bracket_pairs['('] = ')'
        bracket_pairs['{'] = '}'
        bracket_pairs['['] = ']'

        for c in s:
            if c in bracket_pairs:
                stack.append(c)
            else:
                if not stack:
                    return False
                else:
                    opening_bracket = stack.pop()
                    if c != bracket_pairs[opening_bracket]:
                        return False
        return not stack