from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List, Optional
from Helper import ListNode, ListHelper
from collections import defaultdict

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
        matrix.reverse()
        for r in range(len(matrix)):
            for c in range(r+1, len(matrix[0])):
                matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
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
        def sumOfSquares(num):
            res = 0
            while num:
                d = num % 10
                res += d * d
                num //= 10
            return res

        slow, fast = n, sumOfSquares(n)
        while fast != 1 and slow != fast:
            slow = sumOfSquares(slow)
            fast = sumOfSquares(sumOfSquares(fast))
        return fast == 1
    
    # 236
    def plusOne(self, digits: List[int]) -> List[int]:
        i = len(digits)-1
        while i >= 0 and digits[i] == 9:
            digits[i] = 0
            i -= 1
        if i < 0:
            return [1] + digits
        digits[i] += 1
        return digits
    
    # 237
    def romanToInt(self, s: str) -> int:
        pass

    # 238
    def myPow(self, x: float, n: int) -> float:
        if x == 0:
            return 0
        if n == 0:
            return 1
        res = 1
        power = abs(n)
        while power:
            if power & 1:
                res *= x
            x *= x
            power >>= 1
        return round(res, 5) if n > 0 else round(1/res, 5)
        
    # 239
    def multiply(self, num1: str, num2: str) -> str:
        if '0' in [num1, num2]:
            return '0'
        res = [0] * (len(num1) + len(num2))
        num1, num2 = num1[::-1], num2[::-1]
        for i1 in range(len(num1)):
            for i2 in range(len(num2)):
                digit = int(num1[i1]) * int(num2[i2])
                new = res[i1 + i2] + digit
                res[i1 + i2 + 1] += new // 10
                res[i1 + i2] = new % 10
        res, beg = res[::-1], 0
        while beg < len(res) and res[beg] == 0:
            beg += 1
        res = map(str, res[beg:])
        return ''.join(res)
    
    # 240
    class CountSquares:
        def __init__(self):
            self.ct = defaultdict(int)
            self.pts = []

        def add(self, point: List[int]) -> None:
            self.ct[tuple(point)] += 1
            self.pts.append(point)

        def count(self, point: List[int]) -> int:
            res = 0
            px, py = point
            for x, y in self.pts:
                if abs(py-y) != abs(px-x) or x == px or y == py:
                    continue
                res += self.ct[(x, py)] * self.ct[(px, y)]
            return res

if __name__ == "__main__":
    s = Solution(); hl = ListHelper()
