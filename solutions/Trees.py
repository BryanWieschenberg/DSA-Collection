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
            ppos = positions[cid]
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

class Solution:
    class Traverse:
        def dfs(self, root):
            if not root:
                return []
            return [root.val] + self.dfs(root.left) + self.dfs(root.right)

        def dfs_inorder(self, root):
            if not root:
                return []
            return self.dfs_inorder(root.left) + [root.val] + self.dfs_inorder(root.right)

        def dfs_postorder(self, root):
            if not root:
                return []
            return self.dfs_postorder(root.left) + self.dfs_postorder(root.right) + [root.val]

        def bfs(self, root):
            if not root:
                return []
            res = []
            q = deque([root])
            while q:
                node = q.popleft()
                res.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            return res

    def invertTree(self, root: Optional[Node]) -> Optional[Node]:
        if not root:
            return None

        root.left, root.right = root.right, root.left

        self.invertTree(root.left)
        self.invertTree(root.right)
        
        return root

    def maxDepth(self, root: Optional[Node]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
    
    def diameterOfBinaryTree(self, root: Optional[Node]) -> int:
        res = 0
        def dfs(root):
            if not root:
                return 0
            left = dfs(root.left)
            right = dfs(root.right)
            
            nonlocal res
            res = max(res, left + right)
            return 1 + max(left, right)

        dfs(root)
        return res
    
    def isBalanced(self, root: Optional[Node]) -> bool:
        def dfs(root):
            if not root:
                return [True, 0]
            left, right = dfs(root.left), dfs(root.right)
            balanced = (
                left[0] and right[0] and
                abs(left[1] - right[1]) <= 1
            )
            return [balanced, 1 + max(left[1], right[1])]
        
        return dfs(root)[0]
    
    def isSameTree(self, p: Optional[Node], q: Optional[Node]) -> bool:
        if not (p or q):
            return True
        if p and q and p.val == q.val:
            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        else:
            return False

    def searchBST(self, root: Optional[Node], val: int) -> Optional[Node]:
        if not root:
            return None
        if root.val < val:
            return self.searchBST(root.right, val)
        elif root.val > val:
            return self.searchBST(root.left, val)
        else:
            return root
            
    def isSubtree(self, root: Optional[Node], subRoot: Optional[Node]) -> bool:
        pass

s = Solution()
h = Helper()

t = s.Traverse()
iterable = range(1, 2**3)
h.printTree( h.toTree([i for i in iterable]) )
print("DFS:            ", t. dfs ( h.toTree([i for i in iterable]) ))
print("DFS (Inorder):  ", t. dfs_inorder ( h.toTree([i for i in iterable]) ))
print("DFS (Postorder):", t. dfs_postorder ( h.toTree([i for i in iterable]) ))
print("BFS:            ", t. bfs ( h.toTree([i for i in iterable]) ))

# h.printTree( s. invertTree ( root=h.toTree([1,2,3,4,5,6,7]) )) # [3,1,2]

# print( s. maxDepth ( root=h.toTree([1,2,3,None,None,4]) )) # 3

# print( s. isBalanced ( root=h.toTree([1,2,3,None,None,4]) )) # True

# print( s. isSameTree ( p=h.toTree([1,2,3]), q=h.toTree([1,2,3]) )) # True

# h.printTree( s. searchBST ( root=h.toTree([4,2,7,1,3]), val=2 ) ) # [2,1,3]

# print( s. isSubtree ( p=h.toTree([1,2,3]), q=h.toTree([1,2,3]) )) # True
