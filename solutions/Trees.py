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

        def bfs(self, root): # Level order traversal
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
        if root.val > val:
            return self.searchBST(root.left, val)
        elif root.val < val:
            return self.searchBST(root.right, val)
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
        def dfs(root, height):
            if not root: return None
            if len(res) == height:
                res.append(root.val)
            
            dfs(root.right, height+1)
            dfs(root.left, height+1)
            
        res = []
        dfs(root, 0)
        return res
        
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, maxVal):
            if not node: return 0

            res = 1 if node.val >= maxVal else 0
            maxVal = max(maxVal, node.val)

            res += dfs(node.left, maxVal)
            res += dfs(node.right, maxVal)
            
            return res

        return dfs(root, root.val)
    
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def dfs(node, left, right):
            if not node: return True

            if not (left < node.val < right): return False
            
            return (
                dfs(node.left, left, node.val) and
                dfs(node.right, node.val, right)
            )

        return dfs(root, float('-inf'), float('inf'))
    
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        curr = root

        while curr:
            if not curr.left:
                k -= 1
                if k == 0:
                    return curr.val
                curr = curr.right
            else:
                pred = curr.left
                while pred.right and pred.right != curr:
                    pred = pred.right

                if not pred.right:
                    pred.right = curr
                    curr = curr.left
                else:
                    pred.right = None
                    k -= 1
                    if k == 0:
                        return curr.val
                    curr = curr.right
        return -1
    
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def dfs(root1, root2):
            if not (root1 or root2):
                return True
            if (
                root1 and not root2 or
                root2 and not root1
            ):
                return False
            if root1.val != root2.val:
                return False
            return (
                dfs(root1.left, root2.right) and
                dfs(root1.right, root2.left)
            )

        return dfs(root, root)

    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root: return TreeNode(val)

        cur = root
        while True:
            if val > cur.val:
                if not cur.right:
                    cur.right = TreeNode(val)
                    return root
                cur = cur.right
            else:
                if not cur.left:
                    cur.left = TreeNode(val)
                    return root
                cur = cur.left

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not (preorder and inorder):
            return None

        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1 :], inorder[mid + 1 :])

        return root

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        def dfs(root):
            if not root: return 0

            leftMax = dfs(root.left)
            rightMax = dfs(root.right)
            leftMax = max(leftMax, 0)
            rightMax = max(rightMax, 0)

            res[0] = max(res[0], root.val + leftMax + rightMax)
            return root.val + max(leftMax, rightMax)
        res = [root.val]
        dfs(root)
        return res[0]
    
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return root

        if key > root.val:
            root.right = self.deleteNode(root.right, key)
        elif key < root.val:
            root.left = self.deleteNode(root.left, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            cur = root.right
            while cur.left:
                cur = cur.left
            cur.left = root.left
            res = root.right
            del root
            return res

        return root

s = Solution()
h = Helper()

# t = s.Traverse()
# iterable = range(1, 2**7+10)
# h.printTree( h.toTree([i for i in iterable]) )
# print("DFS:            ", t. dfs ( h.toTree([i for i in iterable]) ))
# print("DFS (Inorder):  ", t. dfs_inorder ( h.toTree([i for i in iterable]) ))
# print("DFS (Postorder):", t. dfs_postorder ( h.toTree([i for i in iterable]) ))
# print("BFS:            ", t. bfs ( h.toTree([i for i in iterable]) ))

# h.printTree( root=h.toTree([5,3,6,None,4,None,10,None,None,7]) )

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

# print( s. goodNodes ( root=h.toTree([1,2,-1,3,4]) )) # 3

# print( s. isValidBST ( root=h.toTree([5,4,6,None,None,3,7]) )) # False

# print( s. kthSmallest ( root=h.toTree([4,3,5,2,None]), k=2 )) # 1

# print( s. isSymmetric ( root=h.toTree([1,2,2,3,4,4,3]) )) # True

# h.printTree( s. insertIntoBST ( root=h.toTree([5,3,6,None,4,None,10,None,None,7]), val=1000 )) # True

# h.printTree( s. buildTree ( preorder=[1,2,30,4], inorder=[2,1,30,4] )) # [1,2,3,None,None,None,4]

# print( s. maxPathSum ( root=h.toTree([1,2,3]) )) # 6

# h.printTree( s. deleteNode ( root=h.toTree([5,3,6,None,4,None,10,None,None,7]), key=3 )) # [5,4,6,None,None,None,10,7]
