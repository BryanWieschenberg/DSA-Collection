from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List

class Solution:
    # 45
    def calPoints(self, operations: List[str]) -> int:
        pass
    
    # 46
    def isValid(self, s: str) -> bool:
        st = []
        for c in s:
            if c in ['(','{','[']:
                st.append(c)
            elif st and (
                (c == ')' and st[-1] == '(') or
                (c == '}' and st[-1] == '{') or
                (c == ']' and st[-1] == '[')
            ):
                st.pop()
            else:
                return False
        return not st
        
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
            self.st = []
            self.minst = []

        def push(self, val: int) -> None:
            self.st.append(val)
            if not self.minst or val <= self.minst[-1]:
                self.minst.append(val)
            else:
                self.minst.append(self.minst[-1])

        def pop(self) -> None:
            self.st.pop()
            self.minst.pop()

        def top(self) -> int:
            return self.st[-1]

        def getMin(self) -> int:
            return self.minst[-1]

    # 50
    def evalRPN(self, tokens: List[str]) -> int:
        st = []
        for t in tokens:
            if t == '+':
                val2, val1 = st.pop(), st.pop()
                st.append(val1 + val2)
            elif t == '-':
                val2, val1 = st.pop(), st.pop()
                st.append(val1 - val2)
            elif t == '*':
                val2, val1 = st.pop(), st.pop()
                st.append(val1 * val2)
            elif t == '/':
                val2, val1 = st.pop(), st.pop()
                st.append(int(val1 / val2))
            else:
                st.append(int(t))
        return st[-1]
        
    # 51
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        pass

    # 52
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        st = []
        res = [0] * len(temperatures)
        for i in range(len(temperatures)):
            while st and temperatures[i] > temperatures[st[-1]]:
                idx = st.pop()
                res[idx] = i - idx
            st.append(i)
        return res
    
    # 53
    class StockSpanner:
        def __init__(self):
            pass

        def next(self, price: int) -> int:
            pass
    
    # 54
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pair = [(p, s) for p, s in zip(position, speed)]
        pair.sort(reverse=True)
        st = []
        for p, s in pair:
            time = (target - p) / s
            if not st or time > st[-1]:
                st.append(time)
        return len(st)
    
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
        st = []
        res = 0
        heights.append(-1)
        for i, h in enumerate(heights):
            start = i
            while st and h < st[-1][1]:
                idx, height = st.pop()
                res = max(res, height * (i-idx))
                start = idx
            st.append((start, h))
        return res
    
    # Input: heights = [7,1,7,2,2,4]
    
if __name__ == "__main__":
    s = Solution()
