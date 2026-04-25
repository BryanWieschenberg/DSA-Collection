from __future__ import annotations
from typing import List, Optional
from collections import deque


class ListNode:
    def __init__(
        self,
        val: int = 0,
        next: Optional[ListNode] = None,
        prev: Optional[ListNode] = None,
        key: Optional[int] = None,
        random: Optional[ListNode] = None,
        starts_cycle: bool = False
    ):
        self.val = val
        self.next = next
        self.prev = prev
        self.key = key
        self.random = random
        self.starts_cycle = starts_cycle


class ListHelper:
    def to(
        self,
        lst: List[int | List[int]],
        cycle_val: Optional[int] = None
    ) -> ListNode:
        dummy = curr = ListNode()
        nodes = {}
        if isinstance(lst[0], int):
            for val in lst:
                node = ListNode(val)
                nodes[val] = node
                curr.next = node
                curr = curr.next
        else:
            for val, _ in lst:
                node = ListNode(val)
                nodes[val] = node
                curr.next = node
                curr = curr.next
            for val, rand in lst:
                nodes[val].random = nodes[rand]
        if cycle_val:
            curr.starts_cycle = True
            curr.next = nodes[cycle_val]
        return dummy.next

    def prnt(
        self,
        head: Optional[ListNode],
        verbose: bool = True
    ) -> str:
        if not head:
            if verbose:
                print("< Empty linked list >")
            return "L[]"

        res = []
        if head.random:
            curr = head
            while curr:
                res.append(f"[{curr.val}, {curr.random.val}]")
                if curr.starts_cycle:
                    res.append(f"{curr.next.val}...")
                    break
                curr = curr.next
        else:
            curr = head
            while curr:
                res.append(f"{curr.val}")
                if curr.starts_cycle:
                    res.append(f"{curr.next.val}...")
                    break
                curr = curr.next
        res_str = f"L[{', '.join(res)}]"
        if verbose:
            print(res_str)
        return res_str


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional[TreeNode] = None,
        right: Optional[TreeNode] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


class TreeHelper:
    def to(
        self,
        lst: List[Optional[int]],
    ) -> TreeNode:
        root = TreeNode(lst[0])
        q = deque([root])
        pos = 1
        while q:
            for _ in range(len(q)):
                parent = q.popleft()
                for side in ['left', 'right']:
                    if pos < len(lst) and lst[pos] is not None:
                        child = TreeNode(lst[pos])
                        setattr(parent, side, child)
                        q.append(child)
                    pos += 1
        return root

    def prnt(
        self,
        root: Optional[TreeNode],
        verbose: bool = True
    ) -> str:
        if not root:
            if verbose:
                print("< Empty binary tree >")
            return "T[]"

        res = []
        q = deque([root])
        
        while q:
            node = q.popleft()
            if node:
                res.append(str(node.val))
                q.append(node.left)
                q.append(node.right)
            else:
                res.append('N')
                
        while res and res[-1] == 'N':
            res.pop()
            
        res_str = f"T[{', '.join(res)}]"
        if verbose:
            print(res_str)
        return res_str


class QuadNode:
    def __init__(
        self,
        val: bool,
        isLeaf: bool,
        topLeft: Optional[QuadNode] = None,
        topRight: Optional[QuadNode] = None,
        bottomLeft: Optional[QuadNode] = None,
        bottomRight: Optional[QuadNode] = None,
    ):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


class QuadHelper:
    def to(
        self,
        lst: List[Optional[List[int]]],
    ) -> QuadNode:
        root = QuadNode(bool(lst[0][1]), bool(lst[0][0]))
        q = deque([root])
        pos = 1

        while q:
            parent = q.popleft()
            if not parent.isLeaf:
                for corner in ['topLeft', 'topRight', 'bottomLeft', 'bottomRight']:
                    if pos < len(lst) and lst[pos] is not None:
                        isLeaf = bool(lst[pos][0])
                        val = bool(lst[pos][1])
                        child = QuadNode(val, isLeaf)
                        setattr(parent, corner, child)
                        q.append(child)
                    pos += 1
        return root

    def prnt(
        self,
        root: Optional[QuadNode],
        verbose: bool = True
    ) -> str:
        if not root:
            if verbose:
                print("< Empty quad tree >")
            return "Q[]"

        res = []
        q = deque([root])
        
        while q:
            node = q.popleft()
            if node:
                res.append(f"[{int(node.isLeaf)}, {int(node.val)}]")
                if not node.isLeaf:
                    q.append(node.topLeft)
                    q.append(node.topRight)
                    q.append(node.bottomLeft)
                    q.append(node.bottomRight)
            else:
                res.append('N')
                
        while res and res[-1] == 'N':
            res.pop()
            
        res_str = f"Q[{', '.join(res)}]"
        if verbose:
            print(res_str)
        return res_str


class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False


class TrieHelper:
    def to(
        self,
        lst: List[str],
    ) -> TrieNode:
        root = TrieNode()
        for word in lst:
            curr = root
            for char in word:
                if char not in curr.children:
                    curr.children[char] = TrieNode()
                curr = curr.children[char]
            curr.end = True
        return root

    def prnt(
        self,
        root: Optional[TrieNode],
        verbose: bool = True
    ) -> str:
        def dfs(node: TrieNode, path: List[str]) -> None:
            if node.end:
                words.append("'" + "".join(path) + "'")

            for char, child in sorted(node.children.items()):
                path.append(char)
                dfs(child, path)
                path.pop()

        if not root:
            if verbose:
                print("< Empty trie >")
            return "I[]"

        words = []
        dfs(root, [])

        res_str = f"I[{', '.join(words)}]"
        if verbose:
            print(res_str)
        return res_str


class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List[Node]] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class GraphHelper:
    def to(
        self,
        lst: List[List[int]]
    ) -> Node:
        nodes = {i + 1: Node(val=i + 1) for i in range(len(lst))}
        for i, neighbors in enumerate(lst):
            nodes[i + 1].neighbors = [nodes[n] for n in neighbors]
            
        return nodes[1] if nodes else None

    def prnt(
        self,
        node: Optional[Node],
        verbose: bool = True
    ) -> str:
        if not node:
            if verbose:
                print("< Empty graph >")
            return "G[]"
            
        visited = set()
        q = deque([node])
        nodes = {}
        
        while q:
            curr = q.popleft()
            if curr.val not in visited:
                visited.add(curr.val)
                nodes[curr.val] = curr
                for neighbor in curr.neighbors:
                    if neighbor.val not in visited:
                        q.append(neighbor)
                        
        max_val = max(nodes.keys()) if nodes else 0
        adj_list = []
        for i in range(1, max_val + 1):
            if i in nodes:
                adj_list.append(f"[{', '.join(str(n.val) for n in nodes[i].neighbors)}]")
            else:
                adj_list.append("[]")
                
        res_str = f"G[{', '.join(adj_list)}]"
        if verbose:
            print(res_str)
        return res_str


class Interval:
    def __init__(self, start: int = 0, end: int = 0):
        self.start = start
        self.end = end


class IntervalHelper:
    def to(
        self,
        lst: List[List[int]]
    ) -> List[Interval]:
        return [Interval(start, end) for start, end in lst]

    def prnt(
        self,
        lst: List[Interval],
        verbose: bool = True
    ) -> str:
        if not lst:
            if verbose:
                print("< Empty interval >")
            return "V[]"
            
        res = [f"[{i.start}, {i.end}]" for i in lst]
        res_str = f"V[{', '.join(res)}]"
        if verbose:
            print(res_str)
        return res_str
