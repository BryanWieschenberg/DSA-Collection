from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import defaultdict, Counter
from Helper import ListNode, ListHelper

class Solution:
    # 1
    def getConcatenation(self, nums: List[int]) -> List[int]:
        return nums * 2

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
        res = strs[0]
        for s in strs:
            res = res[:len(s)]
            for i in range(min(len(res), len(s))):
                if res[i] != s[i]:
                    res = res[:i]
                    break
        return res
        
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
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k
            
    # 8
    def majorityElement(self, nums: List[int]) -> int:
        curr, val = 0, nums[0]
        for n in nums:
            if val == n:
                curr += 1
            elif val != n:
                curr -= 1
            if curr == 0:
                curr = 1
                val = n
        return val
            
    # 9
    class MyHashSet:
        def __init__(self):
            self.space = [ListNode()] * 10**4

        def add(self, key: int) -> None:
            keyc = key % len(self.space)
            curr = self.space[keyc]
            while curr.next:
                if curr.next.key == key:
                    return
                curr = curr.next
            curr.next = ListNode(key=key)

        def remove(self, key: int) -> None:
            keyc = key % len(self.space)
            curr = self.space[keyc]
            while curr.next:
                if curr.next.key == key:
                    curr.next = curr.next.next
                    return
                curr = curr.next

        def contains(self, key: int) -> bool:
            keyc = key % len(self.space)
            curr = self.space[keyc]
            while curr.next:
                if curr.next.key == key:
                    return True
                curr = curr.next
            return False
        
    # 10
    class MyHashMap:
        def __init__(self):
            self.space = [ListNode()] * 10**4

        def put(self, key: int, value: int) -> None:
            keyc = key % len(self.space)
            curr = self.space[keyc]
            while curr.next:
                if curr.next.key == key:
                    curr.next.val = value
                    return
                curr = curr.next
            curr.next = ListNode(val=value, key=key)

        def get(self, key: int) -> int:
            keyc = key % len(self.space)
            curr = self.space[keyc]
            while curr.next:
                if curr.next.key == key:
                    return curr.next.val
                curr = curr.next
            return -1

        def remove(self, key: int) -> None:
            keyc = key % len(self.space)
            curr = self.space[keyc]
            while curr.next:
                if curr.next.key == key:
                    curr.next = curr.next.next
                    return
                curr = curr.next
    
    # 11
    def sortArray(self, nums: List[int]) -> List[int]:
        def partition(l, r):
            pivot = nums[l + (r - l) // 2]
            while l <= r:
                while nums[l] < pivot: l += 1
                while nums[r] > pivot: r -= 1
                if l <= r:
                    nums[l], nums[r] = nums[r], nums[l]
                    l += 1
                    r -= 1
            return l, r

        def quicksort(l, r):
            if l >= r:
                return []
            i, j = partition(l, r)
            quicksort(l, j)
            quicksort(i, r)

        quicksort(0, len(nums)-1)
        return nums
    
    # 12
    def sortColors(self, nums: List[int]) -> List[int]:
        freq = defaultdict(int) # could also use Counter()
        for n in nums:
            freq[n] += 1
        idx = 0
        for i in range(3):
            while freq[i] > 0:
                nums[idx] = i
                idx += 1
                freq[i] -= 1
        return nums
    
    # 13
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        ct = [[] for _ in range(len(nums)+1)]
        for v in freq:
            ct[freq[v]].append(v)
        res = []
        for i in range(len(ct)-1, -1, -1):
            for j in range(len(ct[i])):
                res.append(ct[i][j])
                if len(res) == k:
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
            R, C = len(matrix), len(matrix[0])
            self.sums = [[0] * (C+1) for _ in range(R+1)]
            for r in range(1, R+1):
                for c in range(1, C+1):
                    self.sums[r][c] = (
                        matrix[r-1][c-1] +
                        self.sums[r-1][c] +
                        self.sums[r][c-1] -
                        self.sums[r-1][c-1]
                    )

        def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
            row1, col1, row2, col2 = row1+1, col1+1, row2+1, col2+1
            return (
                self.sums[row2][col2] -
                self.sums[row1-1][col2] -
                self.sums[row2][col1-1] +
                self.sums[row1-1][col1-1]
            )
    
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
        res, buy = 0, prices[0]
        for p in prices:
            if p > buy:
                res += p - buy
            buy = p
        return res
            
    # 20
    def majorityElement2(self, nums: List[int]) -> int:
        curr1, val1, curr2, val2 = 0, nums[0], 0, 0
        for n in nums:
            if val1 == n:
                curr1 += 1
            elif val2 == n:
                curr2 += 1
            elif curr1 == 0:
                curr1 = 1
                val1 = n
            elif curr2 == 0:
                curr2 = 1
                val2 = n
            else:
                curr1 -= 1
                curr2 -= 1
        res = []
        if nums.count(val1) > len(nums) // 3:
            res.append(val1)
        if nums.count(val2) > len(nums) // 3:
            res.append(val2)        
        return res
            
    # 21
    def subarraySum(self, nums: List[int], k: int) -> int:
        mp = defaultdict(int)
        mp[0] = 1
        res = curr = 0
        for n in nums:
            curr += n
            res += mp[curr - k]
            mp[curr] += 1
        return res
            
    # 22
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        i = 0
        while i < n:
            correct = nums[i] - 1
            if 0 < nums[i] <= n and nums[i] != nums[correct]:
                nums[i], nums[correct] = nums[correct], nums[i]
            else:
                i += 1
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
            
if __name__ == "__main__":
    s = Solution()
