from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from collections import defaultdict, deque
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
            self.q = None

        def push(self, x: int) -> None:
            self.q = deque([x, self.q])

        def pop(self) -> int:
            top = self.q.popleft()
            self.q = self.q.popleft()
            return top

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

        def pop(self) -> int:
            if not self.s2:
                while self.s1:
                    self.s2.append(self.s1.pop())
            return self.s2.pop()

        def peek(self) -> int:
            if not self.s2:
                while self.s1:
                    self.s2.append(self.s1.pop())
            return self.s2[-1]

        def empty(self) -> bool:
            return not (self.s1 or self.s2)

    # 49
    class MinStack:
        def __init__(self):
            self.s = []
            self.m = []

        def push(self, val: int) -> None:
            self.s.append(val)
            self.m.append(val if not self.m or val < self.m[-1] else self.m[-1])

        def pop(self) -> None:
            self.s.pop()
            self.m.pop()

        def top(self) -> int:
            return self.s[-1]        

        def getMin(self) -> int:
            return self.m[-1]

    # 50
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for t in tokens:
            if t == '+':
                tmp = stack.pop()
                op = stack.pop() + tmp
                stack.append(op)
            elif t == '-':
                tmp = stack.pop()
                op = stack.pop() - tmp
                stack.append(op)
            elif t == '*':
                tmp = stack.pop()
                op = stack.pop() * tmp
                stack.append(op)
            elif t == '/':
                tmp = stack.pop()
                op = int(stack.pop() / tmp)
                stack.append(op)
            else:
                stack.append(int(t))
        return stack[0]
    
    # 51
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []

        for a in asteroids:
            while stack and stack[-1] > 0 and a < 0:
                if stack[-1] < -a:
                    stack.pop()
                    continue
                elif stack[-1] == -a:
                    stack.pop()
                break
            else: # only enters if while ends without break
                stack.append(a)

        return stack

    # 52
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        s = []
        temp = temperatures
        n = len(temp)
        res = [0] * n
        for i in range(n):
            while s and temp[i] > temp[s[-1]]:
                idx = s.pop()
                res[idx] = i - idx
            s.append(i)
        return res
    
    # 53
    class StockSpanner:
        def __init__(self):
            self.s = []

        def next(self, price: int) -> int:
            span = 1
            while self.s and self.s[-1][0] <= price:
                i += self.s.pop()[1]
            self.s.append((price, i))
            return span
    
    # 54
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pair = sorted(zip(position, speed), reverse=True)
        stack = []
        for p, s in pair:
            time = (target - p) / s
            if not stack or time > stack[-1]:
                stack.append(time)
        return len(stack)
    
    # 55
    def simplifyPath(self, path: str) -> str:
        stack = []
        for p in path.split("/"):
            if p == '' or p == '.': continue
            elif p == '..':
                if stack: stack.pop()
            else:
                stack.append(p)
        return "/" + "/".join(stack)
    
    # 56
    def decodeString(self, s: str) -> str:
        sStr, sCt = [], []
        curr = ""
        k = 0
        for c in s:
            if c.isdigit():
                k = k * 10 + int(c)
            elif c == "[":
                sStr.append(curr)
                sCt.append(k)
                curr = ""
                k = 0
            elif c == "]":
                tmp = curr
                curr = sStr.pop()
                ct = sCt.pop()
                curr += tmp * ct
            else:
                curr += c
        return curr
    
    # 57
    class FreqStack:
        def __init__(self):
            self.freq = defaultdict(int)
            self.group = defaultdict(list)
            self.maxFreq = 0

        def push(self, val: int) -> None:
            self.freq[val] += 1
            f = self.freq[val]
            self.group[f].append(val)
            if f > self.maxFreq:
                self.maxFreq = f

        def pop(self) -> int:
            val = self.group[self.maxFreq].pop()
            self.freq[val] -= 1
            if not self.group[self.maxFreq]:
                self.maxFreq -= 1
            return val
    
    # 58
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []
        res = 0
        heights.append(0)
        for i in range(len(heights)):
            while stack and heights[stack[-1]] > heights[i]:
                height = heights[stack.pop()]
                left = stack[-1] if stack else -1
                width = i - left - 1
                res = max(res, height * width)
            stack.append(i)
        return res
    
if __name__ == "__main__":
    s = Solution()
