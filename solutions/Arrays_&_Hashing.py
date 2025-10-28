from typing import List
from collections import defaultdict
from time import perf_counter

from HELPER import Test

class Solution:
    def maximum(self, numbers: List[int]) -> int:
        start = perf_counter()
        
        biggest = numbers[0]

        for number in numbers:
            if number > biggest:
                biggest = number
        
        print(f"Time: {perf_counter() - start:.8f} seconds")

        return biggest
    
    def hasDuplicate(self, nums: List[int]) -> bool:
        return not(len(set(nums)) == len(nums))
    
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        map = [0] * 26
        for i in range(len(s)):
            map[ord(s[i]) - ord('a')] += 1
            map[ord(t[i]) - ord('a')] -= 1
        for m in map:
            if m != 0:
                return False
        return True
    
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map = {}

        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in map:
                return [map[diff], i]
            map[nums[i]] = i

        return None

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        lst = defaultdict(list)

        for word in strs:
            map = [0] * 26
            for c in word:
                map[ord(c) - ord('a')] += 1
            
            lst[tuple(map)].append(word)
        
        return list(lst.values())
    
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        cts = {}
        freq = [[] for _ in range(len(nums))]
        res = []

        for n in nums:
            cts[n] = 1 + cts.get(n, 0)
        for num, ct in cts.items():
            freq[ct - 1].append(num)
        for i in range(len(freq) - 1, -1, -1):
            for n in freq[i]:
                res.append(n)
                if len(res) == k:
                    return res
        return None

    class encodeDecode:
        def encode(self, strs: List[str]) -> str:
            final_str = ""
            for s in strs:
                final_str += f"{len(s)}#{s}"
            return final_str

        def decode(self, s: str) -> List[str]:
            i = 0
            res = []
            while i < len(s):
                num_str = ""
                while s[i].isdigit():
                    num_str += s[i]
                    i += 1
                i += 1
                num = int(num_str)
                word = ""
                for _ in range(num):
                    word += s[i]
                    i += 1
                res.append(word)
            return res

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1] * len(nums)
        pre, suf = nums[0], nums[-1]
        
        for i in range(1, len(nums)):
            res[i] *= pre
            pre *= nums[i]
        for i in range(len(nums)-2, -1, -1):
            res[i] *= suf
            suf *= nums[i]
        
        return res

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        for i in range(9):
            row_set, col_set, sub_set = set(), set(), set()
            for j in range(9):
                row_check = board[i][j]
                col_check = board[j][i]
                sub_check = board[(i // 3 * 3) + (j // 3)][(i % 3 * 3) + (j % 3)]
                
                if (
                    row_check in row_set or
                    col_check in col_set or
                    sub_check in sub_set
                ):
                    return False
                
                if row_check != ".":
                    row_set.add(row_check)
                if col_check != ".":
                    col_set.add(col_check)
                if sub_check != ".":
                    sub_set.add(sub_check)
        return True
    
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0
        for n in num_set:
            if n - 1 not in num_set:
                length = 0
                while n + length in num_set:
                    length += 1
                longest = max(longest, length)
        return longest
        
    def removeDuplicates(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return 1
        k = 0
        for i in range(1, len(nums)):
            if nums[k] != nums[i]:
                k += 1
            nums[k] = nums[i]
        return k+1

    def removeElement(self, nums: List[int], val: int) -> int:
        if len(nums) == 1:
            return 1 if val != nums[0] else 0
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k
    
    def getConcatenation(self, nums: List[int]) -> List[int]:
        leng = len(nums)
        ans = [0] * (leng * 2)
        for i in range(leng):
            ans[i] = nums[i]
            ans[i + leng] = nums[i]
        return ans
    
s = Solution()
t = Test()

# print(s.maximum([
#     -999999, 42, 873, 5000000, -284, 192837, 9999999, 10, 58291, -10293,
#     385, 720183, 3, 9123456, 28374, 999, 205, 3847, 700000, 1945,
#     -450, 320, 888888, 1, 938475, 583920, -50000, 1234567, 43928, 2,
#     912, 348590, 56789, 875, 3984571, 657483, 324, 745920, 4444, 27,
#     3920, 43210, 9000001, 576, 38192, 564738, 810283, 109283, 778899, 4581,
#     1290384, 9081723, 123, 598273, 384920, 1024, 839, 2048, 16384, 8192,
#     9999998, 38475, 32000, 478392, 28475, 9021834, 4000000, 5000001, 912398, 2837465,
#     918273, 987654, 321098, 7654321, 6543210, 5432109, 13579, 24680, 112233, 556677,
#     -789, 19283, 383920, 473829, 82918, 120398, 203984, 91827, 59403, 7000001,
#     857493, 2345678, 876543, 97531, 24681012, 1357911, 19283746, 37482910, 918273645, 99999999
# ]))

t.test(s. hasDuplicate , [
    (( [1,2,3,4] ), False),
    (( [1,2,3,3] ), True),
    (( [] ), False)
])

# t.test(s. isAnagram , [
#     (( "racecar", "carrace" ), True),
#     (( "hello", "billion" ), False),
#     (( "anagram", "nagaram" ), True)
# ])

# print(s. twoSum ( nums=[3,4,5,6], target=7 )) # [0,1]

# print(s. groupAnagrams ( strs=["act","pots","tops","cat","stop","hat"] )) # [["act","cat"],["pots","tops","stop"],["hat"]]

# print(s. topKFrequent ( nums=[1,2,2,3,3,3], k=2 )) # [3,2]

# ed = s.encodeDecode()
# enc = ed. encode ( strs=["neet","code","loves","you"] )
# print(enc) # "4#neet4#code4#loves3#you"
# print(ed. decode ( s=enc )) # ["neet","code","loves","you"]

# print(s. productExceptSelf ( nums=[1,2,3,4] )) # [24,12,8,6]

# board = [[".",".",".",".","5",".",".","1","."],
#          [".","4",".","3",".",".",".",".","."],
#          [".",".",".",".",".","3",".",".","1"],
#          ["8",".",".",".",".",".",".","2","."],
#          [".",".","2",".","7",".",".",".","."],
#          [".","1","5",".",".",".",".",".","."],
#          [".",".",".",".",".","2",".",".","."],
#          [".","2",".","9",".",".",".",".","."],
#          [".",".","4",".",".",".",".",".","."]]
# print(s. isValidSudoku ( board=board )) # True

# print(s. longestConsecutive ( nums=[2,20,4,10,3,4,5] )) # 4

# print(s. removeDuplicates ( nums=[1,1,2,3,4] )) # 4

# print(s. removeElement ( nums=[1,1,2,3,4], val=1 )) # 3

# print(s. getConcatenation ( nums=[1,4,1,2] )) # [1,4,1,2,1,4,1,2]
