from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 241
    def singleNumber(self, nums: List[int]) -> int:
        pass

    # 242
    def hammingWeight(self, n: int) -> int:
        res = 0
        while n:
            n &= n-1
            res += 1
        return res

    # 243
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n+1)
        for i in range(n+1):
            dp[i] = dp[i >> 1] + (i & 1)
        return dp

    # 244
    def addBinary(self, a: str, b: str) -> str:
        pass

    # 245
    def reverseBits(self, n: int) -> int:
        res = 0
        for _ in range(32):
            res = (res << 1) | (n & 1)
            n >>= 1
        return res

    # 246
    def missingNumber(self, nums: List[int]) -> int:
        xor = len(nums)
        for i, n in enumerate(nums):
            xor ^= i ^ n
        return xor

    # 247
    def getSum(self, a: int, b: int) -> int:
        MASK = 0xffffffff
        MAX_INT = 0x7fffffff
        while b != 0:
            carry = (a & b) << 1
            a = (a ^ b) & MASK
            b = carry & MASK
        return a if a <= MAX_INT else ~(a ^ MASK)
    
    # 248
    def reverse(self, x: int) -> int:
        pass

    # 249
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        pass

    # 250
    def minEnd(self, n: int, x: int) -> int:
        pass

if __name__ == "__main__":
    s = Solution()
