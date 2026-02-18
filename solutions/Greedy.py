from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import Counter

class Solution:
    # 207
    def lemonadeChange(self, bills: List[int]) -> bool:
        pass

    # 208
    def maxSubArray(self, nums: List[int]) -> int:
        res, curr = nums[0], 0
        for n in nums:
            curr = max(curr, 0) + n
            res = max(res, curr)
        return res

    # 209
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        pass

    # 210
    def maxTurbulenceSize(self, arr: List[int]) -> int:
        pass

    # 211
    def canJump(self, nums: List[int]) -> bool:
        goal = len(nums)-1
        for i in range(len(nums)-2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0
    
    # 212
    def jump(self, nums: List[int]) -> int:
        res = l = r = 0
        while r < len(nums)-1:
            furthest = 0
            for i in range(l, r+1):
                furthest = max(furthest, i + nums[i])
            l = r + 1
            r = furthest
            res += 1
        return res
    
    # 213
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        pass

    # 214
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        for i in range(len(gas)):
            if sum(gas) < sum(cost):
                return -1
            res = curr = 0
            for i in range(len(gas)):
                curr += gas[i] - cost[i]
                if curr < 0:
                    curr = 0
                    res = i + 1
            return res
        
    # 215
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        count = Counter(hand)
        keys = sorted(count.keys())
        for x in keys:
            freq = count[x]
            if freq > 0:
                for v in range(x, x + groupSize):
                    if count[v] < freq:
                        return False
                    count[v] -= freq
        return True
        
    # 216
    def predictPartyVictory(self, senate: str) -> str:
        pass
    
    # 217
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        X, Y, Z = target
        gotX = gotY = gotZ = False
        for a, b, c in triplets:
            if a > X or b > Y or c > Z:
                continue
            if a == X:
                gotX = True
            if b == Y:
                gotY = True
            if c == Z:
                gotZ = True
        return gotX and gotY and gotZ
    
    # 218
    def partitionLabels(self, s: str) -> List[int]:
        pass

    # 219
    def checkValidString(self, s: str) -> bool:
        pass

    # 220
    def candy(self, ratings: List[int]) -> int:
        pass

if __name__ == "__main__":
    s = Solution()
