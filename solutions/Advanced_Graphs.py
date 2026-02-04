from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from Helper import Node, GraphHelper
from collections import defaultdict

class Solution:
    # 164
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        pass

    # 165
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        pass

    # 166
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        pass

    # 167
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        pass

    # 168
    def swimInWater(self, grid: List[List[int]]) -> int:
        pass

    # 169
    def foreignDictionary(self, words: List[str]) -> str:
        def dfs(c):
            if c in visit:
                return visit[c]
            visit[c] = True
            for nei in graph[c]:
                if dfs(nei):
                    return True
            visit[c] = False
            res.append(c)
            return False

        graph = {c: set() for w in words for c in w}
        for i in range(len(words)-1):
            w1, w2 = words[i], words[i+1]
            minLen = min(len(w1), len(w2))
            if len(w1) > len(w2) and w1[:minLen] == w2[:minLen]:
                return ""
            for j in range(minLen):
                if w1[j] != w2[j]:
                    graph[w1[j]].add(w2[j])
                    break

        visit = {} # False = visited, True = in current path
        res = []
        for c in graph:
            if dfs(c):
                return ""
        res.reverse()
        return "".join(res)

    # 170
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        pass

    # 171
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        pass

    # 172
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        pass

    # 173
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        pass

if __name__ == "__main__":
    s = Solution(); hg = GraphHelper()
