from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        def dfs(r, c, i):
            if i == len(word):
                return True

            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[i]:
                return False

            temp = board[r][c]
            board[r][c] = '#'

            found = (
                dfs(r + 1, c, i + 1) or
                dfs(r - 1, c, i + 1) or
                dfs(r, c + 1, i + 1) or
                dfs(r, c - 1, i + 1)
            )

            board[r][c] = temp
            return found

        rows, cols = len(board), len(board[0])

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0): return True

        return False

s = Solution()

# print( s. exist ( board=[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word="ABCCED" )) # True
