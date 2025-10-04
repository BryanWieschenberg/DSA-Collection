from collections import defaultdict, deque
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

        def bottomUp(node, depth=0, is_left=False, is_right=False):
            if node is None:
                return []
            left_vals = bottomUp(node.left, depth+1, False, True)
            right_vals = bottomUp(node.right, depth+1, True, False)
            
            return (
                left_vals
                + [(node.val, depth, is_left, is_right)]
                + right_vals
            )

        depth = getHeight(root)
        vals = bottomUp(root)

        lines = ["" for _ in range(depth * 2 - 1)]
        offsets = [0] * (depth * 2 - 1)

        for i, (val, d, Lparent, Rparent) in enumerate(vals):
            text = str(val)
            w = len(text)

            line_index = d * 2
            
            lsp, rsp = 0, 0
            if i-1 >= 0 and vals[i-1][1] == d-1:
                lsp = 1
            elif i+1 < len(vals) and vals[i+1][1] == d-1:
                rsp = 1

            lines[line_index] += " " * (offsets[line_index] - len(lines[line_index]))
            
            if Lparent:
                lines[line_index-1] += " " * (offsets[line_index] - len(lines[line_index-1]) + lsp - 1) + "\\"
            elif Rparent:
                lines[line_index-1] += " " * (offsets[line_index] - len(lines[line_index-1]) + w) + "/"

            lines[line_index] += " " * lsp + text + " " * rsp
            offsets[line_index] = len(lines[line_index])

            for i in range(depth):
                li = i * 2
                if li != line_index:
                    offsets[li] += w + lsp + rsp

        for line in lines:
            print(line)


class Solution:
    def invertTree(self, root: Optional[Node]) -> Optional[Node]:
        pass

s = Solution()
h = Helper()

h.printTree( h.toTree([3,2,1]) ) # [3,1,2]
