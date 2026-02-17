from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 191
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for _ in range(m-1):
            for j in range(n-2, -1, -1):
                dp[j] += dp[j+1]
        return dp[0]
    
    # 192
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        pass

    # 193
    def minPathSum(self, grid: List[List[int]]) -> int:
        pass

    # 194
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        R, C = len(text1), len(text2)
        dp = [0] * (C+1)
        for i in range(R-1, -1, -1):
            curr = [0] * (C+1)
            for j in range(C-1, -1, -1):
                if text1[i] == text2[j]:
                    curr[j] = dp[j+1] + 1
                else:
                    curr[j] = max(dp[j], curr[j+1])
            dp = curr
        return dp[0]
    
    # 195
    def lastStoneWeightII(self, stones: List[int]) -> int:
        pass

    # 196
    def maxProfit(self, prices: List[int]) -> int:
        hold = -prices[0]
        sold = rest = 0
        for price in prices[1:]:
            prev_hold, prev_sold, prev_rest = hold, sold, rest
            hold = max(prev_hold, prev_rest - price)
            sold = prev_hold + price
            rest = max(prev_rest, prev_sold)
        return max(sold, rest)
    
    # 197
    def change(self, amount: int, coins: List[int]) -> int:
        dp = [0] * (amount+1)
        dp[0] = 1
        for c in coins:
            for a in range(c, amount+1):
                dp[a] += dp[a - c]
        return dp[amount]
    
    # 198
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total or (target + total) % 2 != 0:
            return 0
        S = (target + total) // 2
        dp = [0] * (S+1)
        dp[0] = 1
        for num in nums:
            for s in range(S, num-1, -1):
                dp[s] += dp[s - num]
        return dp[S]
    
    # 199
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        pass

    # 200
    def stoneGame(self, piles: List[int]) -> bool:
        pass

    # 201
    def stoneGameII(self, piles: List[int]) -> int:
        pass

    # 202
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        pass

    # 203
    def numDistinct(self, s: str, t: str) -> int:
        pass

    # 204
    def minDistance(self, word1: str, word2: str) -> int:
        pass

    # 205
    def maxCoins(self, nums: List[int]) -> int:
        pass

    # 206
    def isMatch(self, s: str, p: str) -> bool:
        pass

if __name__ == "__main__":
    s = Solution()
