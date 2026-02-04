from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 122
    def subsetXORSum(self, nums: List[int]) -> int:
        pass
    
    # 123
    def subsets(self, nums: List[int]) -> List[List[int]]:
        pass

    # 124
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        def dfs(i, curr, total):
            if total == target:
                res.append(curr.copy())
                return
            for j in range(i, len(nums)):
                if total + nums[j] > target:
                    return
                curr.append(nums[j])
                dfs(j, curr, total + nums[j])
                curr.pop()
        
        res = []
        nums.sort()
        dfs(0, [], 0)
        return res

    # 125
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        pass

    # 126
    def combine(self, n: int, k: int) -> List[List[int]]:
        pass

    # 127
    def permute(self, nums: List[int]) -> List[List[int]]:
        pass

    # 128
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        pass

    # 129
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        pass

    # 130
    def generateParenthesis(self, n: int) -> List[str]:
        pass

    # 131
    def exist(self, board: List[List[str]], word: str) -> bool:
        def dfs(r, c, i):
            if i == len(word):
                return True
            if (
                r < 0 or c < 0 or r >= R or c >= C or
                word[i] != board[r][c] or board[r][c] == '#'
            ):
                return False
            board[r][c] = '#'
            res = any(dfs(r+dr, c+dc, i+1) for dr, dc in dirs)
            board[r][c] = word[i]
            return res
        
        R, C = len(board), len(board[0])
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        for r in range(R):
            for c in range(C):
                if dfs(r, c, 0):
                    return True
        return False
    
    # 132
    def partition(self, s: str) -> List[List[str]]:
        pass

    # 133
    def letterCombinations(self, digits: str) -> List[str]:
        pass

    # 134
    def makesquare(self, matchsticks: List[int]) -> bool:
        pass

    # 135
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        pass

    # 136
    def solveNQueens(self, n: int) -> List[List[str]]:
        pass

    # 137
    def totalNQueens(self, n: int) -> int:
        pass

    # 138
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        pass

if __name__ == "__main__":
    s = Solution()
