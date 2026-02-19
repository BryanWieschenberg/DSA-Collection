from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import defaultdict, deque

class Solution:
    # 36
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        mp = {}
        for i, n in enumerate(nums):
            if n in mp and mp[n] + k >= i:
                return True
            mp[n] = i
        return False
        
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
        req = obt = 0
        ct1, ct2 = [0] * 26, [0] * 26
        for c in s1:
            ch = ord(c) - ord('a')
            if ct1[ch] == 0: req += 1
            ct1[ch] += 1
        l = 0
        for r in range(len(s2)):
            chR = ord(s2[r]) - ord('a')
            ct2[chR] += 1
            if ct2[chR] == ct1[chR]: obt += 1
            if ct2[chR] == ct1[chR]+1: obt -= 1
            if r >= len(s1):
                chL = ord(s2[l]) - ord('a')
                ct2[chL] -= 1
                if ct2[chL] == ct1[chL]: obt += 1
                if ct2[chL] == ct1[chL]-1: obt -= 1
                l += 1
            if req == obt:
                return True
        return False
            
    # 41
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        res = float('inf')
        curr = l = 0
        for r in range(len(nums)):
            curr += nums[r]
            while l < r and curr - nums[l] >= target:
                curr -= nums[l]
                l += 1
            if curr >= target:
                res = min(res, r-l+1)
        return res if res != float('inf') else 0
                
    # 42
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        l, r = 0, len(arr)-k
        while l < r:
            windStart = l + (r - l) // 2
            if x - arr[windStart] > arr[windStart + k] - x:
                l = windStart + 1
            else:
                r = windStart
        return arr[l : l+k]
        
    # 43
    def minWindow(self, s: str, t: str) -> str:
        res = ""
        req = obt = 0
        ctS, ctT = [0] * 128, [0] * 128
        for c in t:
            ch = ord(c)
            if ctT[ch] == 0: req += 1
            ctT[ch] += 1
        l = 0
        for r in range(len(s)):
            chR = ord(s[r])
            ctS[chR] += 1
            if ctS[chR] == ctT[chR]: obt += 1
            while req == obt:
                if len(res) > r-l+1 or not res:
                    res = s[l : r+1]
                chL = ord(s[l])
                ctS[chL] -= 1
                if ctS[chL] == ctT[chL]-1: obt -= 1
                l += 1
        return res
            
    # 44
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = [0] * (len(nums)-k+1)
        q = deque()
        l = 0
        for r in range(len(nums)):
            while q and nums[q[-1]] <= nums[r]:
                q.pop()
            q.append(r)
            while l > q[0]:
                q.popleft()
            if r >= k-1:
                res[l] = nums[q[0]]
                l += 1
        return res
            
if __name__ == "__main__":
    s = Solution()
