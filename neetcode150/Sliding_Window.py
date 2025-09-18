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
            
s = Solution()

# print(s. maxProfit ( prices=[10,1,5,6,7,1] )) # 6

# print(s. lengthOfLongestSubstring ( s="zxyzxyz" )) # 3
