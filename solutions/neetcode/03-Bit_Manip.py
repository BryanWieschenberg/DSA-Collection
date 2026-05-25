from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(ospath.dirname(__file__))))
from typing import List
from math import fmod


class Solution:
    # 47
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for n in nums:
            res ^= n
        return res
    
    # 48
    def hammingWeight(self, n: int) -> int:
        res = 0
        while n > 0:
            res += n & 1
            n >>= 1
        return res

    # 49
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n+1)
        for i in range(n+1):
            dp[i] = dp[i >> 1] + (i & 1)
        return dp

    # 50
    def addBinary(self, a: str, b: str) -> str:
        res = []
        carry = 0
        i, j = len(a)-1, len(b)-1
        while i >= 0 or j >= 0 or carry:
            digA = int(a[i]) if i >= 0 else 0
            digB = int(b[j]) if j >= 0 else 0
            total = digA + digB + carry
            res.append(total & 1)
            carry = total >> 1
            i -= 1
            j -= 1
        res.reverse()
        return ''.join(map(str, res))

    # 51
    def reverseBits(self, n: int) -> int:
        res = 0
        for _ in range(32):
            res = (res << 1) | (n & 1)
            n >>= 1
        return res

    # 52
    def missingNumber(self, nums: List[int]) -> int:
        res = len(nums)
        for i, n in enumerate(nums):
            res ^= i ^ n
        return res

    # 53
    def getSum(self, a: int, b: int) -> int:
        MASK = 0xffffffff
        MAX_INT = 0x7fffffff
        while b != 0:
            carry = (a & b) << 1
            a = (a ^ b) & MASK
            b = carry & MASK
        return a if a <= MAX_INT else ~(a ^ MASK)
    
    # 54
    def reverse(self, x: int) -> int:
        MIN, MAX = -2**31, 2**31-1 
        # use int() over // to 0-trunc to prevent x != 0 inf loop
        # since // rounds down, it continuously rounds to -1, and -1 / 1 continuously never reaches 0
        MIN_BOUND, MAX_BOUND = int(MIN / 10), int(MAX / 10)
        MIN_LSD, MAX_LSD = MIN % -10, MAX % 10
        res = 0
        while x != 0:
            digit = x % 10 if x >= 0 else x % -10
            x = int(x / 10)
            if res > MAX_BOUND or (res == MAX_BOUND and digit > MAX_LSD):
                return 0
            if res < MIN_BOUND or (res == MIN_BOUND and digit < MIN_LSD):
                return 0
            res = res * 10 + digit            
        return res

    # 55
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        res = 0
        for i in range(32):
            bit = (left >> i) & 1
            if not bit:
                continue
            remain = left % (1 << (i+1))
            diff = (1 << (i + 1)) - remain
            if right - left < diff:
                res |= (1 << i)
        return res

    # 56
    def minEnd(self, n: int, x: int) -> int:
        n -= 1
        res = x
        pos_x = 0
        pos_n = 0
        while (1 << pos_n) <= n:
            if not (x & (1 << pos_x)):
                if (n & (1 << pos_n)):
                    res |= (1 << pos_x)
                pos_n += 1
            pos_x += 1
        return res


if __name__ == "__main__":
    s = Solution()
