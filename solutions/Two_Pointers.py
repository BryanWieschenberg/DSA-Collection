from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 23
    def reverseString(self, s: List[str]) -> List[str]:
        pass
    
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
        pass
    
    # 26
    def mergeAlternately(self, word1: str, word2: str) -> str:
        pass
    
    # 27
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> List[int]:
        pass
    
    # 28
    def removeDuplicates(self, nums: List[int]) -> int:
        pass
    
    # 29
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        pass
    
    # 30
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i-1]: continue
            l, r = i+1, len(nums)-1
            while l < r:
                while l > i+1 and nums[l] == nums[l-1]: l += 1
                while r < len(nums)-1 and nums[r] == nums[r+1]: r -= 1
                if l >= r: break
                if nums[i] + nums[l] + nums[r] < 0:
                    l += 1
                elif nums[i] + nums[l] + nums[r] > 0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
        return res
        
    # 31
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        pass
    
    # 32
    def rotate(self, nums: List[int], k: int) -> List[int]:
        pass
    
    # 33
    def maxArea(self, heights: List[int]) -> int:
        l, r = 0, len(heights)-1
        res = 0
        while l < r:
            res = max(res, min(heights[l], heights[r]) * (r-l))
            if heights[l] < heights[r]:
                l += 1
            else:
                r -= 1
        return res
        
    # 34
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        pass
        
    # 35
    def trap(self, height: List[int]) -> int:
        pass
        
if __name__ == "__main__":
    s = Solution()
