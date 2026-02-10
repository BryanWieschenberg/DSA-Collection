from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List, Optional
from Helper import TreeNode, TreeHelper, QuadTreeNode, QuadTreeHelper
from collections import deque

class Solution:
    # 87
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        pass

    # 88
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        pass

    # 89
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        pass

    # 90
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node):
            if not node:
                return
            node.left, node.right = node.right, node.left
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return root
    
    # 91
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0
            return 1 + max(dfs(node.left), dfs(node.right))
        return dfs(root)
        
    # 92
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

    # 93
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def dfs(node):
            if not node:
                return 0
            l = dfs(node.left)
            if l == -1:
                return -1
            r = dfs(node.right)
            if r == -1:
                return -1
            if abs(l - r) > 1:
                return -1
            return 1 + max(l, r)
        return dfs(root) != -1

    # 94
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not (p or q):
            return True
        if p and q and p.val == q.val:
            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        return False
    
    # 95
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
    
    # 96
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)
        if p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)
        return root
        
    # 97
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        pass
    
    # 98
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        pass
    
    # 99
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
    
    # 100
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
    
    # 101
    def construct(self, grid: List[List[int]]) -> Optional[QuadTreeNode]:
        pass
    
    # 102
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

    # 103
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
    
    # 104
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
    
    # 105
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

    # 106
    def rob(self, root: Optional[TreeNode]) -> int:
        pass

    # 107
    def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        pass

    # 108
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
    
    # 109
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
    s = Solution(); ht = TreeHelper(); hq = QuadTreeHelper()
