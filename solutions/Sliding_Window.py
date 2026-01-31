from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import defaultdict

class Solution:
    # 36
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        pass
    
    # 37
    def maxProfit(self, prices: List[int]) -> int:
        res = l = 0
        for r in range(len(prices)):
            if prices[r] <= prices[l]:
                l = r
            else:
                res = max(res, prices[r] - prices[l])
        return res
            
    # 38
    def lengthOfLongestSubstring(self, s: str) -> int:
        mp = {}
        res = l = 0
        for r in range(len(s)):
            if s[r] in mp:
                l = max(l, mp[s[r]] + 1)
            mp[s[r]] = r
            res = max(res, r - l + 1)
        return res
    
    # 39
    def characterReplacement(self, s: str, k: int) -> int:
        ct = defaultdict(int)
        res = l = maxF = 0
        for r in range(len(s)):
            ct[s[r]] += 1
            maxF = max(maxF, ct[s[r]])
            while (r - l + 1) - maxF > k:
                ct[s[l]] -= 1
                l += 1
            res = max(res, r - l + 1)
        return res
    
    # 40
    def checkInclusion(self, s1: str, s2: str) -> bool:
        pass
        
    # 41
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        pass
        
    # 42
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        pass
    
    # 43
    def minWindow(self, s: str, t: str) -> str:
        sCt, tCt = [0] * 128, [0] * 128
        res, matching, required, l = "", 0, 0, 0
        for i in range(len(t)):
            if tCt[ord(t[i])] == 0:
                required += 1
            tCt[ord(t[i])] += 1
            
        for r in range(len(s)):
            rc = ord(s[r])
            sCt[rc] += 1
            if tCt[rc] > 0 and sCt[rc] == tCt[rc]:
                matching += 1
            while matching == required:
                if not res or r - l + 1 < len(res):
                    res = s[l : r+1]
                lc = ord(s[l])
                if tCt[lc] > 0 and sCt[lc] == tCt[lc]:
                    matching -= 1
                sCt[lc] -= 1
                l += 1
        return res
        
    # 44
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        pass
        
if __name__ == "__main__":
    s = Solution()
