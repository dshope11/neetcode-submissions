from collections import Counter

DIRECTIONS = [
    (0, -1),  # up
    (1, 0),   # right
    (0, 1),   # down
    (-1, 0),  # left
]

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        exists = False
        m = len(board)
        n = len(board[0])
        if len(word) > m * n:
            return False
        count_board = Counter(c for row in board for c in row)
        count_word = Counter(c for c in word)
        for c in count_word:
            if count_board[c] < count_word[c]:
                return False

        def dfs(i, j, wordIdx) -> bool:
            if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]):
                return False
            if board[i][j] == "#":
                return False
            if word[wordIdx] != board[i][j]:
                return False
            if wordIdx == len(word) - 1:
                return True
            c_tmp = board[i][j]
            board[i][j] = "#"
            for dx, dy in DIRECTIONS:
                if dfs(i + dx, j + dy, wordIdx + 1):
                    return True
            board[i][j] = c_tmp
            return False

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == word[0]:
                    exists = dfs(i, j, 0)
                    if exists:
                        return exists
        return exists
