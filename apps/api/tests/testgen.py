import random
from typing import List, Optional, Dict, Set, Union
from app.dsa import TreeNode

class TestGen:
    def __init__(self):
        self.id = 181
        self.name = "AVL Tree"
        self.difficulty = "Hard"
        self.code = """class AVLTree:
    def __init__(self):
        

    def insert(self, val: int) -> None:
        

    def delete(self, val: int) -> None:
        

    def getRoot(self) -> TreeNode:
        """
        self.description = "Design a self-balancing binary search tree (AVL tree) supporting insert, delete, and height maintenance."
        self.constraints = [
            "`1 <= operations.length <= 5000`",
            "`-10^5 <= val <= 10^5`"
        ]

    def get_public_cases(self):
        return [
            [("AVLTree", []), ("insert", [10]), ("insert", [20]), ("insert", [30]), ("getRoot", [])]
        ]

    def get_private_cases(self):
        cases = []
        for size in [1000, 2000, 3000, 4000, 5000]:
            ops = [("AVLTree", [])]
            inserted = []
            for _ in range(size):
                if inserted and random.random() < 0.3:
                    val = random.choice(inserted)
                    ops.append(("delete", [val]))
                    inserted.remove(val)
                else:
                    val = random.randint(-100000, 100000)
                    ops.append(("insert", [val]))
                    inserted.append(val)
            ops.append(("getRoot", []))
            cases.append(ops)
        return cases

    class AVLTree:
        def __init__(self):
            self.root = None

        def get_height(self, node):
            if not node: return 0
            return getattr(node, 'height', 0)

        def get_balance(self, node):
            if not node: return 0
            return self.get_height(node.left) - self.get_height(node.right)

        def rotate_right(self, y):
            x = y.left
            T2 = x.right
            x.right = y
            y.left = T2
            y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
            x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
            return x

        def rotate_left(self, x):
            y = x.right
            T2 = y.left
            y.left = x
            x.right = T2
            x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
            y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
            return y

        def insert(self, val: int) -> None:
            def _insert(node, val):
                if not node:
                    n = TreeNode(val)
                    n.height = 1
                    return n
                if val < node.val:
                    node.left = _insert(node.left, val)
                else:
                    node.right = _insert(node.right, val)
                node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
                balance = self.get_balance(node)
                if balance > 1 and val < node.left.val:
                    return self.rotate_right(node)
                if balance < -1 and val > node.right.val:
                    return self.rotate_left(node)
                if balance > 1 and val > node.left.val:
                    node.left = self.rotate_left(node.left)
                    return self.rotate_right(node)
                if balance < -1 and val < node.right.val:
                    node.right = self.rotate_right(node.right)
                    return self.rotate_left(node)
                return node
            self.root = _insert(self.root, val)

        def delete(self, val: int) -> None:
            def _delete(node, val):
                if not node:
                    return node
                if val < node.val:
                    node.left = _delete(node.left, val)
                elif val > node.val:
                    node.right = _delete(node.right, val)
                else:
                    if not node.left:
                        return node.right
                    elif not node.right:
                        return node.left
                    temp = node.right
                    while temp.left:
                        temp = temp.left
                    node.val = temp.val
                    node.right = _delete(node.right, temp.val)
                node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
                balance = self.get_balance(node)
                if balance > 1 and self.get_balance(node.left) >= 0:
                    return self.rotate_right(node)
                if balance > 1 and self.get_balance(node.left) < 0:
                    node.left = self.rotate_left(node.left)
                    return self.rotate_right(node)
                if balance < -1 and self.get_balance(node.right) <= 0:
                    return self.rotate_left(node)
                if balance < -1 and self.get_balance(node.right) > 0:
                    node.right = self.rotate_right(node.right)
                    return self.rotate_left(node)
                return node
            self.root = _delete(self.root, val)

        def getRoot(self) -> TreeNode:
            return self.root
