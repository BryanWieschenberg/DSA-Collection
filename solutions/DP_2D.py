from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 191
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for _ in range(1, m):
            for c in range(1, n):
                dp[c] += dp[c-1]
        return dp[-1]

    # 192
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        pass

    # 193
    def minPathSum(self, grid: List[List[int]]) -> int:
        pass

    # 194
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        R, C = len(text1), len(text2)
        prev = [0] * (C+1)
        for i in range(1, R+1):
            curr = [0] * (C+1)
            for j in range(1, C+1):
                if text1[i-1] == text2[j-1]:
                    curr[j] = prev[j-1] + 1
                else:
                    curr[j] = max(prev[j], curr[j-1])
            prev = curr
        return prev[-1]

    # 195
    def lastStoneWeightII(self, stones: List[int]) -> int:
        pass

    # 196
    def maxProfit(self, prices: List[int]) -> int:
        pass

    # 197
    def change(self, amount: int, coins: List[int]) -> int:
        pass

    # 198
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        pass

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
