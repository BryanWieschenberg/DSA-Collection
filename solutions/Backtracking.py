from typing import List, Optional

from HELPER import TreeNode, TreeHelper

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = [[]]

        for n in nums:
            res += [subset + [n] for subset in res]
        
        return res

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        def dfs(root, total):
            if not root: return False
            
            sumtotal = total + root.val
            if sumtotal == targetSum and not (root.left or root.right):
                return True
            
            return (
                dfs(root.left, sumtotal) or
                dfs(root.right, sumtotal)
            )

        if not root: return False
        return dfs(root, 0)
    
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        def dfs(i, cur, total):
            if total == target:
                res.append(cur)
                return
            
            for j in range(i, len(nums)):
                if total + nums[j] > target:
                    return
                dfs(j, cur + [nums[j]], total + nums[j])
        
        res = []
        nums.sort()

        dfs(0, [], 0)
        return res
    
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        def dfs(i, cur, total):
            if total == target:
                res.append(cur)
                return
            if total > target:
                return
            
            prev = -1
            for j in range(i, len(candidates)):
                if candidates[j] == prev:
                    continue
                if total + candidates[j] > target:
                    return
                dfs(j+1, cur + [candidates[j]], total + candidates[j])
                prev = candidates[j]
                
        candidates.sort()
        res = []
        dfs(0, [], 0)
        return res

    def permute(self, nums: List[int]) -> List[List[int]]:
        def dfs(cur):
            if len(cur) == len(nums):
                res.append(cur)
                return

            for i in range(len(nums)):
                if nums[i] in cur:
                    continue
                dfs(cur + [nums[i]])
                
        res = []
        dfs(cur=[])
        return res

    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res = [[]]
        nums.sort()
        start = 0

        for i, n in enumerate(nums):
            if i > 0 and nums[i] == nums[i - 1]:
                new_subsets = [subset + [n] for subset in res[start:]]
            else:
                new_subsets = [subset + [n] for subset in res]
            start = len(res)
            res += new_subsets
        
        return res
    
s = Solution()
h = TreeHelper()

# print( s. subsets ( nums=[1,2,3] )) # [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

# print( s. hasPathSum ( root=h.toTree([1,2,3]), targetSum=3 )) # True

# print( s. combinationSum ( nums=[2,5,6,9], target=9 )) # [[2,2,5],[9]]

# print( s. combinationSum2 ( candidates = [9,2,2,4,6,1,5], target = 8 )) # [[1, 2, 5], [2, 2, 4], [2, 6]]

# print( s. permute ( nums=[1,2,3] )) # [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

# print( s. subsetsWithDup ( nums=[1,2,1] )) # [[], [1], [1, 1], [2], [1, 2], [1, 1, 2]
