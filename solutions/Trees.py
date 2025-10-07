from collections import defaultdict, deque
import math
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Helper:
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
        def dfs(self, root): # Preorder traversal
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

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        root.left, root.right = root.right, root.left

        self.invertTree(root.left)
        self.invertTree(root.right)
        
        return root

    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
    
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def dfs(root):
            if not root:
                return 0
            left = dfs(root.left)
            right = dfs(root.right)
            
            nonlocal res
            res = max(res, left + right)
            return 1 + max(left, right)

        res = 0
        dfs(root)
        return res
    
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
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
    
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        elif p and q and p.val == q.val:
            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        else:
            return False

    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return None
        if root.val < val:
            return self.searchBST(root.right, val)
        elif root.val > val:
            return self.searchBST(root.left, val)
        else:
            return root
    
    class Codec:
        def serialize(self, root: Optional[TreeNode]) -> str:
            def dfs(root):
                nonlocal s
                if not root:
                    s.append("#")
                    return
                s.append(str(root.val))

                dfs(root.left)
                dfs(root.right)
        
            s = []
            dfs(root)
            return ",".join(s)
            
        def deserialize(self, data: str) -> Optional[TreeNode]:
            def dfs():
                if not q:
                    return None
                val = q.popleft()
                if val == '#':
                    return None
                node = TreeNode(int(val))
                node.left = dfs()
                node.right = dfs()
                return node
            
            q = deque(data.split(","))
            return dfs()

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def serialize(root):
            if not root:
                return "$#"
            return "$" + str(root.val) + serialize(root.left) + serialize(root.right)
        
        def z_func(s):
            z = [0] * len(s)
            l, r, n = 0, 0, len(s)
            for i in range(1, n):
                if i <= r:
                    z[i] = min(r - i + 1, z[i - l])
                while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                    z[i] += 1
                if i + z[i] - 1 > r:
                    l, r = i, i + z[i] - 1
            return z
        
        rootSer = serialize(root)
        subRootSer = serialize(subRoot)
        z_vals = z_func(subRootSer + "|" + rootSer)

        for z in z_vals:
            if z == len(subRootSer):
                return True
        
        return False
    
    def lowestCommonAncestor(self, root: Optional[TreeNode], p: Optional[TreeNode], q: Optional[TreeNode]) -> Optional[TreeNode]:
        curr = root
        while curr:
            if curr.val > p.val and curr.val > q.val:
                curr = curr.left
            elif curr.val < p.val and curr.val < q.val:
                curr = curr.right
            else:
                return curr
        
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root: return []
        res = []
        q = deque()
        q.append(root)
        while q:
            qLen = len(q)
            level = []
            for i in range(qLen):
                node = q.popleft()
                if node:
                    level.append(node.val)
                    q.append(node.left)
                    q.append(node.right)
            if level:
                res.append(level)
        return res
    
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        def dfs(root, height):
            if not root: return None
            if len(res) == height:
                res.append(root.val)
            
            dfs(root.right, height+1)
            dfs(root.left, height+1)
            
        dfs(root, 0)
        return res
    
    def goodNodes(self, root: TreeNode) -> int:
        if not root: return 0
        res = 1
        def dfs(root):
            if not root: return None

            nonlocal res
            if root.left and root.left.val >= root.val:
                res += 1
            if root.right and root.right.val >= root.val:
                res += 1

            dfs(root.left)
            dfs(root.right)

        dfs(root)
        return res
    
s = Solution()
h = Helper()

# t = s.Traverse()
# iterable = range(1, 2**3)
# h.printTree( h.toTree([i for i in iterable]) )
# print("DFS:            ", t. dfs ( h.toTree([i for i in iterable]) ))
# print("DFS (Inorder):  ", t. dfs_inorder ( h.toTree([i for i in iterable]) ))
# print("DFS (Postorder):", t. dfs_postorder ( h.toTree([i for i in iterable]) ))
# print("BFS:            ", t. bfs ( h.toTree([i for i in iterable]) ))

h.printTree( h.toTree([1,2,-1,3,4]) )

# h.printTree( s. invertTree ( root=h.toTree([1,2,3,4,5,6,7]) )) # [3,1,2]

# print( s. maxDepth ( root=h.toTree([1,2,3,None,None,4]) )) # 3

# print( s. isBalanced ( root=h.toTree([1,2,3,None,None,4]) )) # True

# print( s. isSameTree ( p=h.toTree([1,2,3]), q=h.toTree([1,2,3]) )) # True

# h.printTree( s. searchBST ( root=h.toTree([4,2,7,1,3]), val=2 ) ) # [2,1,3]

# codec = s.Codec()
# serialized = ( codec.serialize ( root=h.toTree([1,2,3,None,None,4,5,6,7,8,None,None,None,12,15]) )) # "1,2,#,#,3,4,#,#,5,#,#"
# print(serialized)
# h.printTree( codec.deserialize ( data=serialized )) # [1,2,3,None,None,4,5]

# print( s. isSubtree ( root=h.toTree([1,2,3,4,5]), subRoot=h.toTree([2,4,5]) )) # True

# h.printTree( s. lowestCommonAncestor ( root=h.toTree([5,3,8,1,4,7,9,None,2]), p=3, q=8 )) # [3,1,2,4]

# print( s. levelOrder ( root=h.toTree([1,2,3,4,5,6,7]) )) # [[1],[2,3],[4,5,6,7]]

# print( s. rightSideView ( root=h.toTree([1,2,3,4]) )) # [1,3,4]

print( s. goodNodes ( root=h.toTree([1,2,-1,3,4]) )) # 3
