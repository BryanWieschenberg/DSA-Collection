from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from Helper import API
from typing import List
from math import ceil

class Solution:
    # 59
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums)-1
        while l <= r:
            m = (l + r) // 2
            if nums[m] < target:
                l = m + 1
            elif nums[m] > target:
                r = m - 1
            else:
                return m
        return -1
    
    # 60
    def searchInsert(self, nums: List[int], target: int) -> int:
        if target > nums[-1]: return len(nums)
        l, r = 0, len(nums)-1
        while l < r:
            m = (l + r) // 2
            if nums[m] < target:
                l = m + 1
            else:
                r = m
        return l
    
    # 61
    def guessNumber(self, n: int, pick: int) -> int:
        l, r = 1, n
        while l <= r:
            m = (l + r) // 2
            res = API.guess(m, pick)
            if res == 1:
                l = m + 1
            elif res == -1:
                r = m - 1
            else:
                return m

    # 62
    def mySqrt(self, x: int) -> int:
        l, r = 0, x
        res = 0
        while l <= r:
            m = (l + r) // 2
            if m**2 < x:
                l = m + 1
                res = m
            elif m**2 > x:
                r = m - 1
            else:
                return m
        return res
    
    # 63
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        rows, cols = len(matrix), len(matrix[0])
        l, r = 0, rows*cols-1
        while l <= r:
            m = (l + r) // 2
            if matrix[m // cols][m % cols] < target:
                l = m + 1
            elif matrix[m // cols][m % cols] > target:
                r = m - 1
            else:
                return True
        return False
    
    # 64
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles)
        res = r
        while l <= r:
            m = l + (r - l) // 2
            time = 0
            for p in piles:
                time += ceil(p / m)
            if time <= h:
                res = min(res, m)
                r = m - 1
            else:
                l = m + 1
        return res
    
    # 65
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        l, r = max(weights), sum(weights)
        res = r
        while l <= r:
            cap = l + (r - l) // 2
            currVal, currDays = 0, 1
            for w in weights:
                if currVal + w <= cap:
                    currVal += w
                else:
                    currVal = w
                    currDays += 1
            if currDays <= days:
                res = min(res, cap)
                r = cap - 1
            else:
                l = cap + 1
        return res
    
    # 66
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums)-1
        while l < r:
            m = l + (r - l) // 2
            if nums[m] < nums[r]:
                r = m
            else:
                l = m + 1
        return nums[l]
    
    # 67
    def searchRotated(self, nums: List[int], target: int) -> int:
        pass

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
