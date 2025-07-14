from typing import List, Optional
from data_structures import ListNode, toLL, printLL

class Solution:
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

s = Solution()

print(s.getDecimalValue ( toLL([1,0,1]) ))
