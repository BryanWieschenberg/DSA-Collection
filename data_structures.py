from typing import List, Optional

class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None
        self.prev = None

def toLL(list: List[int]) -> Optional[ListNode]:
    if not list:
        return None
    head = ListNode(list[0])
    curr = head
    for value in list[1:]:
        curr.next = ListNode(value)
        curr = curr.next
    return head

def printLL(head: Optional[ListNode]) -> None:
    while head:
        print(head.val, end=" -> " if head.next else "")
        head = head.next
