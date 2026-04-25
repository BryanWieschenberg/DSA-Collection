from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(ospath.dirname(__file__))))
from typing import List, Dict
from Helper import Node, GraphHelper
from collections import defaultdict
from heapq import *


class Solution:
    # 244
    class Dijkstra:
        def __init__(self, adj: Dict[int, List[List[int, int]]]):
            pass

        def get_shortest_path(self, start: int, end: int) -> int:
            pass

    # 245
    class BellmanFord:
        def __init__(self, n: int, edges: List[List[int, int, int]]):
            pass

        def get_shortest_path(self, start: int) -> List[int]:
            pass

    # 246
    class Prim:
        def __init__(self, adj: Dict[int, List[List[int, int]]]):
            pass

        def get_mst(self) -> int:
            pass

    # 247
    class Kruskal:
        def __init__(self, n: int, edges: List[List[int, int, int]]):
            pass

        def get_mst(self) -> int:
            pass

    # 248
    class AStar:
        def __init__(self, adj: Dict[int, List[List[int, int]]]):
            pass

        def heuristic(self, u: int, v: int) -> int:
            pass

        def get_path(self, start: int, target: int) -> List[int]:
            pass

    # 249
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        pass

    # 250
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = [[] for _ in range(n+1)]
        for u, v, w in times:
            graph[u].append((v, w))
        h = [(0, k)]
        visit = set()
        res = 0
        while h:
            w1, n1 = heappop(h)
            if n1 in visit:
                continue
            visit.add(n1)
            res = max(res, w1)
            for n2, w2 in graph[n1]:
                if n2 in visit:
                    continue
                heappush(h, (w1 + w2, n2))
        return res if len(visit) == n else -1

    # 251
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        def dfs(u):
            while graph[u]:
                v = heappop(graph[u])
                dfs(v)
            res.append(u)

        graph = defaultdict(list)
        for u, v in tickets:
            heappush(graph[u], v)
        res = []
        dfs("JFK")
        return res[::-1]

    # 252
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        in_mst = [False] * n
        min_dist = [float('inf')] * n
        res = min_dist[0] = 0
        for _ in range(n):
            u = -1
            for i in range(n):
                if not in_mst[i] and (u == -1 or min_dist[i] < min_dist[u]):
                    u = i
            in_mst[u] = True
            res += min_dist[u]
            x1, y1 = points[u]
            for v in range(n):
                if in_mst[v]:
                    continue
                x2, y2 = points[v]
                dist = abs(x1 - x2) + abs(y1 - y2)
                min_dist[v] = min(min_dist[v], dist)
        return res

    # 253
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        h = [(grid[0][0], 0, 0)]
        visit = [[False] * n for _ in range(n)]
        while h:
            t, r, c = heappop(h)
            if visit[r][c]:
                continue
            visit[r][c] = True
            if r == n-1 and c == n-1:
                return t
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if 0 <= nr < n and 0 <= nc < n and not visit[nr][nc]:
                    nt = max(t, grid[nr][nc])
                    heappush(h, (nt, nr, nc))

    # 254
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start_node: int, end_node: int) -> float:
        pass

    # 255
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

        visit = {}
        res = []
        for c in graph:
            if dfs(c):
                return ""
        res.reverse()
        return "".join(res)

    # 256
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        INF = float('inf')
        dist = [INF] * n
        dist[src] = 0
        for _ in range(k+1):
            newDist = dist[:]
            for u, v, w in flights:
                if dist[u] != INF and dist[u] + w < newDist[v]:
                    newDist[v] = dist[u] + w
            dist = newDist
        return dist[dst] if dist[dst] != INF else -1

    # 257
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        pass

    # 258
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        pass

    # 259
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        pass

    # 260
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        pass


if __name__ == "__main__":
    s = Solution(); hg = GraphHelper()
