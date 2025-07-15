from typing import List, Optional
from data_structures import ListNode, toLL, printLL

class Solution:    
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        return prev

    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        node = ListNode()
        dummy = node # dummy is the same listNode as node, just pts to its head with dummy.next
        while list1 and list2:
            if list1.val < list2.val:
                node.next = list1
                list1 = list1.next
            else:
                node.next = list2
                list2 = list2.next
            node = node.next
        node.next = list1 or list2 # appends remainder of the remaining list if needed
        return dummy.next

    class MyLinkedList:
        def __init__(self):
            self.head = None
            self.tail = None
            self.length = 0

        def get(self, index: int) -> int:
            if index < 0 or index >= self.length:
                return -1
            curr = self.head
            for _ in range(index):
                curr = curr.next
            return curr.val
            
        def addAtHead(self, val: int) -> None:
            node = ListNode(val)
            node.next = self.head
            self.head = node
            self.length += 1

        def addAtTail(self, val: int) -> None:
            pass

        def addAtIndex(self, index: int, val: int) -> None:
            pass

        def deleteAtIndex(self, index: int) -> None:
            pass

s = Solution()

# printLL ( s.reverseList ( toLL([0,1,2,3]) ))

# printLL ( s.mergeTwoLists ( toLL([1]), toLL([1,2]) ))

myLL = s.MyLinkedList()
print ( myLL.addAtHead ( 1 ) )
print ( myLL.addAtHead ( 3 ) )
print ( myLL.get ( 0 ))
