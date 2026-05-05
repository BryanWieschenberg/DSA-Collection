from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(ospath.dirname(__file__))))
from typing import List
from collections import defaultdict, Counter
from Helper import ListNode, ListHelper, RNG

global_rng = RNG(id(object()))


class Solution:
    # 1
    def getConcatenation(self, nums: List[int]) -> List[int]:
        return nums * 2

    # 2
    class DynamicArray:
        def __init__(self, capacity: int):
            self.cap = capacity
            self.size = 0
            self.arr = [-1] * self.cap

        def get(self, i: int) -> int:
            return self.arr[i]

        def set(self, i: int, n: int) -> None:
            self.arr[i] = n

        def pushback(self, n: int) -> None:
            if self.getSize() == self.getCapacity():
                self.resize()
            self.arr[self.size] = n
            self.size += 1

        def popback(self) -> int:
            val = self.arr[self.size-1]
            self.arr[self.size-1] = -1
            self.size -= 1
            return val

        def resize(self) -> None:
            self.cap *= 2
            new = [-1] * self.cap
            for i in range(self.cap // 2):
                new[i] = self.arr[i]
            self.arr = new

        def getSize(self) -> int:
            return self.size
        
        def getCapacity(self) -> int:
            return self.cap

    # 3
    def hasDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))

    # 4
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        res = curr = 0
        for n in nums:
            if n:
                curr += 1
            else:
                curr = 0
            res = max(res, curr)
        return res

    # 5
    def replaceElements(self, arr: List[int]) -> List[int]:
        maxVal = -1
        for i in range(len(arr)-1, -1, -1):
            prev = maxVal
            maxVal = max(maxVal, arr[i])
            arr[i] = prev
        return arr

    # 6
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
    
    # 7
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        mp = {}
        for i, n in enumerate(nums):
            diff = target - n
            if diff in mp:
                return [mp[diff], i]
            mp[n] = i
        return []
        
    # 8
    def longestCommonPrefix(self, strs: List[str]) -> str:
        res = strs[0]
        for s in strs:
            res = res[:len(s)]
            for i in range(min(len(res), len(s))):
                if res[i] != s[i]:
                    res = res[:i]
                    break
        return res
        
    # 9
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            ct = [0] * 26
            for c in s:
                ct[ord(c) - ord('a')] += 1
            res[tuple(ct)].append(s)
        return list(res.values())
            
    # 10
    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k
            
    # 11
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
            
    # 12
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
        
    # 13
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
    
    # 14
    class MySortingAlgorithms:
        def bogo_sort(self, nums: List[int]) -> List[int]:
            def isSorted(nums):
                for i in range(1, len(nums)):
                    if nums[i-1] > nums[i]:
                        return False
                return True

            def shuffle(nums):
                for i in range(len(nums)-1, 0, -1):
                    j = global_rng.randint(0, i)
                    nums[i], nums[j] = nums[j], nums[i]

            while True:
                if isSorted(nums):
                    return nums
                shuffle(nums)

        def bubble_sort(self, nums: List[int]) -> List[int]:
            n = len(nums)
            for i in range(n):
                for j in range(0, n-i-1):
                    if nums[j] > nums[j+1]:
                        nums[j], nums[j+1] = nums[j+1], nums[j]
            return nums

        def selection_sort(self, nums: List[int]) -> List[int]:
            n = len(nums)
            for i in range(n):
                minVal = nums[i]
                minPos = i
                for j in range(i+1, n):
                    if nums[j] < minVal:
                        minVal = nums[j]
                        minPos = j
                nums[i], nums[minPos] = nums[minPos], nums[i]
            return nums

        def insertion_sort(self, nums: List[int]) -> List[int]:
            n = len(nums)
            for i in range(1, n):
                key = nums[i]
                j = i-1
                while j >= 0 and nums[j] > key:
                    nums[j+1] = nums[j]
                    j -= 1
                nums[j+1] = key
            return nums

        def merge_sort(self, nums: List[int]) -> List[int]:
            def combine(l, m, r):
                for k in range(l, r+1):
                    aux[k] = nums[k]
                i, j = l, m+1
                for k in range(l, r+1):
                    if i > m:
                        nums[k] = aux[j]
                        j += 1
                    elif j > r:
                        nums[k] = aux[i]
                        i += 1
                    elif aux[j] < aux[i]:
                        nums[k] = aux[j]
                        j += 1
                    else:
                        nums[k] = aux[i]
                        i += 1

            def merge(l, r):
                if l < r:
                    m = l + (r - l) // 2
                    merge(l, m)
                    merge(m+1, r)
                    combine(l, m, r)

            aux = [0] * len(nums)
            merge(0, len(nums)-1)
            return nums

        def quick_sort(self, nums: List[int]) -> List[int]:
            def partition(l, r):
                pivot = nums[r]
                i = l-1
                for j in range(l, r):
                    if nums[j] <= pivot:
                        i += 1
                        nums[i], nums[j] = nums[j], nums[i]
                nums[i+1], nums[r] = nums[r], nums[i+1]
                return i+1

            def quicksort(l, r):
                if l < r:
                    random_idx = global_rng.randint(l, r)
                    nums[random_idx], nums[r] = nums[r], nums[random_idx]
                    pivot_idx = partition(l, r)
                    quicksort(l, pivot_idx-1)
                    quicksort(pivot_idx+1, r)

            quicksort(0, len(nums)-1)
            return nums

        def heap_sort(self, nums: List[int]) -> List[int]:
            def sift_down(n, i):
                largest = i
                l = i*2 + 1
                r = i*2 + 2
                if l < n and nums[l] > nums[largest]:
                    largest = l
                if r < n and nums[r] > nums[largest]:
                    largest = r
                if largest != i:
                    nums[i], nums[largest] = nums[largest], nums[i]
                    sift_down(n, largest)

            n = len(nums)
            for i in range(n // 2 - 1, -1, -1):
                sift_down(n, i)
            for i in range(n-1, 0, -1):
                nums[i], nums[0] = nums[0], nums[i]
                sift_down(i, 0)
            return nums

        def counting_sort(self, nums: List[int]) -> List[int]:
            smallest, largest = min(nums), max(nums)
            cts = [0] * (largest - smallest + 1)
            res = [0] * len(nums)
            for n in nums:
                cts[n - smallest] += 1
            for i in range(1, len(cts)):
                cts[i] += cts[i-1]
            for i in range(len(nums)-1, -1, -1):
                val = nums[i]
                pos = cts[val - smallest] - 1
                res[pos] = val
                cts[val - smallest] -= 1
            return res

        def bucket_sort(self, nums: List[int], bucket_ct: int = 5) -> List[int]:
            smallest, largest = min(nums), max(nums)
            if smallest == largest:
                return nums
            buckets = [[] for _ in range(bucket_ct)]
            for n in nums:
                i = int((n - smallest) / (largest - smallest) * (bucket_ct))
                if i == bucket_ct:
                    i -= 1
                buckets[i].append(n)
            nums.clear()
            for bucket in buckets:
                self.insertion_sort(bucket)
                nums.extend(bucket)
            return nums

        def radix_sort(self, nums: List[int]) -> List[int]:
            def counting_sort_for_radix(exp):
                n = len(nums)
                cts = [0] * 10
                res = [0] * n
                for i in range(n):
                    idx = (nums[i] // exp) % 10
                    cts[idx] += 1
                for i in range(1, 10):
                    cts[i] += cts[i-1]
                for i in range(n-1, -1, -1):
                    idx = (nums[i] // exp) % 10
                    pos = cts[idx] - 1
                    res[pos] = nums[i]
                    cts[idx] -= 1
                for i in range(n):
                    nums[i] = res[i]

            largest = max(nums)
            exp = 1
            while largest // exp > 0:
                counting_sort_for_radix(exp)
                exp *= 10
            return nums

    # 15
    def sortColors(self, nums: List[int]) -> List[int]:
        freq = defaultdict(int)
        for n in nums:
            freq[n] += 1
        idx = 0
        for i in range(3):
            while freq[i] > 0:
                nums[idx] = i
                idx += 1
                freq[i] -= 1
        return nums
    
    # 16
    def pivotIndex(self, nums: List[int]) -> int:
        lSum = 0
        total = sum(nums)
        for i in range(len(nums)):
            rSum = total - nums[i] - lSum
            if lSum == rSum:
                return i
            lSum += nums[i]
        return -1

    # 17
    def countStudents(self, students: List[int], sandwiches: List[int]) -> int:
        res = len(students)
        cts = Counter(students)
        for s in sandwiches:
            if cts[s] > 0:
                res -= 1
                cts[s] -= 1
            else:
                break
        return res
        
    # 18
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
            
    # 19
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

    # 20
    class NumArray:
        def __init__(self, nums: List[int]):
            self.sums = [0] * (len(nums)+1)
            for i in range(len(nums)):
                self.sums[i+1] = self.sums[i] + nums[i]

        def sumRange(self, left: int, right: int) -> int:
            return self.nums[right+1] - self.nums[left]

    # 21
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
    
    # 22
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
            
    # 23
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
        
    # 24
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
            
    # 25
    def maxProfit(self, prices: List[int]) -> int:
        res, buy = 0, prices[0]
        for p in prices:
            if p > buy:
                res += p - buy
            buy = p
        return res
            
    # 26
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
            
    # 27
    def subarraySum(self, nums: List[int], k: int) -> int:
        mp = defaultdict(int)
        mp[0] = 1
        res = curr = 0
        for n in nums:
            curr += n
            res += mp[curr - k]
            mp[curr] += 1
        return res
            
    # 28
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
            
    # 29
    def shortestPalindrome(self, s: str) -> str:
        pass

    # 30
    def longestDupSubstring(self, s: str) -> str:
        pass


if __name__ == "__main__":
    s = Solution()
