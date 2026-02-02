from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from Helper import API

class Solution:
    # 59
    def search(self, nums: List[int], target: int) -> int:
        pass
    
    # 60
    def searchInsert(self, nums: List[int], target: int) -> int:
        pass
    
    # 61
    def guessNumber(self, n: int, pick: int) -> int:
        pass

    # 62
    def mySqrt(self, x: int) -> int:
        pass
    
    # 63
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        pass
    
    # 64
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        pass
    
    # 65
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        pass
    
    # 66
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums)-1
        while l < r:
            m = l + (r - l) // 2
            if nums[m] >= nums[r]:
                l = m + 1
            else:
                r = m
        return nums[l]
        
    # 67
    def searchRotated(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums)-1
        while l <= r:
            m = l + (r - l) // 2
            if nums[m] == target:
                return m

            if nums[l] <= nums[m]:
                if target > nums[m] or target < nums[l]:
                    l = m + 1
                else:
                    r = m - 1
            else:
                if target < nums[m] or target > nums[r]:
                    r = m - 1
                else:
                    l = m + 1
        return -1
        
    # 68
    def searchRotated2(self, nums: List[int], target: int) -> bool:
        pass
    
    # 69
    class TimeMap:
        def __init__(self):
            pass

        def set(self, key: str, value: str, timestamp: int) -> None:
            pass

        def get(self, key: str, timestamp: int) -> str:
            pass
        
    # 70
    def splitArray(self, nums: List[int], k: int) -> int:
        pass
    
    # 71
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        pass
    
    # 72
    def findInMountainArray(self, mountainArr: List[int], target: int) -> int:
        pass

if __name__ == "__main__":
    s = Solution()
