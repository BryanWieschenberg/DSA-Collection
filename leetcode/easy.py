import inspect
import sys
from utils import p, e

from typing import List, Optional
from data_structures import ListNode, toLL, printLL

class Solution:
    # https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/description/
    # Time : O(n)
    # Space: O(n)
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        curr = head
        arr = []
        while curr:
            arr.append(curr.val)
            curr = curr.next

        sum = 0
        for i in range(len(arr)):
            if arr[i]:
                sum += 2**(len(arr)-1-i)    
        return sum

    # https://leetcode.com/problems/valid-word/description/
    def isValid(self, word: str) -> bool:
        if len(word) < 3:
            return False
        
        has_vowel = has_consonant = 0

        for w in word:
            if not w.isalnum():
                return False
            if w.lower() in "aeiou":
                has_vowel += 1
            elif w.isalpha():
                has_consonant += 1
        return True if has_vowel and has_consonant else False

s = Solution()

# print(s.getDecimalValue ( toLL([1,0,1]) ))

print(s.isValid ( "AhI" ))
