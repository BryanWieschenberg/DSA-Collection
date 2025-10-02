import time
from typing import List

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        for p in s:
            if p in ['[', '(', '{']:
                stack.append(p)
            elif stack and (
                (p == ']' and stack[-1] == '[') or
                (p == ')' and stack[-1] == '(') or
                (p == '}' and stack[-1] == '{')
            ):
                stack.pop()
            else:
                return False
        return True if not stack else False

    class MinStack:
        def __init__(self):
            self.stack = []
            self.minimum = []

        def push(self, val: int) -> None:
            if not self.stack:
                self.minimum.append(val)
                self.stack.append(val)
            else:
                self.stack.append(val)
                self.minimum.append(val if self.minimum[-1] > val else self.minimum[-1])

        def pop(self) -> None:
            self.stack.pop()
            self.minimum.pop()

        def top(self) -> int:
            return self.stack[-1]

        def getMin(self) -> int:
            return self.minimum[-1]

    def evalRPN(self, tokens: List[str]) -> int:
        if len(tokens) == 1:
            return int(tokens[0])
        elif len(tokens) < 3:
            return None

        operand1, operand2 = 0, 0
        stack = []

        for i in range(len(tokens)):
            print(stack)
            if not tokens[i] in ['+', '-', '*', '/']:
                stack.append(int(tokens[i]))
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
            
            op = tokens[i]

            match op:
                case '+': stack.append(operand1 + operand2)
                case '-': stack.append(operand1 - operand2)
                case '*': stack.append(operand1 * operand2)
                case '/': stack.append(int(operand1 / operand2))

        if len(stack) != 1:
            return None
        
        return stack[0]

    def generateParenthesis(self, n: int) -> List[str]:
        stack = []
        def backtrack(s, open_ct, close_ct):
            if len(s) == 2 * n:
                stack.append(s)
                return
            if open_ct < n:
                backtrack(s + '(', open_ct + 1, close_ct)
            if close_ct < open_ct:
                backtrack(s + ')', open_ct, close_ct + 1)
        
        backtrack("", 0, 0)
        return stack
    
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pair = [(p, s) for p, s in zip(position, speed)]
        stack = []
        fleets = 0
        for p, s in sorted(pair)[::-1]:
            time = (target - p) / s
            stack.append(time)

            if len(stack) >= 2 and time <= stack[-2]:
                stack.pop()
        return len(stack)
    
    def largestRectangleArea(self, heights: List[int]) -> int:
        maxArea = 0
        stack = []
        for i in range(len(heights)):
            start = i
            while stack and stack[-1][1] > heights[i]:
                index, height = stack.pop()
                maxArea = max(maxArea, height * (i - index))
                start = index
            stack.append((start, heights[i]))
        
        for i, h in stack:
            maxArea = max(maxArea, h * (len(heights) - i))
        
        return maxArea
        
s = Solution()

# print(s. isValid ( "([{}])" )) # True

# min_stack = s.MinStack()
# min_stack.push(1)
# min_stack.push(2)
# min_stack.push(0)
# print(min_stack.getMin()) # 0
# min_stack.pop()
# print(min_stack.getMin()) # 0
# print(min_stack.top()) # 1
# print(min_stack.getMin()) # 0

# print(s. evalRPN ( tokens=["10","6","9","3","+","-11","*","/","*","17","+","5","+"] )) // 22

# print(s. generateParenthesis ( n=3 )) # ["((()))","(()())","(())()","()(())","()()()"]

# print(s. carFleet ( target=10, position=[1,4], speed=[3,2] )) # 1

# print(s. largestRectangleArea ( heights=[7,1,7,2,2,4] )) # 8
