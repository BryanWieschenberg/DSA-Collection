from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 174
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        dp1, dp2 = 1, 2
        for _ in range(3, n+1):
            dp1, dp2 = dp2, dp1 + dp2
        return dp2
    
    # 175
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        pass

    # 176
    def tribonacci(self, n: int) -> int:
        pass

    # 177
    def rob(self, nums: List[int]) -> int:
        dp1 = dp2 = 0
        for n in nums:
            dp1, dp2 = dp2, max(n + dp1, dp2)
        return dp2
    
    # 178
    def rob2(self, nums: List[int]) -> int:
        pass

    # 179
    def longestPalindrome(self, s: str) -> str:
        pass

    # 180
    def countSubstrings(self, s: str) -> int:
        pass

    # 181
    def numDecodings(self, s: str) -> int:
        pass

    # 182
    def coinChange(self, coins: List[int], amount: int) -> int:
        pass

    # 183
    def maxProduct(self, nums: List[int]) -> int:
        pass

    # 184
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        pass

    # 185
    def lengthOfLIS(self, nums: List[int]) -> int:
        pass

    # 186
    def canPartition(self, nums: List[int]) -> bool:
        pass

    # 187
    def combinationSum4(self, nums: List[int], target: int) -> int:
        pass

    # 188
    def numSquares(self, n: int) -> int:
        pass

    # 189
    def integerBreak(self, n: int) -> int:
        pass

    # 190
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        pass

if __name__ == "__main__":
    s = Solution()
