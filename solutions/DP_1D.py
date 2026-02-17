from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from Helper import TrieNode, TrieHelper

class Solution:
    # 174
    def climbStairs(self, n: int) -> int:
        prev2, prev1 = 1, 1
        for _ in range(n - 1):
            tmp = prev2
            prev2 = prev1
            prev1 += tmp
        return prev1
    
    # 175
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        prev1, prev2 = cost[-1], 0
        for i in range(len(cost)-2, -1, -1):
            curr = cost[i] + min(prev1, prev2)
            prev2 = prev1
            prev1 = curr
        return min(prev1, prev2)

    # 176
    def tribonacci(self, n: int) -> int:
        pass

    # 177
    def rob(self, nums: List[int]) -> int:
        prev1 = prev2 = 0
        for n in nums:
            curr = max(prev1, n + prev2)
            prev2 = prev1
            prev1 = curr
        return prev1
    
    # 178
    def rob2(self, nums: List[int]) -> int:
        def helper(nums):
            prev1 = prev2 = 0
            for n in nums:
                curr = max(prev1, prev2 + n)
                prev2 = prev1
                prev1 = curr
            return prev1

        return max(nums[0], helper(nums[1:]), helper(nums[:-1]))
    
    # 179
    def longestPalindrome(self, s: str) -> str:
        def palCheck(l, r):
            nonlocal resIdx, resLen
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if (r - l + 1) > resLen:
                    resIdx = l
                    resLen = r - l + 1
                l -= 1
                r += 1

        resIdx = 0
        resLen = 0
        for i in range(len(s)):
            palCheck(i, i)
            palCheck(i, i+1)
        return s[resIdx : resIdx + resLen]
    
    # 180
    def countSubstrings(self, s: str) -> int:
        def palCheck(l, r):
            ct = 0
            while l >= 0 and r < len(s) and s[l] == s[r]:
                ct += 1
                l -= 1
                r += 1
            return ct

        res = 0
        for i in range(len(s)):
            res += palCheck(i, i)
            res += palCheck(i, i+1)        
        return res
    
    # 181
    def numDecodings(self, s: str) -> int:
        if s[0] == '0':
            return 0
        prev1 = prev2 = 1
        for i in range(1, len(s)):
            curr = 0
            if s[i] != '0':
                curr += prev1
            if 10 <= int(s[i-1 : i+1]) <= 26:
                curr += prev2
            prev2 = prev1
            prev1 = curr
        return prev1
    
    # 182
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [amount+1] * (amount+1)
        dp[0] = 0
        for i in range(1, amount+1):
            for c in coins:
                if i - c >= 0:
                    dp[i] = min(dp[i], dp[i-c]+1)
        return dp[amount] if dp[amount] != amount+1 else -1
    
    # 183
    def maxProduct(self, nums: List[int]) -> int:
        maxEnd = minEnd = res = nums[0]
        for n in nums[1:]:
            candidates = (n, n * maxEnd, n * minEnd)
            maxEnd = max(candidates)
            minEnd = min(candidates)
            res = max(res, maxEnd)
        return res
    
    # 184
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        class Trie:
            def __init__(self):
                self.root = TrieNode()
            def insert(self, word):
                curr = self.root
                for c in word:
                    curr = curr.children.setdefault(c, TrieNode())
                curr.end = True
            def search(self, s, i, j):
                curr = self.root
                for idx in range(i, j+1):
                    if s[idx] not in curr.children:
                        return False
                    curr = curr.children[s[idx]]
                return curr.end
        
        trie = Trie()
        longest = 0
        for w in wordDict:
            trie.insert(w)
            longest = max(longest, len(w))
        dp = [False] * (len(s)+1)
        dp[len(s)] = True
        for i in range(len(s)-1, -1, -1):
            rBound = min(len(s), i+longest)
            for j in range(i, rBound):
                if trie.search(s, i, j) and dp[j+1]:
                    dp[i] = True
        return dp[0]

    # 185
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j]+1)
        return max(dp)
        # Alternative solution using greedy + bisect
        # tails = []
        # for x in nums:
            # i = bisect.bisect_left(tails, x)
        #     if i == len(tails):
        #         tails.append(x)
        #     else:
        #         tails[i] = x
        # return len(tails)
    
    # 186
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 == 1:
            return False
        half = total // 2
        dp = [False] * (half+1)
        dp[0] = True
        for num in nums:
            for i in range(half, num-1, -1):
                dp[i] = dp[i] or dp[i - num]
        return dp[half]
    
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
