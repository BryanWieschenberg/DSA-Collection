from collections import deque
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) == 1:
            return 0
        minval, maxval = prices[0], 0
        for i in range(1, len(prices)):
            if prices[i] > minval:
                maxval = max(maxval, prices[i] - minval)
            minval = min(minval, prices[i])
        return maxval

    def lengthOfLongestSubstring(self, s: str) -> int:
        mp, l, res = {}, 0, 0
        for r in range(len(s)):
            if s[r] in mp:
                l = max(mp[s[r]] + 1, l)
            mp[s[r]] = r
            res = max(res, r-l + 1)
        return res
    
    def characterReplacement(self, s: str, k: int) -> int:
        cts = {}
        res = 0
        l = 0
        maxf = 0

        for r in range(len(s)):
            cts[s[r]] = 1 + cts.get(s[r], 0)
            maxf = max(maxf, cts[s[r]])
            while (r-l+1) - maxf > k:
                cts[s[l]] -= 1
                l += 1
            res = max(res, r-l+1)
        return res
    
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s2) < len(s1):
            return False
        s1_count = {}
        s2_count = {}
        for s in s1:
            s1_count[s] = 1 + s1_count.get(s, 0)
        l = 0
        for r in range(len(s2)):
            if (r - l) + 1 > len(s1):
                s2_count[s2[l]] -= 1
                if not s2_count[s2[l]]:
                    del s2_count[s2[l]]
                l += 1
            s2_count[s2[r]] = 1 + s2_count.get(s2[r], 0)
            if s1_count == s2_count:
                return True
        return False
    
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""
        res = ""
        smap, tmap = [0] * 58, [0] * 58
        chars = set(t)
        for c in t:
            tmap[ord(c) - ord('A')] += 1
        l, r = 0, 0
        for r in range(len(s)):
            if s[r] in chars:
                smap[ord(s[r]) - ord('A')] += 1
            if l+1 < len(s) and s[l] not in chars:
                l += 1
            while smap[ord(s[l]) - ord('A')] > tmap[ord(s[l]) - ord('A')]:
                smap[ord(s[l]) - ord('A')] -= 1
                l += 1
                while s[l] not in chars:
                    l += 1
            equal = True
            for i in range(58):
                if (
                    tmap[i] == 0 and smap[i] != 0 or
                    tmap[i] > 0 and smap[i] < tmap[i]
                ):
                    equal = False
                    break
            if equal and (not res or (r-l)+1 < len(res)):
                res = s[l : r+1]
        return res

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        l, vals = 0, [0] * (len(nums) - k+1)
        q = deque()
        
        for r in range(len(nums)):
            while q and nums[q[-1]] < nums[r]:
                q.pop()
            q.append(r)

            if l > q[0]:
                q.popleft()
            
            if (r+1) >= k:
                vals[r-k+1] = nums[q[0]]
                l += 1
        return vals
    
s = Solution()

# print(s. maxProfit ( prices=[10,1,5,6,7,1] )) # 6

# print(s. lengthOfLongestSubstring ( s="zxyzxyz" )) # 3

# print(s. characterReplacement ( s="XYYX", k=2 )) # 4

# print(s. checkInclusion ( s1="ab", s2="lecabee" )) # True

# print(s. minWindow ( s="cabwefgewcwaefgcf", t="cae" )) # "cwae"

# print(s. maxSlidingWindow ( nums=[1,2,1,0,4,2,6], k=3 )) # [2,2,4,4,6]
