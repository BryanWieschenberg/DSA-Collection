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
        for i in range(len(matrix)): # 90 deg rot, reverse rows
            matrix[i].reverse()
        # for j in range(len(matrix)): # -90 deg rot, reverse cols
        #     for i in range(len(matrix) // 2):
        #         matrix[i][j], matrix[-i-1][j] = matrix[-i-1][j], matrix[i][j]
        return matrix

    # 233
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        res = []
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        steps = [len(matrix[0]), len(matrix)-1]
        r, c, d = 0, -1, 0
        while steps[d & 1]:
            for _ in range(steps[d & 1]):
                r += dirs[d][0]
                c += dirs[d][1]
                res.append(matrix[r][c])
            steps[d & 1] -= 1
            d += 1
            d %= 4
        return res
    
    # 234
    def setZeroes(self, matrix: List[List[int]]) -> None:
        pass

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
