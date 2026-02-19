from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import deque, defaultdict

class Solution:
    # 45
    def calPoints(self, operations: List[str]) -> int:
        st = []
        curr = 0
        for o in operations:
            if o == '+':
                new = st[-1] + st[-2]
                st.append(new)
                curr += new
            elif o == 'D':
                new = st[-1] * 2
                st.append(new)
                curr += new
            elif o == 'C':
                curr -= st.pop()
            else:
                new = int(o)
                st.append(new)
                curr += new
        return curr
        
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
            self.q = deque()

        def push(self, x: int) -> None:
            if not self.q:
                self.q.append(x)
                return
            self.q = deque([x, self.q])

        def pop(self) -> int:
            val = self.q.popleft()
            if self.q:
                self.q = self.q[0]
            return val

        def top(self) -> int:
            return self.q[0]

        def empty(self) -> bool:
            return not self.q

    # 48
    class MyQueue:
        def __init__(self):
            self.s1 = []
            self.s2 = []

        def push(self, x: int) -> None:
            self.s1.append(x)

        def _mov(self):
            if not self.s2:
                while self.s1:
                    self.s2.append(self.s1.pop())

        def pop(self) -> int:
            self._mov()
            return self.s2.pop()

        def peek(self) -> int:
            self._mov()
            return self.s2[-1]

        def empty(self) -> bool:
            return not (self.s1 or self.s2)

    # 49
    class MinStack:
        def __init__(self):
            self.st = []
            self.minst = []

        def push(self, val: int) -> None:
            self.st.append(val)
            if not self.minst or val <= self.minst[-1]:
                self.minst.append(val)
                return
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
        for tok in tokens:
            if tok == '+':
                st.append(st.pop() + st.pop())
            elif tok == '-':
                val2, val1 = st.pop(), st.pop()
                st.append(val1 - val2)
            elif tok == '*':
                st.append(st.pop() * st.pop())
            elif tok == '/':
                val2, val1 = st.pop(), st.pop()
                st.append(int(val1 / val2))
            else:
                st.append(int(tok))
        return st[0]
            
    # 51
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        st = []
        for a in asteroids:
            while st and st[-1] > 0 and a < 0:
                if abs(st[-1]) < abs(a):
                    st.pop()
                elif abs(st[-1]) > abs(a):
                    break
                elif abs(st[-1]) == abs(a):
                    st.pop()
                    break
            else:
                st.append(a)
        return st

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
            self.prices = []

        def next(self, price: int) -> int:
            res = 1
            while self.prices and price >= self.prices[-1][0]:
                res += self.prices[-1][1]
                self.prices.pop()
            self.prices.append((price, res))
            return res
        
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
        st = []
        for p in path.split('/'):
            if not p or p == '.':
                continue
            elif p == '..':
                if st: st.pop()
                continue
            else:
                st.append(p)
        return '/' + '/'.join(st)
        
    # 56
    def decodeString(self, s: str) -> str:
        def helper():
            res, k = "", 0
            nonlocal i
            while i < len(s):
                if s[i].isdigit():
                    k = k * 10 + int(s[i])
                elif s[i] == '[':
                    i += 1
                    res = res + k * helper()
                    k = 0
                elif s[i] == ']':
                    return res
                else:
                    res += s[i]
                i += 1
            return res

        i = 0
        return helper()
        
    # 57
    class FreqStack:
        def __init__(self):
            self.freq = defaultdict(int)
            self.stacks = defaultdict(list)
            self.maxFreq = 0

        def push(self, val: int) -> None:
            self.freq[val] += 1
            f = self.freq[val]
            self.stacks[f].append(val)
            self.maxFreq = max(self.maxFreq, f)

        def pop(self) -> int:
            res = self.stacks[self.maxFreq].pop()
            self.freq[res] -= 1
            if len(self.stacks[self.maxFreq]) == 0:
                self.maxFreq -= 1
            return res
    
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
        
if __name__ == "__main__":
    s = Solution()
