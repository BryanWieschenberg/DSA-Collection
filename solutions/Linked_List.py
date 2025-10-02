from collections import defaultdict
from typing import List, Optional

class Node:
    def __init__(self, val=0, next=None, prev=None, random=None, key=0):
        self.val = val
        self.next = next
        self.prev = prev
        self.random = random
        self.key = key

class Helper:
    def printLL(self, head: Optional[Node], end="\n"):
        curr = head
        while curr:
            print(f"{curr.val},{curr.random.val}" if curr.random else f"{curr.val}", end=" -> " if curr.next else end)
            curr = curr.next
    
    def toLL(self, values: List, cycle_index: Optional[int] = None) -> Optional[Node]:
        if isinstance(values[0], int):
            nodes = [Node(val=v) for v in values]
        else:
            nodes = [Node(val=pair[0]) for pair in values]

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
    def reverseList(self, head: Optional[Node]) -> Optional[Node]:
        curr, prev = head, None
        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        return prev

    def mergeTwoLists(self, list1: Optional[Node], list2: Optional[Node]) -> Optional[Node]:
        dummy = node = Node()
        
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
    
    def hasCycle(self, head: Optional[Node]) -> bool:
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
    
    def reorderList(self, head: Optional[Node]) -> Optional[Node]:
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

    def removeNthFromEnd(self, head: Optional[Node], n: int) -> Optional[Node]:
        dummy = Node(0, head)
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
    
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        old = defaultdict(lambda: Node(0))
        old[None] = None
        curr = head
        while curr:
            old[curr].val = curr.val
            old[curr].next = old[curr.next]
            old[curr].random = old[curr.random]
            curr = curr.next
        return old[head]
    
    # could be optimized with by making the curr OoM sum the .next, while remembering the carry val
    def addTwoNumbers(self, l1: Optional[Node], l2: Optional[Node]) -> Optional[Node]:
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
        dummy = node = Node()
        totalSum = str(totalSum)
        
        for i in range(len(totalSum)-1, -1, -1):
            node.next = Node(val=int(totalSum[i]))
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
            self.left, self.right = Node(0, 0), Node(0, 0)
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
            self.cache[key] = Node(key=key, val=value)
            self._insert(self.cache[key])

            if len(self.cache) > self.cap:
                lru = self.left.next
                self._remove(lru)
                del self.cache[lru.key]

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
