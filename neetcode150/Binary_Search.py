from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums)-1

        while l < r:
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
        
s = Solution()

# print(s. search ( nums=[2,5], target=5 )) # 3

# print(s. searchMatrix ( matrix=[[1,2,4,8],[10,11,12,13],[14,20,30,40]], target=10 )) # True
