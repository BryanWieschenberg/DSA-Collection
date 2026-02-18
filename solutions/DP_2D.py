from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from functools import lru_cache

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
        n1, n2, n3 = len(s1), len(s2), len(s3)
        if n1 + n2 != n3:
            return False
        dp = [[False] * (n2+1) for _ in range(n1+1)]
        dp[n1][n2] = True
        for i in range(n1, -1, -1):
            for j in range(n2, -1, -1):
                if i == n1 and j == n2:
                    continue
                dp[i][j] = (
                    (i < n1 and s1[i] == s3[i + j] and dp[i + 1][j]) or
                    (j < n2 and s2[j] == s3[i + j] and dp[i][j + 1])
                )
        return dp[0][0]
    
    # 200
    def stoneGame(self, piles: List[int]) -> bool:
        pass

    # 201
    def stoneGameII(self, piles: List[int]) -> int:
        pass

    # 202
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        @lru_cache(None)
        def dfs(r, c):
            res = 1
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if 0 <= nr < R and 0 <= nc < C and matrix[nr][nc] > matrix[r][c]:
                    res = max(res, 1 + dfs(nr, nc))
            return res
        
        R, C = len(matrix), len(matrix[0])
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        res = 0
        for r in range(R):
            for c in range(C):
                res = max(res, dfs(r, c))
        return res

    # 203
    def numDistinct(self, s: str, t: str) -> int:
        @lru_cache(None)
        def dfs(i, j):
            if j == len(t):
                return 1
            if i == len(s):
                return 0
            if s[i] == t[j]:
                return dfs(i+1, j+1) + dfs(i+1, j)
            else:
                return dfs(i+1, j)
        
        return dfs(0, 0)

    # 204
    def minDistance(self, word1: str, word2: str) -> int:
        R, C = len(word1), len(word2)
        dp = list(range(C+1))
        for i in range(1, R+1):
            curr = [i] + [0] * C
            for j in range(1, C+1):
                if word1[i-1] == word2[j-1]:
                    curr[j] = dp[j-1]
                else:
                    curr[j] = 1 + min(
                        curr[j-1],
                        dp[j],
                        dp[j-1]
                    )
            dp = curr
        return dp[C]
    
    # 205
    def maxCoins(self, nums: List[int]) -> int:
        @lru_cache(None)
        def dfs(l, r):
            if l > r:
                return 0
            res = 0
            for i in range(l, r+1):
                coins = nums[l-1] * nums[i] * nums[r+1]
                coins += dfs(l, i-1) + dfs(i+1, r)
                res = max(res, coins)
            return res
            
        nums = [1] + nums + [1]
        return dfs(1, len(nums)-2)
    
    # 206
    def isMatch(self, s: str, p: str) -> bool:
        @lru_cache(None)
        def dfs(i, j):
            if j == len(p):
                return i == len(s)
            match = i < len(s) and (s[i] == p[j] or p[j] == '.')
            if j+1 < len(p) and p[j+1] == '*':
                return (
                    dfs(i, j+2) or          # don't use *
                    (match and dfs(i+1, j)) # use *
                )
            if match:
                return dfs(i+1, j+1)
            return False
        
        return dfs(0, 0)

if __name__ == "__main__":
    s = Solution()
