from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 23
    def reverseString(self, s: List[str]) -> List[str]:
        for i in range(len(s) // 2):
            s[i], s[-i-1] = s[-i-1], s[i]
        return s
    
    # 24
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s)-1
        while l < r:
            while l < r and not s[l].isalnum(): l += 1
            while l < r and not s[r].isalnum(): r -= 1
            if l > r or s[l].lower() != s[r].lower():
                return False
            l += 1; r -= 1
        return True
    
    # 25
    def validPalindrome(self, s: str) -> bool:
        def isPalindrome(l, r):
            while l < r:
                while l < r and not s[l].isalnum(): l += 1
                while l < r and not s[r].isalnum(): r -= 1
                if l > r or s[l].lower() != s[r].lower():
                    return False
                l += 1; r -= 1
            return True

        l, r = 0, len(s)-1
        while l < r:
            while l < r and not s[l].isalnum(): l += 1
            while l < r and not s[r].isalnum(): r -= 1
            if l > r or s[l].lower() != s[r].lower():
                return isPalindrome(l, r-1) or isPalindrome(l+1, r)
            l += 1; r -= 1
        return True
    
    # 26
    def mergeAlternately(self, word1: str, word2: str) -> str:
        res = []
        for i in range(min(len(word1), len(word2))):
            res.extend([word1[i], word2[i]])
        if len(word1) > len(word2):
            res.extend(word1[len(word2):])
        elif len(word1) < len(word2):
            res.extend(word2[len(word1):])
        return "".join(res)
    
    # 27
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> List[int]:
        i = m-1
        j = n-1
        k = m+n-1

        while j >= 0:
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1
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
        l, r = 0, len(numbers)-1
        while l < r:
            if numbers[l] + numbers[r] < target:
                l += 1
            elif numbers[l] + numbers[r] > target:
                r -= 1
            else:
                return [l+1, r+1]
        return []
    
    # 30
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        n = len(nums)
        nums.sort()
        for i in range(n):
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
                    while 0 < l < len(nums) and nums[l] == nums[l-1]: l += 1
                    r -= 1
                    while 0 < r < len(nums) and nums[r] == nums[r+1]: r -= 1
        return res
    
    # 31
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        res = []
        n = len(nums)
        nums.sort()
        for i in range(n):
            if i > 0 and nums[i] == nums[i-1]: continue
            for j in range(i+1, n):
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
                        while 0 < l < len(nums) and nums[l] == nums[l-1]: l += 1
                        r -= 1
                        while 0 < r < len(nums) and nums[r] == nums[r+1]: r -= 1
        return res
    
    # 32
    def rotate(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        ct = start = 0
        while ct < n:
            curr = start
            prev = nums[start]
            while True:
                next = (curr + k) % n
                nums[next], prev = prev, nums[next]
                curr = next
                ct += 1
                if start == curr: break
            start += 1
        return nums
        
    # 33
    def maxArea(self, heights: List[int]) -> int:
        pass

    # 34
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        pass

    # 35
    def trap(self, height: List[int]) -> int:
        pass

if __name__ == "__main__":
    s = Solution()
