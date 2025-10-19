import math
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None, prev=None, random=None, key=0):
        self.val = val
        self.next = next
        self.prev = prev
        self.random = random
        self.key = key

class ListHelper:
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

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class TreeHelper:
    def toTree(self, values: List):
        nodes = [TreeNode(v) if v is not None else None for v in values]
        for i in range(len(values)):
            if nodes[i] is not None:
                left = 2*i + 1
                right = 2*i + 2
                if left < len(values):
                    nodes[i].left = nodes[left]
                if right < len(values):
                    nodes[i].right = nodes[right]
        return nodes[0]

    def printTree(self, root):
        def getHeight(node):
            if node is None:
                return 0
            return 1 + max(getHeight(node.left), getHeight(node.right))

        def bottomUp(root):
            tmp = []

            def dfs(node, depth=0, connector="", parent=None):
                if not node:
                    return
                dfs(node.left, depth + 1, 'L', node)
                tmp.append([None, node, depth, connector, parent])
                dfs(node.right, depth + 1, 'R', node)

            dfs(root, 0, "", None)

            for i, it in enumerate(tmp):
                it[0] = i

            idx = {it[1]: it[0] for it in tmp}

            vals = [(it[0], it[1].val, it[2], it[3], (idx[it[4]] if it[4] is not None else None)) for it in tmp]
            return vals

        depth = getHeight(root)
        vals = bottomUp(root)
        if not vals:
            print("< Empty tree >")
            return
        
        lines = ["" for _ in range(depth * 2 - 1)]
        offsets = [0] * (depth * 2 - 1)
        positions = {}

        for i, (id, val, d, connector_sign, _) in enumerate(vals):
            text = str(val)
            w = len(text)

            line_index = d * 2
            
            lsp, rsp = 0, 0
            if i-1 >= 0 and vals[i-1][2] == d-1:
                lsp = 1
            elif i+1 < len(vals) and vals[i+1][2] == d-1:
                rsp = 1

            lines[line_index] += " " * (offsets[line_index] - len(lines[line_index]) + lsp) + text + " " * rsp
            offsets[line_index] = len(lines[line_index])

            if connector_sign == 'L':
                positions[id] = offsets[line_index] - rsp - 1
            else:
                positions[id] = offsets[line_index] - w - rsp

            for i in range(depth):
                li = i * 2
                if li != line_index:
                    offsets[li] += w + lsp + rsp
        for (id, val, d, connector, cid) in vals:
            if cid is None:
                continue
            ppos = positions[cid] + (len(str(vals[cid][1])) - 1 if connector == 'R' else -len(str(vals[cid][1])) // 2)
            cpos = positions[id]
            mid = (ppos + cpos) / 2
            mid = math.ceil(mid) if connector == 'L' else math.floor(mid)
            connectorLine = d * 2 - 1
            lines[connectorLine] += " " * (mid - len(lines[connectorLine])) + ('/' if connector == 'L' else '\\')

        output = ""
        for i in range(len(lines)):
            output += lines[i]
            if i + 1 < len(lines):
                output += "\n"

        print(output)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class TrieHelper:
    def toTrie(self, words):
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.end = True
        return root
  
    def printTrie(self, root):
        def helper(node, prefix, indent, is_last, is_root_child=False):
            while len(node.children) == 1 and not node.end:
                char = next(iter(node.children))
                prefix += char
                node = node.children[char]
            
            if is_root_child:
                lines.append(prefix)
                new_indent = ""
            else:
                connector = "└─ " if is_last else "├─ "
                lines.append(indent + connector + prefix)
                continuation = "  " if is_last else "│  "
                new_indent = indent + continuation
            
            if node.children:
                children = sorted(node.children.keys())
                for i, char in enumerate(children):
                    child_is_last = (i == len(children) - 1)
                    helper(node.children[char], char, new_indent, child_is_last, False)

        lines = []
        children = sorted(root.children.keys())
        for i, char in enumerate(children):
            is_last = (i == len(children) - 1)
            helper(root.children[char], char, "", is_last, True)

        print("\n".join(lines))
