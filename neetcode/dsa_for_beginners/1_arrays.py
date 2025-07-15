from typing import List

class Solution:
    # TC: O(n)
    # SC: O(n)
    # You can also just "return len(set(nums))", altho for this problem u also have to alter the array
    def removeDuplicates(self, nums: List[int]) -> int:
        dupes = set()
        uniquePtr = 0
        for i in range(len(nums)):
            if nums[i] in dupes:
                continue
            nums[uniquePtr] = nums[i]
            dupes.add(nums[i])
            uniquePtr += 1
        return uniquePtr

    # TC: O(n)
    # SC: O(1)
    def removeElement(self, nums: List[int], val: int) -> int:
        uniquePtr = 0
        for i in range(len(nums)):
            if nums[i] == val:
                continue
            nums[uniquePtr] = nums[i]
            uniquePtr += 1
        return uniquePtr

    # TC: O(n)
    # SC: O(2n)
    def getConcatenation(self, nums: List[int]) -> List[int]:
        numsLen = len(nums)
        concatNums = [0] * 2 * numsLen
        for i in range(numsLen):
            concatNums[i] = nums[i]
            concatNums[numsLen + i] = nums[i]
        return concatNums

    # TC: O(n)
    # SC: O(n)
    # lots of weird edge cases for this one, just make sure u continue if its a left char cuz if u don't, the big if will fail so it'll always be false
    def isValid(self, str: str) -> bool:
        stack = []
        for s in str:
            if s == '[' or s == '(' or s == '{':
                stack.append(s)
                continue
            if len(stack) == 0:
                return False
            if (s == ']' and stack[-1] == '[') or (s == ')' and stack[-1] == '(') or (s == '}' and stack[-1] == '{'):
                stack.pop()
            else:
                return False
        return not stack

    class MinStack:
        def __init__(self):
            self.stack = []

        def push(self, val: int) -> None:
            min = self.getMin()
            if min == None or val < min:
                min = val
            self.stack.append([val, min])

        def pop(self) -> None:
            self.stack.pop()

        def top(self) -> int:
            return self.stack[-1][0]

        def getMin(self) -> int:
            return self.stack[-1][1] if self.stack else None

s = Solution()

# print(s.removeDuplicates( [1,1,2,3,4] ))

# print(s.removeElement( [1,1,2,3,4], 1 ))

# print(s.getConcatenation( [1,4,1,2] ))

# print(s.isValid( ("()") ))

minStack = s.MinStack()
print( minStack.push(-2) )
print( minStack.push(0) )
print( minStack.push(-3) )
print( minStack.getMin() ) # -3
print( minStack.pop() )
print( minStack.top() ) # 0
print( minStack.getMin() ) # -2
