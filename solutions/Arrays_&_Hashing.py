import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Helper import Test, ListNode
from typing import List
from collections import defaultdict

class Solution:
    # https://leetcode.com/problems/concatenation-of-array/
    def getConcatenation(self, nums: List[int]) -> List[int]:
        ans = [0] * (len(nums)*2)
        for i in range(len(nums)):
            ans[i] = nums[i]
            ans[i+len(nums)] = nums[i]
        return ans
    
    # https://leetcode.com/problems/contains-duplicate/
    def hasDuplicate(self, nums: List[int]) -> bool:
        return len(set(nums)) < len(nums)
    
    # https://leetcode.com/problems/valid-anagram/
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t): return False
        chars = [0] * 26
        for i in range(len(s)):
            chars[ord(s[i]) - ord('a')] += 1
            chars[ord(t[i]) - ord('a')] -= 1
        for c in chars:
            if c != 0:
                return False
        return True
    
    # https://leetcode.com/problems/two-sum/
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map = {}
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in map:
                return [map[diff], i]
            map[nums[i]] = i

    # https://leetcode.com/problems/longest-common-prefix/
    def longestCommonPrefix(self, strs: List[str]) -> str:
        lgst = strs[0]
        for i in range(1, len(strs)):
            word = strs[i]
            minLen = min(len(lgst), len(word))
            lgst = lgst[:minLen]
            for j in range(minLen):
                if lgst[j] != word[j]:
                    lgst = lgst[:j]
                    break
        return lgst

    # https://leetcode.com/problems/group-anagrams/
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for i in range(len(strs)):
            word = strs[i]
            cts = [0] * 26
            for j in range(len(word)):
                cts[ord(word[j]) - ord('a')] += 1
            groups[tuple(cts)].append(word)
        return list(groups.values())

    # https://leetcode.com/problems/remove-element/
    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0
        for i in range(len(nums)):
            if val != nums[i]:
                nums[k] = nums[i]
                k += 1
        return k

    # https://leetcode.com/problems/majority-element/
    def majorityElement(self, nums: List[int]) -> int:
        currLen = 0
        val = nums[0]
        for num in nums:
            if num == val:
               currLen += 1
            else:
                currLen -= 1
            if currLen == 0:
                val = num
                currLen += 1
        return val

    # https://leetcode.com/problems/design-hashset/
    class MyHashSet:
        def __init__(self):
            self.space = 10**4
            self.set = [None] * self.space

        def add(self, key: int) -> None:
            i = key % self.space
            if not self.set[i]:
                self.set[i] = ListNode(key)
                return
            
            curr = self.set[i]
            while True:
                if curr.val == key: return
                if not curr.next:
                    curr.next = ListNode(key)
                    return
                curr = curr.next

        def remove(self, key: int) -> None:
            i = key % self.space
            curr = self.set[i]
            if not curr: return
            if curr.val == key:
                self.set[i] = curr.next
                return
            while curr.next:
                if curr.next.val == key:
                    curr.next = curr.next.next
                    return
                curr = curr.next

        def contains(self, key: int) -> bool:
            i = key % self.space
            curr = self.set[i]
            while curr:
                if curr.val == key: return True
                curr = curr.next
            return False

    # https://leetcode.com/problems/design-hashmap/
    class MyHashMap:
        def __init__(self):
            self.space = 10**4
            self.set = [None] * self.space

        def put(self, key: int, value: int) -> None:
            i = key % self.space
            if not self.set[i]:
                self.set[i] = ListNode(value, key=key)
                return
            
            curr = self.set[i]
            while True:
                if curr.key == key:
                    curr.val = value
                    return
                if not curr.next:
                    curr.next = ListNode(value, key=key)
                    return
                curr = curr.next

        def get(self, key: int) -> int:
            i = key % self.space
            curr = self.set[i]
            while curr:
                if curr.key == key: return curr.val
                curr = curr.next
            return -1

        def remove(self, key: int) -> None:
            i = key % self.space
            curr = self.set[i]
            if not curr: return
            if curr.key == key:
                self.set[i] = curr.next
                return
            while curr.next:
                if curr.next.key == key:
                    curr.next = curr.next.next
                    return
                curr = curr.next

    # https://leetcode.com/problems/sort-an-array/
    def sortArray(self, nums: List[int]) -> List[int]:
        def quicksort(l, r):
            if r is None: r = len(nums)-1
            if l >= r: return
            
            p = partition(l, r)
            quicksort(l, p)
            quicksort(p+1, r)

        def partition(l, r):
            pivot = nums[(l + r) // 2]
            l -= 1
            r += 1
            while True:
                l += 1
                while nums[l] < pivot:
                    l += 1
                r -= 1
                while nums[r] > pivot:
                    r -= 1
                if l >= r:
                    return r
                nums[l], nums[r] = nums[r], nums[l]

        quicksort(0, len(nums)-1)
        return nums

    # https://leetcode.com/problems/sort-colors/
    def sortColors(self, nums: List[int]) -> None:
        freq = [0] * 3
        for n in nums:
            freq[n] += 1
        curVal = 0
        i = 0
        while i < len(nums):
            if freq[curVal] > 0:
                nums[i] = curVal
                i += 1
            freq[curVal] -= 1
            if freq[curVal] <= 0: curVal += 1
        return nums

    # https://leetcode.com/problems/top-k-frequent-elements/
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = defaultdict(int)
        for n in nums:
            freq[n] += 1
        buckets = [[] for _ in range(len(nums)+1)]
        for v, f in freq.items():
            buckets[f].append(v)
        res = []
        for i in range(len(buckets)):
            ct = buckets[-i-1]
            for j in range(len(ct)):
                res.append(ct[j])
                if len(res) == k:
                    return res

    # https://leetcode.com/problems/encode-and-decode-strings/
    class EncodeDecode:
        def encode(self, strs: List[str]) -> str:
            res = []
            for s in strs:
                res.append(f"{len(s)}#{s}")
            return "".join(res)
        
        def decode(self, s: str) -> List[str]:
            i = 0
            res = []
            while i < len(s):
                start = i
                while s[i].isdigit():
                    i += 1
                end = i
                dist = int(s[start : end])
                i += 1
                res.append(s[i : i + dist])
                i += dist
            return res
    
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

# t.test(s.getConcatenation, [
#     (( [1,2,3,4] ), [1,2,3,4,1,2,3,4] ),
#     (( [22,21,20,1] ), [22,21,20,1,22,21,20,1] ),
# ])

# t.test(s.hasDuplicate, [
#     (( [1,2,3,3] ), True ),
#     (( [1,2,3,4] ), False ),
# ])

# t.test(s.isAnagram, [
#     (( "racecar", "carrace" ), True ),
#     (( "jar", "jam" ), False ),
# ])

# t.test(s.twoSum, [
#     (( [3,4,5,6], 7 ), [0,1] ),
#     (( [4,5,6], 10 ), [0,2] ),
#     (( [5,5], 10 ), [0,1] ),
# ])

# t.test(s.longestCommonPrefix, [
#     (( ["bat","bag","bank","band"] ), "ba" ),
#     (( ["dance","dag","danger","damage"] ), "da" ),
#     (( ["neet","feet"] ), "" ),
# ])

# t.test(s.groupAnagrams, [
#     (( ["act","pots","tops","cat","stop","hat"] ), [["act","cat"],["pots","tops","stop"],["hat"]] ),
#     (( ["x"] ), [["x"]] ),
#     (( [""] ), [[""]] ),
# ])

# t.test(s.removeElement, [
#     (( [1,1,2,3,4], 1 ), len([2,3,4]) ),
#     (( [0,1,2,2,3,0,4,2], 2 ), len([0,1,3,0,4]) ),
# ])

# t.test(s.majorityElement, [
#     (( [5,5,1,1,1,5,5] ), 5 ),
#     (( [2,2,2] ), 2 ),
# ])

# t.testcls(s.MyHashSet, (  ), [
#     ("add", ( 1 ), None ),
#     ("add", ( 2 ), None ),
#     ("contains", ( 1 ), True ),
#     ("contains", ( 3 ), False ),
#     ("add", ( 2 ), None ),
#     ("contains", ( 2 ), True ),
#     ("remove", ( 2 ), None ),
#     ("contains", ( 2 ), False ),
# ])

# t.testcls(s.MyHashMap, (  ), [
#     ("put", ( 1, 1 ), None ),
#     ("put", ( 2, 2 ), None ),
#     ("get", ( 1 ), 1),
#     ("get", ( 3 ), -1),
#     ("put", ( 2, 1 ), None ),
#     ("get", ( 2 ), 1),
#     ("remove", ( 2 ), None ),
#     ("get", ( 2 ), -1 ),
# ])

# t.test(s.sortArray, [
#     (( [10,9,1,1,1,2,3,1] ), [1,1,1,1,2,3,9,10] ),
#     (( [5,10,2,1,3] ), [1,2,3,5,10] ),
# ])

# t.test(s.sortColors, [
#     (( [1,0,1,2] ), [0,1,1,2] ),
#     (( [2,1,0] ), [0,1,2] ),
# ])

# t.test(s.topKFrequent, [
#     (( [1,2,2,3,3,3], 2 ), [3,2] ),
#     (( [7,7], 1 ), [7] ),
# ])

# t.testcls(s.EncodeDecode, (  ), [
#     ("decode", ( s.EncodeDecode().encode(["neet","code","love","you"]) ), ["neet","code","love","you"] ),
#     ("decode", ( s.EncodeDecode().encode(["we","say",":","yes"]) ), ["we","say",":","yes"] ),
# ])

t.testcls(s.NumMatrix, ( [
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

# t.test(s.productExceptSelf, [
#     (( [1,2,4,6] ), [48,24,12,8] ),
#     (( [-1,0,1,2,3] ), [0,-6,0,0,0] ),
# ])

# t.test(s.isValidSudoku, [
#     (( [
#         ['1','2','.','.','3','.','.','.','.'],
#         ['4','.','.','5','.','.','.','.','.'],
#         ['.','9','8','.','.','.','.','.','3'],
#         ['5','.','.','.','6','.','.','.','4'],
#         ['.','.','.','8','.','3','.','.','5'],
#         ['7','.','.','.','2','.','.','.','6'],
#         ['.','.','.','.','.','.','2','.','.'],
#         ['.','.','.','4','1','9','.','.','8'],
#         ['.','.','.','.','8','.','.','7','9']
#     ] ), True ),
#     (( [
#         ['1','2','.','.','3','.','.','.','.'],
#         ['4','.','.','5','.','.','.','.','.'],
#         ['.','9','1','.','.','.','.','.','3'],
#         ['5','.','.','.','6','.','.','.','4'],
#         ['.','.','.','8','.','3','.','.','5'],
#         ['7','.','.','.','2','.','.','.','6'],
#         ['.','.','.','.','.','.','2','.','.'],
#         ['.','.','.','4','1','9','.','.','8'],
#         ['.','.','.','.','8','.','.','7','9']
#     ] ), False ),
# ])

# t.test(s.longestConsecutive, [
#     (( [2,20,4,10,3,4,5] ), 4 ),
#     (( [0,3,2,5,4,6,1,1] ), 7 ),
# ])

# t.test(s.maxProfit, [
#     (( [7,1,5,3,6,4] ), 7 ),
#     (( [1,2,3,4,5] ), 7 ),
# ])

# t.test(s.majorityElement2, [
#     (( [5,2,3,2,2,2,2,5,5,5] ), [2,5] ),
#     (( [4,4,4,4,4] ), [4] ),
#     (( [1,2,3] ), [] ),
# ])

# t.test(s.subarraySum, [
#     (( [2,-1,1,2], 2 ), 4 ),
#     (( [4,4,4,4,4,4], 4 ), 6 ),
# ])

# t.test(s.firstMissingPositive, [
#     (( [-2,-1,0] ), 1 ),
#     (( [1,2,4] ), 3 ),
#     (( [1,2,4,5,6,3,1] ), 7 ),
# ])
