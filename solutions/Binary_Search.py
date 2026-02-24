from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import defaultdict
from Helper import API
from bisect import *
from math import ceil

class Solution:
    # 59
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums)-1
        while l <= r:
            m = l + (r - l) // 2
            if nums[m] < target:
                l = m + 1
            elif nums[m] > target:
                r = m - 1
            else:
                return m
        return -1
        # SOLUTION 2:
        i = bisect_left(nums, target)
        if i < len(nums) and nums[i] == target:
            return i
        return -1
        
    # 60
    def searchInsert(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums)
        while l < r:
            m = l + (r - l) // 2
            if nums[m] < target:
                l = m + 1
            else:
                r = m
        return l
        
    # 61
    def guessNumber(self, n: int, pick: int) -> int:
        l, r = 1, n
        while l < r:
            m = l + (r - l) // 2
            if API.guess(m, pick) == 1:
                l = m + 1
            elif API.guess(m, pick) == -1:
                r = m - 1
            else:
                return m
        return l
    
    # 62
    def mySqrt(self, x: int) -> int:
        l, r = 0, x
        res = 0
        while l <= r:
            m = l + (r - l) // 2
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
        R, C = len(matrix), len(matrix[0])
        l, r = 0, R*C-1
        while l <= r:
            m = l + (r - l) // 2
            cell = matrix[m//C][m%C]
            if cell < target:
                l = m + 1
            elif cell > target:
                r = m - 1
            else:
                return True
        return False
        
    # 64
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles)
        while l < r:
            m = l + (r - l) // 2
            hrs = 0
            for p in piles:
                hrs += ceil(p / m)
            if hrs > h:
                l = m + 1
            else:
                r = m
        return l
        
    # 65
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def canShip(cap, limit):
            days, curr = 1, 0
            for w in weights:
                if curr + w <= cap:
                    curr += w
                else:
                    days += 1
                    curr = w
                if days > limit:
                    return False
            return True

        l, r = max(weights), sum(weights)
        while l < r:
            m = l + (r - l) // 2
            if not canShip(m, days):
                l = m + 1
            else:
                r = m
        return l
        
    # 66
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums)-1
        while l < r:
            m = l + (r - l) // 2
            if nums[m] > nums[r]:
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
            self.mp = defaultdict(list)

        def set(self, key: str, value: str, timestamp: int) -> None:
            self.mp[key].append((value, timestamp))

        def get(self, key: str, timestamp: int) -> str:
            if key not in self.mp or timestamp < self.mp[key][0][1]:
                return ""
            pairs = self.mp[key]
            l, r = 0, len(pairs)
            while l < r:
                m = l + (r - l) // 2
                if pairs[m][1] <= timestamp:
                    l = m + 1
                else:
                    r = m
            return pairs[l-1][0]
        
    # 70
    def splitArray(self, nums: List[int], k: int) -> int:
        pass
    
    # 71
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        if len(A) > len(B):
            A, B = B, A
        l, r = 0, len(A)-1
        total = len(A) + len(B)
        half = total // 2
        while True:
            i = l + (r - l) // 2
            j = half - i - 2
            Aleft = A[i] if i >= 0 else float('-inf')
            Aright = A[i+1] if i+1 < len(A) else float('inf')
            Bleft = B[j] if j >= 0 else float('-inf')
            Bright = B[j+1] if j+1 < len(B) else float('inf')
            if Aleft <= Bright and Bleft <= Aright:
                if total % 2 == 1:
                    return min(Aright, Bright)
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
            elif Aright < Bleft:
                l = i + 1
            else:
                r = i - 1
                    
    # 72
    def findInMountainArray(self, mountainArr: List[int], target: int) -> int:
        pass

if __name__ == "__main__":
    s = Solution()
