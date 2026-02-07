from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import defaultdict

class Solution:
    # 1
    def getConcatenation(self, nums: List[int]) -> List[int]:
        pass

    # 2
    def hasDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))

    # 3
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        ct = [0] * 26
        for i in range(len(s)):
            ct[ord(s[i]) - ord('a')] += 1
            ct[ord(t[i]) - ord('a')] -= 1
        for i in range(26):
            if ct[i] > 0:
                return False
        return True
    
    # 4
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        mp = {}
        for i, n in enumerate(nums):
            diff = target - n
            if diff in mp:
                return [mp[diff], i]
            mp[n] = i
        return []
        
    # 5
    def longestCommonPrefix(self, strs: List[str]) -> str:
        pass
    
    # 6
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            ct = [0] * 26
            for c in s:
                ct[ord(c) - ord('a')] += 1
            res[tuple(ct)].append(s)
        return list(res.values())
            
    # 7
    def removeElement(self, nums: List[int], val: int) -> int:
        pass
        
    # 8
    def majorityElement(self, nums: List[int]) -> int:
        pass
        
    # 9
    class MyHashSet:
        def __init__(self):
            pass

        def add(self, key: int) -> None:
            pass

        def remove(self, key: int) -> None:
            pass

        def contains(self, key: int) -> bool:
            pass
    
    # 10
    class MyHashMap:
        def __init__(self):
            pass

        def put(self, key: int, value: int) -> None:
            pass

        def get(self, key: int) -> int:
            pass

        def remove(self, key: int) -> None:
            pass
    
    # 11
    def sortArray(self, nums: List[int]) -> List[int]:
        pass
        
    # 12
    def sortColors(self, nums: List[int]) -> List[int]:
        pass
    
    # 13
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = defaultdict(int)
        for n in nums:
            freq[n] += 1
        ct = [[] for _ in range(len(nums)+1)]
        for f in freq:
            ct[freq[f]].append(f)
        res = []
        for i in range(len(ct)-1, -1, -1):
            for j in range(len(ct[i])):
                res.append(ct[i][j])
                if len(res) >= k:
                    return res
        return res
            
    # 14
    class EncodeDecode:
        def encode(self, strs: List[str]) -> str:
            res = []
            for s in strs:
                res.append(f'{len(s)}#{s}')
            return "".join(res)
        
        def decode(self, s: str) -> List[str]:
            i = 0
            res = []
            while i < len(s):
                start = i
                while s[i].isdigit():
                    i += 1
                dist = int(s[start : i])
                i += 1
                res.append(s[i : i+dist])
                i += dist
            return res
            
    # 15
    class NumMatrix:
        def __init__(self, matrix: List[List[int]]):
            pass
        
        def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
            pass
    
    # 16
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1] * len(nums)
        prod = 1
        for i in range(1, len(nums)):
            prod *= nums[i-1]
            res[i] *= prod
        prod = 1
        for i in range(len(nums)-2, -1, -1):
            prod *= nums[i+1]
            res[i] *= prod
        return res
            
    # 17
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        for r in range(len(board)):
            rows, cols, subs = set(), set(), set()
            for c in range(len(board[r])):
                row = board[r][c]
                col = board[c][r]
                sub = board[r // 3 * 3 + c // 3][r % 3 * 3 + c % 3]
                if (
                    row in rows or
                    col in cols or
                    sub in subs
                ):
                    return False
                if row != '.': rows.add(row)
                if col != '.': cols.add(col)
                if sub != '.': subs.add(sub)
        return True
        
    # 18
    def longestConsecutive(self, nums: List[int]) -> int:
        numsSet = set(nums)
        res = 0
        for n in nums:
            if n-1 not in numsSet:
                i = 1
                while n+i in numsSet:
                    i += 1
                res = max(res, i)
        return res
            
    # 19
    def maxProfit(self, prices: List[int]) -> int:
        pass
        
    # 20
    def majorityElement2(self, nums: List[int]) -> int:
        pass
        
    # 21
    def subarraySum(self, nums: List[int], k: int) -> int:
        pass
        
    # 22
    def firstMissingPositive(self, nums: List[int]) -> int:
        pass
        
if __name__ == "__main__":
    s = Solution()
