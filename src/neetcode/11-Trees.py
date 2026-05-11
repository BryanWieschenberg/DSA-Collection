from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(ospath.dirname(__file__))))
from typing import List, Optional
from Helper import TreeNode, TreeHelper, QuadNode, QuadHelper
from collections import deque


class Solution:
    # 153
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node):
            if not node:
                return None
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)

        res = []
        dfs(root)
        return res

    # 154
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node):
            if not node:
                return None
            res.append(node.val)
            dfs(node.left)
            dfs(node.right)

        res = []
        dfs(root)
        return res

    # 155
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node):
            if not node:
                return None
            dfs(node.left)
            dfs(node.right)
            res.append(node.val)

        res = []
        dfs(root)
        return res

    # 156
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node):
            if not node:
                return
            node.left, node.right = node.right, node.left
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return root
    
    # 157
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0
            return 1 + max(dfs(node.left), dfs(node.right))
        return dfs(root)
        
    # 158
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0
            nonlocal res
            l = dfs(node.left)
            r = dfs(node.right)
            res = max(res, l + r)
            return 1 + max(l, r)
        res = 0
        dfs(root)
        return res

    # 159
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        if not (root.left or root.right):
            return targetSum == root.val
        total = targetSum - root.val
        return (
            self.hasPathSum(root.left, total) or
            self.hasPathSum(root.right, total)
        )

    # 160
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def dfs(node):
            if not node:
                return (True, 0)
            lBal, l = dfs(node.left)
            rBal, r = dfs(node.right)
            isBalanced = abs(l - r) <= 1 and lBal and rBal
            return (isBalanced, max(l, r) + 1)
        return dfs(root)[0]

    # 161
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not (p or q):
            return True
        if (not p and q) or (p and not q) or p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        
    # 162
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def isSameTree(p, q):
            if not (p or q):
                return True
            if p and q and p.val == q.val:
                return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
            return False
        
        if not (root or subRoot):
            return True
        if not root:
            return False
        if isSameTree(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
    
    # 163
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)
        if p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)
        return root
        
    # 164
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return TreeNode(val)
        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        else:
            root.right = self.insertIntoBST(root.right, val)
        return root
    
    # 165
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            curr = root.right
            while curr.left:
                curr = curr.left
            root.val = curr.val
            root.right = self.deleteNode(root.right, curr.val)
        return root

    # 166
    class BinarySearchTree:
        def __init__(self):
            self.root: Optional[TreeNode] = None

        def insert(self, val: int) -> None:
            def traverse(node, val):
                if not node:
                    return TreeNode(val)
                if val < node.val:
                    node.left = traverse(node.left, val)
                else:
                    node.right = traverse(node.right, val)
                return node

            self.root = traverse(self.root, val)

        def search(self, val: int) -> bool:
            def traverse(node, val):
                if not node:
                    return False
                if val < node.val:
                    return traverse(node.left, val)
                elif val > node.val:
                    return traverse(node.right, val)
                else:
                    return True
            
            return traverse(self.root, val)

        def delete(self, val: int) -> None:
            def traverse(node, key):
                if not node:
                    return None
                if key < node.val:
                    node.left = traverse(node.left, key)
                elif key > node.val:
                    node.right = traverse(node.right, key)
                else:
                    if not node.left:
                        return node.right
                    elif not node.right:
                        return node.left
                    curr = node.right
                    while curr.left:
                        curr = curr.left
                    node.val = curr.val
                    node.right = traverse(node.right, curr.val)
                return node
            
            self.root = traverse(self.root, val)

        def get_root(self) -> TreeNode:
            return self.root

    # 167
    class BSTIterator:
        def __init__(self, root: Optional[TreeNode]):
            self.st = []
            self._leftmost_inorder(root)

        def _leftmost_inorder(self, root: Optional[TreeNode]) -> None:
            while root:
                self.st.append(root)
                root = root.left
            
        def next(self) -> int:
            topmost_node = self.st.pop()
            if topmost_node.right:
                self._leftmost_inorder(topmost_node.right)
            return topmost_node.val

        def hasNext(self) -> bool:
            return bool(self.st)

    # 168
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        q = deque([root])
        res = []
        while q:
            qLen = len(q)
            lvl = []
            for _ in range(qLen):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
                lvl.append(node.val)
            res.append(lvl)
        return res
    
    # 169
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node, depth):
            if not node:
                return 0
            if depth == len(res):
                res.append(node.val)
            dfs(node.right, depth+1)
            dfs(node.left, depth+1)

        res = []
        dfs(root, 0)
        return res
    
    # 170
    def construct(self, grid: List[List[int]]) -> Optional[QuadNode]:
        def solve(r, c, n):
            is_same = True
            first_val = grid[r][c]
            for i in range(r, r+n):
                for j in range(c, c+n):
                    if grid[i][j] != first_val:
                        is_same = False
                        break
                if not is_same:
                    break
            if is_same:
                return QuadNode(first_val == 1, True)
            n //= 2
            tl = solve(r, c, n)
            tr = solve(r, c+n, n)
            bl = solve(r+n, c, n)
            br = solve(r+n, c+n, n)
            return QuadNode(True, False, tl, tr, bl, br)
        
        return solve(0, 0, len(grid))

    # 171
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, maxVal):
            if not node:
                return
            nonlocal res
            if maxVal <= node.val:
                res += 1
            dfs(node.left, max(maxVal, node.val))
            dfs(node.right, max(maxVal, node.val))
            
        res = 0
        dfs(root, float('-inf'))
        return res

    # 172
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def dfs(node, l, r):
            if not node:
                return True
            left = dfs(node.left, l, node.val)
            right = dfs(node.right, node.val, r)
            if l < node.val < r:
                return left and right
            return False

        return dfs(root, float('-inf'), float('inf'))
    
    # 173
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        def dfs(node):
            nonlocal k, res
            if not node or res is not None:
                return
            dfs(node.left)
            k -= 1
            if k == 0:
                res = node.val
                return
            dfs(node.right)
        
        res = None
        dfs(root)
        return res
    
    # 174
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        def dfs(l, r):
            if l > r:
                return None
            nonlocal pre_i
            root_val = preorder[pre_i]
            pre_i += 1
            root = TreeNode(root_val)
            m = idx[root_val]
            root.left = dfs(l, m-1)
            root.right = dfs(m+1, r)
            return root
        idx = {val: i for i, val in enumerate(inorder)}
        pre_i = 0
        return dfs(0, len(inorder)-1)

    # 175
    def rob(self, root: Optional[TreeNode]) -> int:
        pass

    # 176
    def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        pass

    # 177
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0
            nonlocal res
            left = max(dfs(node.left), 0)
            right = max(dfs(node.right), 0)
            res = max(res, node.val + left + right)
            return node.val + max(left, right)

        res = root.val
        dfs(root)
        return res
    
    # 178
    class Codec:
        def serialize(self, root: Optional[TreeNode]) -> str:
            def dfs(root):
                if not root:
                    res.append('N')
                    return
                res.append(str(root.val))
                dfs(root.left)
                dfs(root.right)
            res = []
            dfs(root)
            return ','.join(res)
            
        def deserialize(self, data: str) -> Optional[TreeNode]:
            def dfs():
                nonlocal i
                if vals[i] == 'N':
                    i += 1
                    return None
                node = TreeNode(int(vals[i]))
                i += 1
                node.left = dfs()
                node.right = dfs()
                return node
            vals = data.split(',')
            i = 0
            return dfs()


if __name__ == "__main__":
    s = Solution(); ht = TreeHelper(); hq = QuadHelper()
