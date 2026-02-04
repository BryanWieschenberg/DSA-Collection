from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List, Optional
from Helper import Node, GraphHelper
from collections import deque, defaultdict

class Solution:
    # 143
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        pass

    # 144
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        pass

    # 145
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        pass

    # 146
    def numIslands(self, grid: List[List[str]]) -> int:
        def dfs(r, c):
            grid[r][c] = '0'
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < R and 0 <= nc < C and
                    grid[nr][nc] == '1'
                ):
                    dfs(nr, nc)
        
        R, C = len(grid), len(grid[0])
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        res = 0
        for r in range(R):
            for c in range(C):
                if grid[r][c] == '1':
                    dfs(r, c)
                    res += 1
        return res


    # 147
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        pass

    # 148
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        def dfs(node):
            if node in new:
                return new[node]
            copy = Node(node.val)
            new[node] = copy
            for nei in node.neighbors:
                copy.neighbors.append(dfs(nei))
            return copy
        
        new = {}
        return dfs(node) if node else None
    
    # 149
    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        pass

    # 150
    def orangesRotting(self, grid: List[List[int]]) -> int:
        pass

    # 151
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        def bfs(src, ocean):
            q = deque(src)
            while q:
                r, c = q.popleft()
                ocean[r][c] = True
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < R and 0 <= nc < C and
                        not ocean[nr][nc] and
                        heights[nr][nc] >= heights[r][c]
                    ):
                        q.append((nr, nc))

        R, C = len(heights), len(heights[0])
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        pacReachable = [[False] * C for _ in range(R)]
        atlReachable = [[False] * C for _ in range(R)]
        pacSrc, atlSrc = [], []

        for r in range(R):
            pacSrc.append((r, 0))
            atlSrc.append((r, C-1))
        for c in range(C):
            pacSrc.append((0, c))
            atlSrc.append((R-1, c))

        bfs(pacSrc, pacReachable)
        bfs(atlSrc, atlReachable)

        res = []
        for r in range(R):
            for c in range(C):
                if pacReachable[r][c] and atlReachable[r][c]:
                    res.append([r, c])
        return res
    
    # 152
    def solve(self, board: List[List[str]]) -> None:
        pass

    # 153
    def openLock(self, deadends: List[str], target: str) -> int:
        pass

    # 154
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        def dfs(u):
            if state[u] == 1:
                return False
            elif state[u] == 2:
                return True

            state[u] = 1
            for v in graph[u]:
                if not dfs(v):
                    return False
            state[u] = 2
            return True

        graph = defaultdict(list)
        for a, b in prerequisites:
            graph[b].append(a)

        # 0 = unvisited, 1 = visiting, 2 = visited
        state = [0] * numCourses

        for course in range(numCourses):
            if not dfs(course):
                return False
        return True
    
    # 155
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        pass

    # 156
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        def dfs(node, par):
            if node in visit:
                return False
            visit.add(node)
            for nei in graph[node]:
                if nei == par:
                    continue
                if not dfs(nei, node):
                    return False
            return True
        
        if len(edges) != n-1:
            return False
        
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        visit = set()
        return dfs(0, -1) and len(visit) == n
    
    # 157
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        pass

    # 158
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        def dfs(node):
            for nei in graph[node]:
                if not visit[nei]:
                    visit[nei] = True
                    dfs(nei)
                    
        graph = defaultdict(list)
        visit = [False] * n
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        res = 0
        for node in range(n):
            if not visit[node]:
                visit[node] = True
                dfs(node)
                res += 1
        return res

    # 159
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        pass

    # 160
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        pass

    # 161
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        pass

    # 162
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        pass

    # 163
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        pass

if __name__ == "__main__":
    s = Solution(); hg = GraphHelper()
