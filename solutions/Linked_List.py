from collections import defaultdict
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None, prev=None, random=None, key=0):
        self.val = val
        self.next = next
        self.prev = prev
        self.random = random
        self.key = key

class Helper:
    def printLL(self, head: Optional[ListNode], end="\n"):
        curr = head
        while curr:
            print(f"{curr.val},{curr.random.val}" if curr.random else f"{curr.val}", end=" -> " if curr.next else end)
            curr = curr.next
    
    def toLL(self, values: List, cycle_index: Optional[int] = None) -> Optional[ListNode]:
        if isinstance(values[0], int):
            nodes = [ListNode(val=v) for v in values]
        else:
            nodes = [ListNode(val=pair[0]) for pair in values]

        for i in range(len(nodes)-1):
            nodes[i].next = nodes[i + 1]

        if cycle_index is not None and 0 <= cycle_index < len(nodes):
            nodes[-1].next = nodes[cycle_index]

        if isinstance(values[0], list):
            for i, pair in enumerate(values):
                randID = pair[1]
                if randID is None:
                    continue
                if 0 <= randID < len(nodes):
                    nodes[i].random = nodes[randID]
                else:
                    raise ValueError(f"Invalid random index {randID} for node {i}")

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
    
    def copyRandomList(self, head: 'Optional[ListNode]') -> 'Optional[ListNode]':
        old = defaultdict(lambda: ListNode(0))
        old[None] = None
        curr = head
        while curr:
            old[curr].val = curr.val
            old[curr].next = old[curr.next]
            old[curr].random = old[curr.random]
            curr = curr.next
        return old[head]
    
    # could be optimized with by making the curr OoM sum the .next, while remembering the carry val
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
    
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0, 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow2 = 0
        while True:
            slow = nums[slow]
            slow2 = nums[slow2]
            if slow == slow2:
                return slow

    class LRUCache:
        def __init__(self, capacity: int):
            self.cap = capacity
            self.cache = {}
            self.left, self.right = ListNode(0, 0), ListNode(0, 0)
            self.left.next = self.right
            self.right.prev = self.left

        def _remove(self, node):
            prev, nxt = node.prev, node.next
            prev.next, nxt.prev = nxt, prev

        def _insert(self, node):
            prev = self.right.prev
            prev.next = self.right.prev = node
            node.next, node.prev = self.right, prev

        def get(self, key: int) -> int:
            if key in self.cache:
                node = self.cache[key]
                self._remove(node)
                self._insert(node)
                return node.val
            return -1

        def put(self, key: int, value: int) -> None:
            if key in self.cache:
                self._remove(self.cache[key])
            self.cache[key] = ListNode(key=key, val=value)
            self._insert(self.cache[key])

            if len(self.cache) > self.cap:
                lru = self.left.next
                self._remove(lru)
                del self.cache[lru.key]

    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        def mergeList(l1, l2):
            dummy = tail = ListNode()
            
            while l1 and l2:
                if l1.val < l2.val:
                    tail.next = l1
                    l1 = l1.next
                else:
                    tail.next = l2
                    l2 = l2.next
                tail = tail.next
            tail.next = l1 or l2
            return dummy.next
        
        if len(lists) < 1:
            return None
        
        for i in range(1, len(lists)):
            lists[i] = mergeList(lists[i-1], lists[i])

        return lists[-1]
    
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:        
        def getKth(curr, k):
            while curr and k > 0:
                curr = curr.next
                k -= 1
            return curr

        dummy = groupPrev = ListNode(val=0, next=head)
        while True:
            kth = getKth(groupPrev, k)
            if not kth:
                break
            groupNext = kth.next

            prv, cur = kth.next, groupPrev.next
            while cur != groupNext:
                tmp = cur.next
                cur.next = prv
                prv = cur
                cur = tmp
            tmp = groupPrev.next
            groupPrev.next = kth
            groupPrev = tmp
        return dummy.next
    
    class MyLinkedList:
        def __init__(self):
            self.left = ListNode()
            self.right = ListNode()
            self.left.next = self.right
            self.right.prev = self.left
            self.leng = 0

        def _toIndex(self, index):
            curr = None
            if index < self.leng // 2:
                curr = self.left.next
                i = 0
                while i < index:
                    curr = curr.next
                    i += 1
            else:
                curr = self.right.prev
                i = 0
                while i < self.leng - index - 1:
                    curr = curr.prev
                    i += 1
            return curr

        def get(self, index: int) -> int:
            if index >= self.leng:
                return -1
            node = self._toIndex(index)
            return node.val

        def addAtHead(self, val: int) -> None:
            node = ListNode(val)
            node.next = self.left.next
            node.prev = self.left
            self.left.next.prev = node
            self.left.next = node
            self.leng += 1

        def addAtTail(self, val: int) -> None:
            node = ListNode(val)
            node.prev = self.right.prev
            node.next = self.right
            self.right.prev.next = node
            self.right.prev = node
            self.leng += 1

        def addAtIndex(self, index: int, val: int) -> None:
            if index > self.leng:
                return
            if index == self.leng:
                self.addAtTail(val)
                return
            right = self._toIndex(index)
            left = right.prev
            node = ListNode(val)
            left.next = node
            node.prev = left
            node.next = right
            right.prev = node
            self.leng += 1

        def deleteAtIndex(self, index: int) -> None:
            if index >= self.leng:
                return
            node = self._toIndex(index)
            node.prev.next = node.next
            node.next.prev = node.prev
            self.leng -= 1

    class BrowserHistory:
        def __init__(self, homepage: str):
            self.curr = ListNode(homepage)

        def visit(self, url: str) -> None:
            self.curr.next = None
            self.curr.next = ListNode(url)
            self.curr.next.prev = self.curr
            self.curr = self.curr.next
            return self.curr.val

        def back(self, steps: int) -> str:
            while self.curr.prev and steps:
                self.curr = self.curr.prev
                steps -= 1
            return self.curr.val

        def forward(self, steps: int) -> str:
            while self.curr.next and steps:
                self.curr = self.curr.next
                steps -= 1
            return self.curr.val    

s = Solution()
h = Helper()

# h.printLL( s. reverseList ( list1=h.toLL([1,2,3,4,5]) )) # 5 -> 4 -> 3 -> 2 -> 1

# h.printLL( s. mergeTwoLists ( list1=h.toLL([1,2,4]), list2=h.toLL([1,3,5]) )) # 1 -> 1 -> 2 -> 3 -> 4 -> 5

# print( s. hasCycle ( head=h.toLL([1,2,3,4], 1) )) # True

# h.printLL( s. reorderList ( head=h.toLL([2,4,6,8,10]) )) # 2 -> 10 -> 4 -> 8 -> 6

# h.printLL( s. removeNthFromEnd ( head=h.toLL([1,2,3,4]), n=2 )) # 1 -> 2 -> 4

# h.printLL( s. copyRandomList ( head=h.toLL([[3,None],[7,3],[4,0],[5,1]]) )) # 3 -> 7,5 -> 4,3 -> 5,7

# h.printLL( s. addTwoNumbers ( l1=h.toLL([1,2,3]), l2=h.toLL([4,5,6]) )) # 5 -> 7 -> 9

# print( s. findDuplicate ( [1,2,3,2,2] )) # 2

# LRUCache = s.LRUCache(3)
# LRUCache.put(1, 10)
# print(LRUCache.get(1)) # 10
# LRUCache.put(2, 20)
# LRUCache.put(3, 30)
# print(LRUCache.get(2)) # 20
# print(LRUCache.get(1)) # 10
# print(LRUCache.get(3)) # 30

# h.printLL( s. mergeKLists ( lists=[h.toLL([1,3,5]), h.toLL([2,4,6]), h.toLL([0,7])] )) # 1 -> 1 -> 2 -> 3 -> 3 -> 4 -> 5 -> 6

# h.printLL( s. reverseKGroup ( head=h.toLL([1,2,3,4,5,6,7,8]), k=3 )) # 2 -> 1 -> 4 -> 3 -> 6 -> 5 -> 7 -> 8

# myLinkedList = s.MyLinkedList()
# myLinkedList.addAtHead(1)
# myLinkedList.addAtTail(3)
# myLinkedList.addAtIndex(1, 2) # 1 -> 2 -> 3
# print(myLinkedList.get(1)) # 2
# myLinkedList.deleteAtIndex(1) # 1 -> 3
# print(myLinkedList.get(1)) # 3

# browserHistory = s.BrowserHistory("leetcode.com")
# print(browserHistory.visit("google.com")) # google.com
# print(browserHistory.visit("facebook.com")) # facebook.com
# print(browserHistory.visit("youtube.com")) # youtube.com
# print(browserHistory.back(1)) # facebook.com
# print(browserHistory.back(1)) # google.com
# print(browserHistory.forward(1)) # facebook.com
# print(browserHistory.visit("linkedin.com")) # linkedin.com
# print(browserHistory.forward(2)) # linkedin.com
# print(browserHistory.back(2)) # google.com
# print(browserHistory.back(7)) # leetcode.com
