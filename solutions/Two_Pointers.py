from typing import List
import time

class Solution:
    # https://neetcode.io/problems/valid-palindrome?list=neetcode150
    # Time: O(n)
    # Space: O(1)
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s)-1

        while l < r:
            if not s[l].isalnum():
                l += 1
                continue
            if not s[r].isalnum():
                r -= 1
                continue
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        
        return True
    
    # https://neetcode.io/problems/two-sum-ii-input-array-is-sorted?list=neetcode150
    # Time: O(n)
    # Space: O(1)
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l, r = 0, len(numbers) - 1

        while l != r:
            total = numbers[l] + numbers[r]
            if total == target:
                return [l+1, r+1]
            elif total < target:
                l += 1
            else:
                r -= 1
        return None

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i-1]:
                continue

            l, r = i + 1, len(nums)-1
            while l < r:
                total = nums[i] + nums[l] + nums[r]
                if total < 0:
                    l += 1
                elif total > 0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l-1]:
                        l += 1
                    while l < r and nums[r] == nums[r+1]:
                        r -= 1
        return res
    
    # https://neetcode.io/problems/container-with-most-water?list=neetcode150
    # Time: O(n)
    # Space: O(1)
    def maxArea(self, heights: List[int]) -> int:
        l, r, res = 0, len(heights)-1, 0
        while l < r:
            area = (r - l) * min(heights[l], heights[r])
            res = max(area, res)
            if heights[l] < heights[r]:
                l += 1
            else:
                r -= 1
        return res
    
    # https://neetcode.io/problems/trapping-rain-water?list=neetcode150
    # Time: O(n)
    # Space: O(1)
    def trap(self, heights: List[int]) -> int:
        l, r, res = 0, len(heights)-1, 0
        maxL, maxR = heights[l], heights[r]
        while l < r:
            if heights[l] < heights[r]:
                l += 1
                maxL = max(maxL, heights[l])
                res += maxL - heights[l]
            else:
                r -= 1
                maxR = max(maxR, heights[r])
                res += maxR - heights[r]
        return res
    
s = Solution()

# print(s. isPalindrome ( "Was it a car or a cat I saw?" )) # True

# print(s. twoSum ( numbers=[1,2,5,7,9], target=12 )) # [1,2]

# print(s. threeSum ( nums=[-1,0,1,2,-1,-4] )) # [[-1,-1,2],[-1,0,1]]

# print(s. maxArea ( heights=[1,7,2,5,4,7,3,6] )) # 49

# print(s. trap ( heights=[0,2,0,3,1,0,1,3,2,1] )) # 9
