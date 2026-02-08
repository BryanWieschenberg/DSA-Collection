from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List, Optional
from Helper import ListNode, ListHelper
from heapq import *

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
        curr, tmp2 = head, prev
        while prev:
            tmp2 = tmp2.next
            tmp1 = curr.next
            curr.next = prev
            curr.next.next = tmp1
            curr = curr.next.next
            prev = tmp2
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
        if not head:
            return None
        new = {}
        curr = head
        while curr:
            new[curr] = ListNode(curr.val)
            curr = curr.next
        curr = head
        while curr:
            copy = new[curr]
            copy.next = new.get(curr.next)
            copy.random = new.get(curr.random)
            curr = curr.next
        return new[head]

    # 79
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = curr = ListNode()
        carry = 0
        while l1 or l2 or carry:
            total = 0
            total += carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next
            carry = total // 10
            curr.next = ListNode(total % 10)
            curr = curr.next
        return dummy.next
        
    # 80
    def findDuplicate(self, nums: List[int]) -> int:
        slow = fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
    
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
            self.cache = {}
            self.cap = capacity
            self.left, self.right = ListNode(), ListNode()
            self.left.next = self.right
            self.right.prev = self.left

        def _remove(self, node):
            prev, nxt = node.prev, node.next
            prev.next = nxt
            nxt.prev = prev
        
        def _insert(self, node):
            nxt = self.left.next
            self.left.next = node
            node.prev = self.left
            node.next = nxt
            nxt.prev = node

        def get(self, key: int) -> int:
            if key not in self.cache:
                return -1
            node = self.cache[key]
            self._remove(node)
            self._insert(node)
            return node.val

        def put(self, key: int, value: int) -> None:
            if key in self.cache:
                self._remove(self.cache[key])
            node = ListNode(key=key, val=value)
            self.cache[key] = node
            self._insert(node)

            if len(self.cache) > self.cap:
                lru = self.right.prev
                self._remove(lru)
                del self.cache[lru.key]

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
        heap = []
        for i, node in enumerate(lists):
            if node:
                heappush(heap, (node.val, i, node))
        dummy = curr = ListNode()
        while heap:
            _, i, node = heappop(heap)
            curr.next = node
            curr = curr.next
            if node.next:
                heappush(heap, (node.next.val, i, node.next))
        return dummy.next
    
    # 86
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        def getKth(curr, k):
            while curr and k > 0:
                curr = curr.next
                k -= 1
            return curr

        dummy = groupPrev = ListNode(next=head)
        while True:
            kth = getKth(groupPrev, k)
            if not kth:
                break
            groupNext = kth.next
            curr, prev = groupPrev.next, kth.next
            while curr != groupNext:
                tmp = curr.next
                curr.next = prev
                prev = curr
                curr = tmp
            tmp = groupPrev.next
            groupPrev.next = kth
            groupPrev = tmp
        return dummy.next
    
if __name__ == "__main__":
    s = Solution(); hl = ListHelper()
