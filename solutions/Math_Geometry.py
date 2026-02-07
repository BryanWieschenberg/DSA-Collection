from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List, Optional
from Helper import ListNode, ListHelper

class Solution:
    # 228
    def convertToTitle(self, columnNumber: int) -> str:
        pass

    # 229
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        pass

    # 230
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pass

    # 231
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        pass

    # 232
    def rotate(self, matrix: List[List[int]]) -> None:
        for i in range(len(matrix)):
            for j in range(i+1, len(matrix[0])):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for i in range(len(matrix)):
            matrix[i].reverse()
        return matrix

    # 233
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        res = []
        l, r, t, b = 0, len(matrix[0]), 0, len(matrix)
        while l < r and t < b:
            for i in range(l, r):
                res.append(matrix[t][i])
            t += 1
            for i in range(t, b):
                res.append(matrix[i][r-1])
            r -= 1
            if not (l < r and t < b):
                break
            for i in range(r-1, l-1, -1):
                res.append(matrix[b-1][i])
            b -= 1
            for i in range(b-1, t-1, -1):
                res.append(matrix[i][l])
            l += 1
        return res
    
    # 234
    def setZeroes(self, matrix: List[List[int]]) -> None:
        R, C = len(matrix), len(matrix[0])
        rows, cols = [False] * R, [False] * C
        for r in range(R):
            for c in range(C):
                if matrix[r][c] == 0:
                    rows[r] = True
                    cols[c] = True
        for r in range(R):
            for c in range(C):
                if rows[r] or cols[c]:
                    matrix[r][c] = 0
        return matrix

    # 235
    def isHappy(self, n: int) -> bool:
        pass

    # 236
    def plusOne(self, digits: List[int]) -> List[int]:
        pass

    # 237
    def romanToInt(self, s: str) -> int:
        pass

    # 238
    def myPow(self, x: float, n: int) -> float:
        pass

    # 239
    def multiply(self, num1: str, num2: str) -> str:
        pass

    # 240
    class CountSquares:
        def __init__(self):
            pass

        def add(self, point: List[int]) -> None:
            pass

        def count(self, point: List[int]) -> int:
            pass

if __name__ == "__main__":
    s = Solution(); hl = ListHelper()
