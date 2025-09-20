from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev

class Helper:
    def printLL(self, head: Optional[ListNode], end="\n"):
        curr = head
        while curr:
            print(f"{curr.val}", end=" -> " if curr.next else end)
            curr = curr.next
    
    def toLL(self, values: List, cycle_index: Optional[int] = None) -> Optional[ListNode]:
        if not values:
            return None
        nodes = [ListNode(val=v) for v in values]
        for i in range(len(nodes)-1):
            nodes[i].next = nodes[i+1]
        if cycle_index is not None and 0 <= cycle_index < len(nodes):
            nodes[-1].next = nodes[cycle_index]
        return nodes[0]

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr, prev = head, None
        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        return prev

    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = node = ListNode()
        
        while list1 and list2:
            if list1.val <= list2.val:
                node.next = list1
                list1 = list1.next
            else:
                node.next = list2
                list2 = list2.next
            node = node.next

        node.next = list1 or list2

        return dummy.next
    
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
    
    def reorderList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        curr, slow.next, prev = slow.next, None, None
        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        
        first, second = head, prev
        while second:
            temp1, temp2 = first.next, second.next
            first.next = second
            second.next = temp1
            first, second = temp1, temp2
        return head

    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        left = dummy
        right = head

        while n > 0:
            right = right.next
            n -= 1
        
        while right:
            left = left.next
            right = right.next

        left.next = left.next.next
        return dummy.next
    
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        curr1, curr2 = l1, l2
        OoM = 0
        totalSum = 0
        while curr1 or curr2:
            if curr1:
                totalSum += curr1.val * (10**OoM)
                curr1 = curr1.next
            if curr2:
                totalSum += curr2.val * (10**OoM)
                curr2 = curr2.next
            OoM += 1
        dummy = node = ListNode()
        totalSum = str(totalSum)
        
        for i in range(len(totalSum)-1, -1, -1):
            node.next = ListNode(val=int(totalSum[i]))
            node = node.next

        return dummy.next
    
s = Solution()
h = Helper()

# h.printLL( s. reverseList ( list1=h.toLL([1,2,3,4,5]) )) # 5 -> 4 -> 3 -> 2 -> 1

# h.printLL( s. mergeTwoLists ( list1=h.toLL([1,2,4]), list2=h.toLL([1,3,5]) )) # 1 -> 1 -> 2 -> 3 -> 4 -> 5

# print( s. hasCycle ( head=h.toLL([1,2,3,4], 1) )) # True

# h.printLL( s. reorderList ( head=h.toLL([2,4,6,8,10]) )) # 2 -> 10 -> 4 -> 8 -> 6

# h.printLL( s. removeNthFromEnd ( head=h.toLL([1,2,3,4]), n=2 )) # 1 -> 2 -> 4

h.printLL( s. addTwoNumbers ( l1=h.toLL([1,2,3]), l2=h.toLL([4,5,6]) )) # 5 -> 7 -> 9
