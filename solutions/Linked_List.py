from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List, Optional
from Helper import ListNode, ListHelper

class Solution:
    # 73
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pass
    
    # 74
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        pass
    
    # 75
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        pass
        
    # 76
    def reorderList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pass
    
    # 77
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        pass
    
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
        pass

    # 86
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        pass

if __name__ == "__main__":
    s = Solution(); hl = ListHelper()
