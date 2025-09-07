from typing import List
from collections import defaultdict

class Solution:
    # https://neetcode.io/problems/duplicate-integer?list=neetcode150
    # Time: O(n)
    # Space: O(n)
    def hasDuplicate(self, nums: List[int]) -> bool:
        return not(len(set(nums)) == len(nums))
    
    # https://neetcode.io/problems/is-anagram?list=neetcode150
    # Time: O(n)
    # Space: O(1)
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
    
    # https://neetcode.io/problems/two-sum?list=neetcode150
    # Time: O(n)
    # Space: O(n)
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map = {}

        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in map:
                return [map[diff], i]
            map[nums[i]] = i

        return None

    # https://neetcode.io/problems/group-anagrams?list=neetcode150
    # Time: O(n * m), n = number of words, m = length of longest word
    # Space: O(n * m)
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        lst = defaultdict(list)

        for word in strs:
            map = [0] * 26

            for c in word:
                map[ord(c) - ord('a')] += 1
            
            lst[tuple(map)].append(word)
        
        return list(lst.values())
    
    # https://neetcode.io/problems/top-k-frequent-elements?list=neetcode150
    # Time: TODO:
    # Space: TODO:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        cts = {}
        freq = []
        for n in nums:
            cts[n] += cts.get(n, 0)

s = Solution()

# print(s. hasDuplicate ( nums=[1,2,3,3] ))

# print(s. isAnagram ( s="racecar", t="carrace" ))

# print(s. twoSum ( nums=[3,4,5,6], target=7 ))

# print(s. groupAnagrams ( strs=["act","pots","tops","cat","stop","hat"] ))

print(s. topKFrequent ( nums=[1,2,2,3,3,3], k=2 ))
