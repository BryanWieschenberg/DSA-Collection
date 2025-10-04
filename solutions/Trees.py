from collections import defaultdict, deque
import math
from typing import List, Optional


class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Helper:
    def toTree(self, values: List):
        nodes = [Node(v) if v is not None else None for v in values]
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
                tmp.append([None, node, depth, connector, parent])  # [id, node_ref, depth, conn, parent_ref]
                dfs(node.right, depth + 1, 'R', node)

            dfs(root, 0, "", None)

            for i, it in enumerate(tmp):
                it[0] = i

            idx = {it[1]: it[0] for it in tmp}

            vals = [(it[0], it[1].val, it[2], it[3], (idx[it[4]] if it[4] is not None else None)) for it in tmp]
            return vals

        depth = getHeight(root)
        vals = bottomUp(root)

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
            ppos = positions[cid]
            cpos = positions[id]
            mid = (ppos + cpos) / 2
            mid = math.ceil(mid) if connector == 'L' else math.floor(mid)
            connectorLine = d * 2 - 1
            lines[connectorLine] += " " * (mid - len(lines[connectorLine])) + ('/' if connector == 'L' else '\\')

        output = """"""
        for i in range(len(lines)):
            output += lines[i]
            if i + 1 < len(lines):
                output += "\n"

        print(output)


class Solution:
    def invertTree(self, root: Optional[Node]) -> Optional[Node]:
        if not root: return None

        tmp = root.left
        root.left = root.right
        root.right = tmp

        self.invertTree(root.left)
        self.invertTree(root.right)
        
        return root

    def maxDepth(self, root: Optional[Node]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
    
s = Solution()
h = Helper()

# h.printTree( s. invertTree ( root=h.toTree([1,2,3,4,5,6,7]) )) # [3,1,2]

# print( s. maxDepth ( root=h.toTree([1,2,3,None,None,4]) )) # 3
