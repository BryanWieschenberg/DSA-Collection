from typing import List

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        l, r = 0, len(nums)-1
        i = 0
        while i <= r:
            if nums[i] == 0:
                nums[l], nums[i] = nums[i], nums[l]
                l += 1
            elif nums[i] == 2:
                nums[i], nums[r] = nums[r], nums[i]
                r -= 1
                i -= 1
            i += 1
        return nums

s = Solution()

print(s. sortColors ( nums=[2,0,2,1,1,0] )) # [0,0,1,1,2,2]
