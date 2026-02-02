from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List, Optional
from Helper import ListNode, ListHelper

class Solution:
    # 73
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr, prev = head, None
        while curr:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        return prev
        
    # 74
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = curr = ListNode()
        l1, l2 = list1, list2
        while l1 and l2:
            if l1.val <= l2.val:
                curr.next = l1
                l1 = l1.next
            else:
                curr.next = l2
                l2 = l2.next
            curr = curr.next
        curr.next = l1 or l2
        return dummy.next
        
    # 75
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
            
    # 76
    def reorderList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        curr, prev = slow.next, None
        slow.next = None
        while curr:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        curr = head
        tmp1, tmp2 = curr, prev
        while tmp2:
            tmp1 = tmp1.next
            curr.next = tmp2
            tmp2 = tmp2.next
            curr.next.next = tmp1
            curr = curr.next.next
        return head

    # 77
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        curr = head
        length = 0
        while curr:
            curr = curr.next
            length += 1
        if n == length:
            return head.next
        curr = head
        for i in range(length - n - 1):
            curr = curr.next
        curr.next = curr.next.next
        return head
        
    # 78
    def copyRandomList(self, head: 'Optional[ListNode]') -> 'Optional[ListNode]':
        pass

    # 79
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        pass
        
    # 80
    def findDuplicate(self, nums: List[int]) -> int:
        pass
    
    # 81
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        pass

    # 82
    class MyCircularQueue:
        def __init__(self, k: int):
            pass

        def enQueue(self, value: int) -> bool:
            pass

        def deQueue(self) -> bool:
            pass

        def Front(self) -> int:
            pass

        def Rear(self) -> int:
            pass

        def isEmpty(self) -> bool:
            pass

        def isFull(self) -> bool:
            pass

    # 83
    class LRUCache:
        def __init__(self, capacity: int):
            pass

        def get(self, key: int) -> int:
            pass

        def put(self, key: int, value: int) -> None:
            pass

    # 84
    class LFUCache:
        def __init__(self, capacity: int):
            pass

        def get(self, key: int) -> int:
            pass

        def put(self, key: int, value: int) -> None:
            pass

    # 85
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists: return None
        dummy = l1 = ListNode(next=lists[0])
        for l2 in lists[1:]:
            curr, l1 = dummy, dummy.next
            while l1 and l2:
                if l1.val <= l2.val:
                    curr.next = l1
                    l1 = l1.next
                else:
                    curr.next = l2
                    l2 = l2.next
                curr = curr.next
            curr.next = l1 or l2
        return dummy.next
    
    # 86
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        pass

if __name__ == "__main__":
    s = Solution(); hl = ListHelper()
