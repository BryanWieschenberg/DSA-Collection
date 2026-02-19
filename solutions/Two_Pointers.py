from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 23
    def reverseString(self, s: List[str]) -> List[str]:
        l, r = 0, len(s)-1
        while l < r:
            s[l], s[r] = s[r], s[l]
            l += 1
            r -= 1
        return s
    
    # 24
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s)-1
        while l < r:
            while l < len(s) and not s[l].isalnum(): l += 1
            while r >= 0 and not s[r].isalnum(): r -= 1
            if l < len(s) and r >= 0 and s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        return True
        
    # 25
    def validPalindrome(self, s: str) -> bool:
        def isPal(l, r):
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True
        
        l, r = 0, len(s)-1
        while l < r:
            if s[l] != s[r]:
                return isPal(l+1, r) or isPal(l, r-1)
            l += 1
            r -= 1
        return True
        
    # 26
    def mergeAlternately(self, word1: str, word2: str) -> str:
        res = []
        n1, n2 = len(word1), len(word2)
        for i in range(min(n1, n2)):
            res.append(word1[i])
            res.append(word2[i])
        if n1 > n2:
            res.extend(word1[n2:])
        if n2 > n1:
            res.extend(word2[n1:])
        return ''.join(res)
        
    # 27
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> List[int]:
        i, j = m-1, n-1
        for k in range(m+n-1, -1, -1):
            if j < 0:
                break
            if i >= 0 and nums1[i] >= nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
        return nums1

    # 28
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[k-1]:
                nums[k] = nums[i]
                k += 1
        return k
        
    # 29
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        mp = {}
        for i, n in enumerate(numbers):
            diff = target - n
            if diff in mp:
                return [mp[diff], i+1]
            mp[n] = i+1
        return []
    
    # 30
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        res = []
        for i in range(n-2):
            if i > 0 and nums[i] == nums[i-1]: continue
            l, r = i+1, n-1
            while l < r:
                if nums[i] + nums[l] + nums[r] < 0:
                    l += 1
                elif nums[i] + nums[l] + nums[r] > 0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l-1]: l += 1
                    while l < r and nums[r] == nums[r+1]: r -= 1
        return res
                
    # 31
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        res = []
        for i in range(n-3):
            if i > 0 and nums[i] == nums[i-1]: continue
            for j in range(i+1, n-2):
                if j > i+1 and nums[j] == nums[j-1]: continue
                l, r = j+1, n-1
                while l < r:
                    if nums[i] + nums[j] + nums[l] + nums[r] < target:
                        l += 1
                    elif nums[i] + nums[j] + nums[l] + nums[r] > target:
                        r -= 1
                    else:
                        res.append([nums[i], nums[j], nums[l], nums[r]])
                        l += 1
                        r -= 1
                        while l < r and nums[l] == nums[l-1]: l += 1
                        while l < r and nums[r] == nums[r+1]: r -= 1
        return res
        
    # 32
    def rotate(self, nums: List[int], k: int) -> List[int]:
        def rev(l, r):
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1
                
        n = len(nums)
        k %= n
        rev(0, n-1)
        rev(0, k-1)
        rev(k, n-1)
        return nums

    # 33
    def maxArea(self, heights: List[int]) -> int:
        def getHeight(l, r):
            return (r-l) * min(heights[l], heights[r])
        
        l, r = 0, len(heights)-1
        res = getHeight(l, r)
        while l < r:
            if heights[l] < heights[r]:
                l += 1
            else:
                r -= 1
            res = max(res, getHeight(l, r))
        return res
        
    # 34
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        res = 0
        l, r = 0, len(people)-1
        while l <= r:
            if people[l] + people[r] <= limit:
                l += 1
            r -= 1
            res += 1
        return res
            
    # 35
    def trap(self, height: List[int]) -> int:
        highL, highR = height[0], height[-1]
        res = 0
        l, r = 0, len(height)-1
        while l < r:
            if highL < highR:
                l += 1
                highL = max(highL, height[l])
                res += highL - height[l]
            else:
                r -= 1
                highR = max(highR, height[r])
                res += highR - height[r]
        return res
     
if __name__ == "__main__":
    s = Solution()
