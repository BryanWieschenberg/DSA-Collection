from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List, Optional
from Helper import TreeNode, TreeHelper, QuadTreeNode, QuadTreeHelper

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
        pass

    # 91
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        pass
    
    # 92
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        pass

    # 93
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        pass

    # 94
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        pass

    # 95
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        pass

    # 96
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        pass
    
    # 97
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        pass
    
    # 98
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        pass
    
    # 99
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        pass

    # 100
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        pass
    
    # 101
    def construct(self, grid: List[List[int]]) -> Optional[QuadTreeNode]:
        pass
    
    # 102
    def goodNodes(self, root: TreeNode) -> int:
        pass

    # 103
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        pass

    # 104
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        pass

    # 105
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        pass

    # 106
    def rob(self, root: Optional[TreeNode]) -> int:
        pass

    # 107
    def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        pass

    # 108
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        pass

    # 109
    class Codec:
        def serialize(self, root: Optional[TreeNode]) -> str:
            pass

        def deserialize(self, data: str) -> Optional[TreeNode]:
            pass

if __name__ == "__main__":
    s = Solution(); ht = TreeHelper(); hq = QuadTreeHelper()
