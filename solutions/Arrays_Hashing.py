from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import defaultdict

class Solution:
    # 1
    def getConcatenation(self, nums: List[int]) -> List[int]:
        return nums * 2
    
    # 2
    def hasDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for n in nums:
            if n in seen:
                return True
            seen.add(n)
        return False
        
    # 3
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t): return False
        ct = [0] * 26
        for s, t in zip(s, t):
            ct[ord(s) - ord('a')] += 1
            ct[ord(t) - ord('a')] -= 1
        for i in range(26):
            if ct[i]: return False
        return True
        
    # 4
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        i1 = i2 = 0
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in seen:
                i1, i2 = seen[diff], i
                break
            seen[nums[i]] = i
        return [i1, i2]
    
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
    def sortColors(self, nums: List[int]) -> None:
        pass
    
    # 13
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        pass
    
    # 14
    class EncodeDecode:
        def encode(self, strs: List[str]) -> str:
            pass
        
        def decode(self, s: str) -> List[str]:
            pass
    
    # 15
    class NumMatrix:
        def __init__(self, matrix: List[List[int]]):
            pass

        def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
            pass
    
    # 16
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        pass
    
    # 17
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        pass
    
    # 18
    def longestConsecutive(self, nums: List[int]) -> int:
        pass
    
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
