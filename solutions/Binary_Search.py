from collections import defaultdict
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums)-1

        while l <= r:
            ind = (l + r) // 2
            if nums[ind] > target:
                r = ind - 1
            elif nums[ind] < target:
                l = ind + 1
            else:
                return ind
        return -1

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        l, r = 0, (len(matrix) * len(matrix[0]))-1
        while l <= r:
            mid = (l + r) // 2
            val = matrix[mid // len(matrix[0])][mid % len(matrix[0])]
            if val < target:
                l = mid + 1
            elif val > target:
                r = mid - 1
            else:
                return True
        return False
        
    def findMin(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        l, r = 1, len(nums)-1
        prev = nums[0]
        min_val = nums[0]

        while l <= r:
            mid = (l + r) // 2
            print(l, r, mid, prev)
            if nums[mid] >= prev:
                prev = nums[mid]
                l = mid + 1
            else:
                prev = nums[mid]
                r = mid - 1
            min_val = min(prev, min_val)
        return min_val

    def search(self, nums: List[int], target: int) -> int:
        if len(nums) == 1:
            if nums[0] == target:
                return 0
            else:
                return -1
        l, r = 1, len(nums)-1
        prev = nums[0]
        midcut = [0, nums[0]]
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] >= prev:
                prev = nums[mid]
                l = mid + 1
            else:
                prev = nums[mid]
                r = mid - 1
            if prev < midcut[1]:
                midcut = [mid, prev]
        
        l, r = midcut[0], (midcut[0]-1) + len(nums)

        while l <= r:
            mid = (l + r) // 2
            if nums[mid % len(nums)] < target:
                l = mid + 1
            elif nums[mid % len(nums)] > target:
                r = mid - 1
            else:
                return mid % len(nums)
        return -1
    
    class TimeMap:
        def __init__(self):
            self.store = defaultdict(list)

        def set(self, key: str, value: str, timestamp: int) -> None:
            self.store[key].append((timestamp, value))

        def get(self, key: str, timestamp: int) -> str:
            if key not in self.store:
                return ""

            arr = self.store[key]
            l, r = 0, len(arr)-1
            res = ""
            
            while l <= r:
                mid = (l + r) // 2
                if arr[mid][0] <= timestamp:
                    res = arr[mid][1]
                    l = mid + 1
                else:
                    r = mid - 1 
            return res
    
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        total = len(nums1) + len(nums2)
        half = total // 2
        if len(B) < len(A):
            A, B = B, A
        l, r = 0, len(A) - 1
        while True:
            i = (l + r) // 2 # A mid
            j = half - i - 2 # B mid

            Aleft = A[i] if i >= 0 else float('-inf')
            Aright = A[i + 1] if i+1 < len(A) else float('inf')
            Bleft = B[j] if j >= 0 else float('-inf')
            Bright = B[j + 1] if  j+1 < len(B) else float('inf')

            if Aleft <= Bright and Bleft <= Aright:
                if total % 2: # Odd
                    return min(Aright, Bright)
                else: # Even
                    return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
            elif Aleft > Bright:
                r = i - 1
            else:
                l = i + 1

    def firstBadVersion(self, n: int, bad: int) -> int:
        def isBadVersion(mid):
            return mid >= bad
        
        l, r = 1, n
        mid = 0
        while l <= r:
            mid = (l + r) // 2
            if isBadVersion(mid):
                r = mid - 1
            else:
                l = mid + 1
        return l
    
    def guessNumber(self, n: int, pick: int) -> int:
        def guess(mid):
            if mid < pick:
                return 1
            elif mid > pick:
                return -1
            else:
                return 0

        l, r = 1, n
        while True:
            m1 = l + (r - l) // 3
            m2 = r - (r - l) // 3
            if guess(m1) == 0:
                return m1
            if guess(m2) == 0:
                return m2
            if guess(m1) + guess(m2) == 0:
                l = m1 + 1
                r = m2 - 1
            elif guess(m1) == -1:
                r = m1 - 1
            else:
                l = m2 + 1

s = Solution()

# print(s. search ( nums=[2,5], target=5 )) # 3

# print(s. searchMatrix ( matrix=[[1,2,4,8],[10,11,12,13],[14,20,30,40]], target=10 )) # True

# print(s. findMin ( nums=[3,4,5,6,1,2] )) # 1

# print(s. search ( nums=[3,4,5,6,1,2], target=1 )) # 4

# timeMap = s.TimeMap()
# timeMap.set("alice", "happy", 1)
# print(timeMap.get("alice", 1)) # "happy"
# print(timeMap.get("alice", 2)) # "happy"
# timeMap.set("alice", "sad", 3)
# print(timeMap.get("alice", 3)) # "sad"

# print(s. findMedianSortedArrays ( nums1=[1,3], nums2=[2,4] )) # 2.5

# print(s. firstBadVersion ( n=5, bad=4 )) # 4

# print(s. guessNumber ( n=5, pick=3 )) # 3
