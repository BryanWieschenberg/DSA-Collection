from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from collections import defaultdict, deque
from typing import List

class Solution:
    # 36
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        if not k: return False
        seen = set()
        l = 0
        for r in range(len(nums)):
            if nums[r] in seen:
                return True
            if r >= k:
                seen.remove(nums[l])
                l += 1
            seen.add(nums[r])
        return False
    
    # 37
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) == 1: return 0
        l = 0 # l = lowest val seen
        res = 0
        for r in range(1, len(prices)):
            if prices[r] < prices[l]:
                l = r
            elif prices[r] > prices[l]:
                res = max(res, prices[r] - prices[l])
        return res
        
    # 38
    def lengthOfLongestSubstring(self, s: str) -> int:
        mp = {}
        l = 0
        res = 0

        for r in range(len(s)):
            if s[r] in mp:
                l = max(mp[s[r]] + 1, l)
            mp[s[r]] = r
            res = max(res, r - l + 1)
        return res

    # 39
    def characterReplacement(self, s: str, k: int) -> int:
        ct = defaultdict(int)
        res = 0
        l = 0
        maxFreq = 0
        for r in range(len(s)):
            ct[s[r]] += 1
            maxFreq = max(maxFreq, ct[s[r]])
            if (r - l + 1) - maxFreq > k:
                ct[s[l]] -= 1
                l += 1
            res = max(res, r - l + 1)
        return res

    # 40
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n1, n2 = len(s1), len(s2)
        if n1 > n2: return False

        s1ct, s2ct = [0] * 26, [0] * 26
        for i in range(n1):
            s1ct[ord(s1[i]) - ord('a')] += 1
            s2ct[ord(s2[i]) - ord('a')] += 1

        match = 0
        for i in range(26):
            match += (1 if s1ct[i] == s2ct[i] else 0)

        l = 0
        for r in range(n1, n2):
            if match == 26: return True
            iL = ord(s2[l]) - ord('a')
            iR = ord(s2[r]) - ord('a')
            
            s2ct[iR] += 1
            if s1ct[iR] == s2ct[iR]: match += 1
            elif s1ct[iR] == s2ct[iR] - 1: match -= 1

            s2ct[iL] -= 1
            if s1ct[iL] == s2ct[iL]: match += 1
            elif s1ct[iL] == s2ct[iL] + 1: match -= 1
            l += 1
        return match == 26
        
    # 41
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l = 0
        curr = 0
        res = float('inf')
        for r in range(len(nums)):
            curr += nums[r]
            while curr - nums[l] >= target:
                curr -= nums[l]
                l += 1
            if curr >= target:
                res = min(res, r - l + 1)
        return res if res != float('inf') else 0
        
    # 42
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        n = len(arr)
        l, r = 0, n-1
        while l < r:
            mid = (l + r) // 2
            if arr[mid] < x:
                l = mid + 1
            else:
                r = mid
        l, r = l-1, l
        while r - l - 1 < k:
            if l < 0:
                r += 1
            elif r >= n:
                l -= 1
            elif x - arr[l] <= arr[r] - x:
                l -= 1
            else:
                r += 1
        return arr[l+1 : r]
    
    # 43
    def minWindow(self, s: str, t: str) -> str:
        ns, nt = len(s), len(t)
        if ns < nt: return ""
        CHARS = 128 # to avoid ascii anomalies since full alphabet
        cs, ct = [0] * CHARS, [0] * CHARS
        match = l = 0
        res = ""
        for c in t: ct[ord(c)] += 1
        required = sum(1 for i in range(CHARS) if ct[i] > 0)
        
        for r in range(ns):
            iR = ord(s[r])
            cs[iR] += 1
            if ct[iR] and cs[iR] == ct[iR]:
                match += 1

            while match == required:
                if not res or (r - l + 1) < len(res):
                    res = s[l : r+1]
                iL = ord(s[l])
                cs[iL] -= 1
                if ct[iL] and cs[iL] < ct[iL]:
                    match -= 1
                l += 1
                
        return res
    
    # 44
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        l = 0
        n = len(nums)
        q = deque()
        res = [0] * (n - k + 1)
        for r in range(n):
            while q and nums[q[-1]] < nums[r]:
                q.pop()
            q.append(r)

            if l > q[0]:
                q.popleft()
            
            if (r + 1) >= k:
                res[r - k + 1] = nums[q[0]]
                l += 1
            r += 1
        return res
        
if __name__ == "__main__":
    s = Solution()
