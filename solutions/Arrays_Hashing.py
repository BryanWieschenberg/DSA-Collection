from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import defaultdict
from Helper import ListNode

class Solution:
    # 1
    def getConcatenation(self, nums: List[int]) -> List[int]:
        return nums * 2
    
    # 2
    def hasDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))
            
    # 3
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t): return False
        chars = [0] * 26
        for s, t in zip(s, t):
            chars[ord(s) - ord('a')] += 1
            chars[ord(t) - ord('a')] -= 1
        for c in chars:
            if c: return False
        return True
            
    # 4
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map = {}
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in map:
                return [map[diff], i]
            map[nums[i]] = i
        return []
    
    # 5
    def longestCommonPrefix(self, strs: List[str]) -> str:
        res = strs[0]
        for i in range(len(strs)):
            j = 0
            while j < min(len(res), len(strs[i])) and res[j] == strs[i][j]:
                j += 1
            res = res[:j]
        return res
    
    # 6
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            chars = [0] * 26
            for c in s:
                chars[ord(c) - ord('a')] += 1
            res[tuple(chars)].append(s)
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
        val, freq = nums[0], 1
        for i in range(1, len(nums)):
            if val == nums[i]:
                freq += 1
            elif freq > 1 and val != nums[1]:
                freq -= 1
            elif freq == 1 and val != nums[i]:
                val = nums[i]
        return val
        
    # 9
    class MyHashSet:
        def __init__(self):
            self.set = [ListNode() for _ in range(10**4)]

        def add(self, key: int) -> None:
            curr = self.set[key % len(self.set)]
            while curr.next:
                if curr.next.val == key: return
                curr = curr.next
            curr.next = ListNode(key)

        def remove(self, key: int) -> None:
            curr = self.set[key % len(self.set)]
            while curr.next:
                if curr.next.val == key:
                    curr.next = curr.next.next
                    return
                curr = curr.next

        def contains(self, key: int) -> bool:
            curr = self.set[key % len(self.set)]
            while curr.next:
                if curr.next.val == key: return True
                curr = curr.next
            return False
    
    # 10
    class MyHashMap:
        def __init__(self):
            self.set = [ListNode() for _ in range(10**4)]

        def put(self, key: int, value: int) -> None:
            curr = self.set[key % len(self.set)]
            while curr.next:
                if curr.next.key == key:
                    curr.next.val = value
                    return
                curr = curr.next
            curr.next = ListNode(value, key=key)

        def get(self, key: int) -> int:
            curr = self.set[key % len(self.set)]
            while curr.next:
                if curr.next.key == key: return curr.next.val
                curr = curr.next
            return -1

        def remove(self, key: int) -> None:
            curr = self.set[key % len(self.set)]
            while curr.next:
                if curr.next.key == key:
                    curr.next = curr.next.next
                    return
                curr = curr.next
    
    # 11
    def sortArray(self, nums: List[int]) -> List[int]:
        def partition(l, r, pivot):
            i, j = l, r
            while i <= j:
                while nums[i] < pivot: i += 1
                while nums[j] > pivot: j -= 1
                if i <= j:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
                    j -= 1
            return i, j

        def quicksort(l, r):
            if l >= r: return
            pivot = nums[(l + r) // 2]
            i, j = partition(l, r, pivot)
            quicksort(l, j)
            quicksort(i, r)
        
        quicksort(0, len(nums)-1)
        return nums
        
    # 12
    def sortColors(self, nums: List[int]) -> List[int]:
        freq = [0] * 3
        for n in nums:
            freq[n] += 1
        idx = 0
        for i in range(len(freq)):
            while freq[i]:
                nums[idx] = i
                freq[i] -= 1
                idx += 1
        return nums
    
    # 13
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = defaultdict(int)
        for n in nums:
            freq[n] += 1

        cts = [[] for _ in range(len(nums)+1)]
        for n in freq:
            cts[freq[n]].append(n)

        res = []
        for i in range(len(cts)):
            for j in range(len(cts[-i-1])):
                res.append(cts[-i-1][j])
                if len(res) == k:
                    return res
        return []
        
    # 14
    class EncodeDecode:
        def encode(self, strs: List[str]) -> str:
            res = []
            for s in strs:
                res.append(f"{len(s)}#{s}")
            return "".join(res)

        def decode(self, s: str) -> List[str]:
            res = []
            i = 0
            while i < len(s):
                length = ""
                while s[i].isdigit():
                    length += s[i]
                    i += 1
                length = int(length)
                i += 1
                res.append(s[i:i+length])
                i += length
            return res
        
    # 15
    class NumMatrix:
        def __init__(self, matrix: List[List[int]]):
            ROWS, COLS = len(matrix)+1, len(matrix[0])+1
            self.sums = [[0] * COLS for _ in range(ROWS)]
            for r in range(1, ROWS):
                for c in range(1, COLS):
                    self.sums[r][c] = (
                        matrix[r-1][c-1] +
                        self.sums[r-1][c] +
                        self.sums[r][c-1] -
                        self.sums[r-1][c-1]
                    )
        
        def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
            return (
                self.sums[row2+1][col2+1] -
                self.sums[row1][col2+1] -
                self.sums[row2+1][col1] +
                self.sums[row1][col1]
            )
    
    # 16
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [1] * n
        pre, post = 1, 1
        for i in range(1, n):
            pre *= nums[i-1]
            res[i] = pre
        for i in range(1, n):
            post *= nums[-i]
            res[-i-1] *= post
        return res
        
    # 17
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        for r in range(len(board)):
            rows, cols, subs = set(), set(), set()
            for c in range(len(board[0])):
                row = board[r][c]
                col = board[c][r]
                sub = board[(r // 3 * 3) + (c // 3)][(r % 3 * 3) + (c % 3)]
                if (
                    (row != '.' and row in rows) or
                    (col != '.' and col in cols) or
                    (sub != '.' and sub in subs)
                ):
                    return False
                rows.add(row)
                cols.add(col)
                subs.add(sub)
        return True
    
    # 18
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums: return 0
        nums = set(nums)
        lgst = 1
        for n in nums:
            if n-1 not in nums:
                i = n
                while i in nums:
                    i += 1
                lgst = max(lgst, i-n)
        return lgst
        
    # 19
    def maxProfit(self, prices: List[int]) -> int:
        res = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                res += prices[i] - prices[i-1]
        return res
        
    # 20
    def majorityElement2(self, nums: List[int]) -> int:
        val1 = val2 = None
        freq1 = freq2 = 0

        for n in nums:
            if n == val1:
                freq1 += 1
            elif n == val2:
                freq2 += 1
            elif freq1 == 0:
                val1, freq1 = n, 1
            elif freq2 == 0:
                val2, freq2 = n, 1
            else:
                freq1 -= 1
                freq2 -= 1

        res = []
        n = len(nums)

        if nums.count(val1) > n // 3:
            res.append(val1)
        if val1 != val2 and nums.count(val2) > n // 3:
            res.append(val2)

        return res
        
    # 21
    def subarraySum(self, nums: List[int], k: int) -> int:
        freq = defaultdict(int)
        freq[0] += 1
        curr = 0
        ans = 0

        for n in nums:
            curr += n
            ans += freq[curr - k]
            freq[curr] += 1
        return ans
        
    # 22
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        i = 0
        while i < n:
            correctPos = nums[i] - 1
            if 0 < nums[i] <= n and nums[i] != nums[correctPos]:
                nums[i], nums[correctPos] = nums[correctPos], nums[i]
            else:
                i += 1
        
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        
        return n + 1
        
if __name__ == "__main__":
    s = Solution()
