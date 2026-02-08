from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import defaultdict, deque

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
        req, obt = [0] * 26, [0] * 26
        reqCt = obtCt = l = 0
        for c in s1:
            ch = ord(c) - ord('a')
            if req[ch] == 0:
                reqCt += 1
            req[ord(c) - ord('a')] += 1
        for r in range(len(s2)):
            chR = ord(s2[r]) - ord('a')
            obt[chR] += 1
            if obt[chR] == req[chR]:
                obtCt += 1
            elif obt[chR] == req[chR]+1:
                obtCt -= 1
            if r >= len(s1):
                chL = ord(s2[l]) - ord('a')
                if obt[chL] == req[chL]:
                    obtCt -= 1
                elif obt[chL] == req[chL]+1:
                    obtCt += 1
                obt[chL] -= 1
                l += 1
            if r - l + 1 == len(s1) and obtCt == reqCt:
                return True
        return False
            
    # 41
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        pass
        
    # 42
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        pass
    
    # 43
    def minWindow(self, s: str, t: str) -> str:
        sCt, tCt = [0] * 128, [0] * 128
        l = req = obt = 0
        res = ""
        for c in t:
            ch = ord(c)
            if tCt[ch] == 0:
                req += 1
            tCt[ch] += 1
        for r in range(len(s)):
            cR = ord(s[r])
            sCt[cR] += 1
            if sCt[cR] == tCt[cR]:
                obt += 1
            while req == obt:
                if not res or len(res) > (r - l + 1):
                    res = s[l : r+1]
                cL = ord(s[l])
                sCt[cL] -= 1
                if sCt[cL] < tCt[cL]:
                    obt -= 1
                l += 1
        return res
        
    # 44
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = [0] * (len(nums)-k+1)
        q = deque()
        for r in range(len(nums)):
            while q and nums[q[-1]] <= nums[r]:
                q.pop()
            q.append(r)
            if r >= k - 1:
                while q and q[0] <= r - k:
                    q.popleft()
                res[r-k+1] = nums[q[0]]
        return res
            
if __name__ == "__main__":
    s = Solution()
