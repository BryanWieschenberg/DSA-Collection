from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from Helper import phoneMap

class Solution:
    # 122
    def subsetXORSum(self, nums: List[int]) -> int:
        pass
    
    # 123
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def dfs(start):
            res.append(curr.copy())
            for i in range(start, len(nums)):
                curr.append(nums[i])
                dfs(i+1)
                curr.pop()
            
        res, curr = [], []
        dfs(0)
        return res
    
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
        def dfs(total, start):
            if total == target:
                res.append(curr.copy())
                return
            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i-1]:
                    continue
                if total + candidates[i] > target:
                    return
                curr.append(candidates[i])
                dfs(total + candidates[i], i+1)
                curr.pop()

        candidates.sort()
        res, curr = [], []
        dfs(0, 0)
        return res

    # 126
    def combine(self, n: int, k: int) -> List[List[int]]:
        pass

    # 127
    def permute(self, nums: List[int]) -> List[List[int]]:
        def dfs(start):
            if start >= len(nums):
                res.append(nums[:])
                return
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                dfs(start+1)
                nums[start], nums[i] = nums[i], nums[start]

        res = []
        dfs(0)
        return res

    # 128
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        def dfs(start):
            res.append(curr.copy())
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i-1]:
                    continue
                curr.append(nums[i])
                dfs(i+1)
                curr.pop()

        nums.sort()
        res, curr = [], []
        dfs(0)
        return res

    # 129
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        pass

    # 130
    def generateParenthesis(self, n: int) -> List[str]:
        def dfs(op, cl):
            if op == cl == n:
                res.append(''.join(curr))
                return
            if op < n:
                curr.append('(')
                dfs(op+1, cl)
                curr.pop()
            if cl < op:
                curr.append(')')
                dfs(op, cl+1)
                curr.pop()
        
        res, curr = [], []
        dfs(0, 0)
        return res

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
        def isPalindrome(l, r):
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True
        
        def dfs(start):
            if start >= len(s):
                res.append(curr.copy())
                return
            for i in range(start, len(s)):
                if not isPalindrome(start, i):
                    continue
                curr.append(s[start : i+1])
                dfs(i+1)
                curr.pop()

        res, curr = [], []
        dfs(0)
        return res
    
    # 133
    def letterCombinations(self, digits: str) -> List[str]:
        def dfs(start):
            if start >= len(digits):
                res.append(''.join(curr))
                return
            digit = digits[start]
            for letter in phoneMap[digit]:
                curr.append(letter)
                dfs(start+1)
                curr.pop()

        if not digits:
            return []
        res, curr = [], []
        dfs(0)
        return res

    # 134
    def makesquare(self, matchsticks: List[int]) -> bool:
        pass

    # 135
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        pass

    # 136
    def solveNQueens(self, n: int) -> List[List[str]]:
        def dfs(r):
            if r == n:
                res.append([''.join(row) for row in board])
                return
            for c in range(n):
                if c in cols or (r + c) in diagPos or (r - c) in diagNeg:
                    continue
                cols.add(c); diagPos.add(r + c); diagNeg.add(r - c)
                board[r][c] = 'Q'
                dfs(r+1)
                cols.remove(c); diagPos.remove(r + c); diagNeg.remove(r - c)
                board[r][c] = '.'

        # diagPos: BL -> TR, each diagonal is (r + c)
        # diagNeg: TL -> BR, each diagonal is (r - c)
        cols, diagPos, diagNeg = set(), set(), set()
        res = []
        board = [['.'] * n for _ in range(n)]
        dfs(0)
        return res

    # 137
    def totalNQueens(self, n: int) -> int:
        pass

    # 138
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        pass

if __name__ == "__main__":
    s = Solution()
