from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 45
    def calPoints(self, operations: List[str]) -> int:
        stack = []
        res = 0
        for o in operations:
            if o == '+':
                tmp = stack.pop()
                add = stack[-1] + tmp
                stack.append(tmp)
                stack.append(add)
                res += add
            elif o == 'C':
                res -= stack.pop()
            elif o == 'D':
                stack.append(stack[-1] * 2)
                res += stack[-1]
            else:
                stack.append(int(o))
                res += stack[-1]
        return res
    
    # 46
    def isValid(self, s: str) -> bool:
        stack = []
        opn, cls = ['[', '(', '{'], [']', ')', '}']
        for c in s:
            if not stack and c in cls:
                return False
            elif c in opn:
                stack.append(c)
            elif (
                (c == ']' and stack[-1] == '[') or
                (c == ')' and stack[-1] == '(') or
                (c == '}' and stack[-1] == '{')
            ):
                stack.pop()
            else:
                return False
        return not stack
    
    # 47
    class MyStack:
        def __init__(self):
            pass

        def push(self, x: int) -> None:
            pass

        def pop(self) -> int:
            pass

        def top(self) -> int:
            pass

        def empty(self) -> bool:
            pass

    # 48
    class MyQueue:
        def __init__(self):
            pass

        def push(self, x: int) -> None:
            pass

        def pop(self) -> int:
            pass

        def peek(self) -> int:
            pass

        def empty(self) -> bool:
            pass

    # 49
    class MinStack:
        def __init__(self):
            pass

        def push(self, val: int) -> None:
            pass

        def pop(self) -> None:
            pass

        def top(self) -> int:
            pass

        def getMin(self) -> int:
            pass

    # 50
    def evalRPN(self, tokens: List[str]) -> int:
        pass

    # 51
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        pass

    # 52
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        pass

    # 53
    class StockSpanner:
        def __init__(self):
            pass

        def next(self, price: int) -> int:
            pass
    
    # 54
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pass

    # 55
    def simplifyPath(self, path: str) -> str:
        pass

    # 56
    def decodeString(self, s: str) -> str:
        pass

    # 57
    class FreqStack:
        def __init__(self):
            pass

        def push(self, val: int) -> None:
            pass

        def pop(self) -> int:
            pass

    # 58
    def largestRectangleArea(self, heights: List[int]) -> int:
        pass

if __name__ == "__main__":
    s = Solution()
    s.isValid("[]")