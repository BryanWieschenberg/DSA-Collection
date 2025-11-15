import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Helper import Test
from typing import List

class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        pass

    def hasDuplicate(self, nums: List[int]) -> bool:
        pass
    
    def isAnagram(self, s: str, t: str) -> bool:
        pass

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pass

    def longestCommonPrefix(self, strs: List[str]) -> str:
        pass

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        pass

    def removeElement(self, nums: List[int], val: int) -> int:
        pass

    def majorityElement(self, nums: List[int]) -> int:
        pass

    class MyHashSet:
        def __init__(self):
            pass

        def add(self, key: int) -> None:
            pass

        def remove(self, key: int) -> None:
            pass

        def contains(self, key: int) -> bool:
            pass

        def getMask(self, key: int) -> int:
            pass

    class MyHashMap:
        def __init__(self):
            pass 

        def put(self, key: int, value: int) -> None:
            pass

        def get(self, key: int) -> int:
            pass

        def remove(self, key: int) -> None:
            pass

    def sortArray(self, nums: List[int]) -> List[int]:
        pass

    def sortColors(self, nums: List[int]) -> None:
        pass

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        pass

    class EncodeDecode:
        def encode(self, strs: List[str]) -> str:
            pass

        def decode(self, s: str) -> List[str]:
            pass

    class NumMatrix:
        def __init__(self, matrix: List[List[int]]):
            pass

        def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
            pass

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        pass

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        pass
    
    def longestConsecutive(self, nums: List[int]) -> int:
        pass

    def maxProfit(self, prices: List[int]) -> int:
        pass

    def majorityElement2(self, nums: List[int]) -> int:
        pass

    def subarraySum(self, nums: List[int], k: int) -> int:
        pass

    def firstMissingPositive(self, nums: List[int]) -> int:
        pass
        
s = Solution()
t = Test()

t.test(s.getConcatenation, [
    (( [1,2,3,4] ), [1,2,3,4,1,2,3,4] ),
    (( [22,21,20,1] ), [22,21,20,1,22,21,20,1] ),
])

t.test(s.hasDuplicate, [
    (( [1,2,3,3] ), True ),
    (( [1,2,3,4] ), False ),
])

t.test(s.isAnagram, [
    (( "racecar", "carrace" ), True ),
    (( "jar", "jam" ), False ),
])

t.test(s.twoSum, [
    (( [3,4,5,6], 7 ), [0,1] ),
    (( [4,5,6], 10 ), [0,2] ),
    (( [5,5], 10 ), [0,1] ),
])

t.test(s.longestCommonPrefix, [
    (( ["bat","bag","bank","band"] ), "ba" ),
    (( ["dance","dag","danger","damage"] ), "da" ),
    (( ["neet","feet"] ), "" ),
])

t.test(s.groupAnagrams, [
    (( ["act","pots","tops","cat","stop","hat"] ), [["hat"],["act","cat"],["stop","pots","tops"]] ),
    (( ["x"] ), [["x"]] ),
    (( [""] ), [[""]] ),
])

t.test(s.removeElement, [
    (( [1,1,2,3,4], 1 ), [2,3,4] ),
    (( [0,1,2,2,3,0,4,2], 2 ), [0,1,3,0,4] ),
])

t.test(s.majorityElement, [
    (( [5,5,1,1,1,5,5] ), 5 ),
    (( [2,2,2] ), 2 ),
])

t.test_class(s.MyHashSet, (  ), [
    ("add", ( 1 ), [1] ),
    ("add", ( 2 ), [1,2] ),
    ("contains", ( 1 ), True ),
    ("contains", ( 3 ), False ),
    ("add", ( 2 ), [1,2] ),
    ("contains", ( 2 ), True ),
    ("remove", ( 2 ), [1] ),
    ("contains", ( 2 ), False ),
])

t.test_class(s.MyHashMap, (  ), [
    ("put", ( 1, 1 ), [[1,1]] ),
    ("put", ( 2, 2 ), [[1,1],[2,2]] ),
    ("get", ( 1 ), 1),
    ("get", ( 3 ), -1),
    ("put", ( 2, 1 ), [[1,1],[2,1]] ),
    ("get", ( 2 ), 1),
    ("remove", ( 2 ), [[1,1]] ),
    ("get", ( 2 ), -1 ),
])

t.test(s.sortArray, [
    (( [10,9,1,1,1,2,3,1] ), [1,1,1,1,2,3,9,10] ),
    (( [5,10,2,1,3] ), [1,2,3,5,10] ),
])

t.test(s.sortColors, [
    (( [1,0,1,2] ), [0,1,1,2] ),
    (( [2,1,0] ), [0,1,2] ),
])

t.test(s.topKFrequent, [
    (( [1,2,2,3,3,3], 2 ), [2,3] ),
    (( [7,7], 1 ), [7] ),
])

encode1 = s.EncodeDecode.encode( ["neet","code","love","you"] )
encode2 = s.EncodeDecode.encode( ["we","say",":","yes"] )
t.test_class(s.EncodeDecode, (  ), [
    ("decode", ( encode1 ), ["neet","code","love","you"] ),
    ("decode", ( encode2 ), ["we","say",":","yes"] ),
])

t.test_class(s.NumMatrix, ( [
    [3,0,1,4,2],
    [5,6,3,2,1],
    [1,2,0,1,5],
    [4,1,0,1,7],
    [1,0,3,0,5]
] ), [
    ("sumRegion", ( 2, 1, 4, 3 ), 8 ),
    ("sumRegion", ( 1, 1, 2, 2 ), 11 ),
    ("sumRegion", ( 1, 2, 2, 4 ), 12 ),
])

t.test(s.productExceptSelf, [
    (( [1,2,4,6] ), [48,24,12,8] ),
    (( [-1,0,1,2,3] ), [0,-6,0,0,0] ),
])

t.test(s.isValidSudoku, [
    (( [
        ['1','2','.','.','3','.','.','.','.'],
        ['4','.','.','5','.','.','.','.','.'],
        ['.','9','8','.','.','.','.','.','3'],
        ['5','.','.','.','6','.','.','.','4'],
        ['.','.','.','8','.','3','.','.','5'],
        ['7','.','.','.','2','.','.','.','6'],
        ['.','.','.','.','.','.','2','.','.'],
        ['.','.','.','4','1','9','.','.','8'],
        ['.','.','.','.','8','.','.','7','9']
    ] ), True ),
    (( [
        ['1','2','.','.','3','.','.','.','.'],
        ['4','.','.','5','.','.','.','.','.'],
        ['.','9','1','.','.','.','.','.','3'],
        ['5','.','.','.','6','.','.','.','4'],
        ['.','.','.','8','.','3','.','.','5'],
        ['7','.','.','.','2','.','.','.','6'],
        ['.','.','.','.','.','.','2','.','.'],
        ['.','.','.','4','1','9','.','.','8'],
        ['.','.','.','.','8','.','.','7','9']
    ] ), False ),
])

t.test(s.longestConsecutive, [
    (( [2,20,4,10,3,4,5] ), 4 ),
    (( [0,3,2,5,4,6,1,1] ), 7 ),
])

t.test(s.maxProfit, [
    (( [7,1,5,3,6,4] ), 7 ),
    (( [1,2,3,4,5] ), 7 ),
])

t.test(s.majorityElement2, [
    (( [5,2,3,2,2,2,2,5,5,5] ), [2,5] ),
    (( [4,4,4,4,4] ), [4] ),
    (( [1,2,3] ), [] ),
])

t.test(s.subarraySum, [
    (( [2,-1,1,2], 2 ), 4 ),
    (( [4,4,4,4,4,4], 4 ), 6 ),
])

t.test(s.firstMissingPositive, [
    (( [-2,-1,0] ), 1 ),
    (( [1,2,4] ), 3 ),
    (( [1,2,4,5,6,3,1] ), 7 ),
])
