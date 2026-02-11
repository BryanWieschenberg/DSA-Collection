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
        def dfs(r, c):
            if r < 0 or r >= R or c < 0 or c >= C or grid[r][c] == 0:
                return 0
            grid[r][c] = 0
            area = 0
            for dr, dc in dirs:
                area += dfs(r+dr, c+dc)
            return 1 + area

        res = 0
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        R, C = len(grid), len(grid[0])
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 1:
                    res = max(res, dfs(r, c))
        return res
    
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
        R, C = len(grid), len(grid[0])
        INF = 2**31-1
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        q = deque()
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 0:
                    q.append((r, c, 1))
        while q:
            r, c, dist = q.popleft()
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if nr < 0 or nr >= R or nc < 0 or nc >= C or grid[nr][nc] != INF:
                    continue
                grid[nr][nc] = dist
                q.append((nr, nc, dist+1))
        return grid

    # 150
    def orangesRotting(self, grid: List[List[int]]) -> int:
        res = fresh = 0
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        q = deque()
        R, C = len(grid), len(grid[0])
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 2:
                    q.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1
        while q and fresh > 0:
            qLen = len(q)
            res += 1
            for _ in range(qLen):
                r, c = q.popleft()
                for dr, dc in dirs:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                        fresh -= 1
                        q.append((nr, nc))
                        grid[nr][nc] = 2
        return res if fresh == 0 else -1

    # 151
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        def bfs(starts):
            visit = set(starts)
            q = deque(starts)
            while q:
                r, c = q.popleft()
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < R and 0 <= nc < C and
                        (nr, nc) not in visit and
                        heights[nr][nc] >= heights[r][c]
                    ):
                        visit.add((nr, nc))
                        q.append((nr, nc))
            return visit
        
        R, C = len(heights), len(heights[0])
        dirs = ((1,0), (-1,0), (0,1), (0,-1))
        pacific_starts = [(0, c) for c in range(C)] + [(r, 0) for r in range(R)]
        atlantic_starts = [(R-1, c) for c in range(C)] + [(r, C-1) for r in range(R)]
        pac = bfs(pacific_starts)
        atl = bfs(atlantic_starts)
        return [[r, c] for (r, c) in pac & atl]
    
    # 152
    def solve(self, board: List[List[str]]) -> None:
        R, C = len(board), len(board[0])
        dirs = ((1,0), (-1,0), (0,1), (0,-1))
        q = deque()
        for r in range(R):
            for c in [0, C-1]:
                if board[r][c] == 'O':
                    q.append((r, c))
        for c in range(C):
            for r in [0, R-1]:
                if board[r][c] == 'O':
                    q.append((r, c))
        while q:
            r, c = q.popleft()
            if board[r][c] != 'O':
                continue
            board[r][c] = '#'
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and board[nr][nc] == 'O':
                    q.append((nr, nc))
        for r in range(R):
            for c in range(C):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
                elif board[r][c] == '#':
                    board[r][c] = 'O'
        return board

    # 153
    def openLock(self, deadends: List[str], target: str) -> int:
        pass

    # 154
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for u, v in prerequisites:
            graph[v].append(u)
            indeg[u] += 1
        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        taken = 0
        while q:
            u = q.popleft()
            taken += 1
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return taken == numCourses
    
    # 155
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for u, v in prerequisites:
            graph[v].append(u)
            indeg[u] += 1
        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return order if len(order) == numCourses else []
    
    # 156
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[rb] = ra
            return True
        
        if len(edges) != n-1:
            return False
        parent = list(range(n))
        for u, v in edges:
            if not union(u, v):
                return False
        return True
    
    # 157
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        pass

    # 158
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(a, b):
            ar, br = find(a), find(b)
            if ar == br:
                return False
            nonlocal comps
            comps -= 1
            if rank[ar] < rank[br]:
                parent[ar] = br
            elif rank[ar] > rank[br]:
                parent[br] = ar
            else:
                parent[br] = ar
                rank[ar] += 1
            return True
        
        parent = list(range(n))
        rank = [0] * n
        comps = n
        for u, v in edges:
            union(u, v)
        return comps

    # 159
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(a, b):
            ar, br = find(a), find(b)
            if ar == br:
                return False
            if rank[ar] < rank[br]:
                parent[ar] = br
            elif rank[ar] > rank[br]:
                parent[br] = ar
            else:
                parent[br] = ar
                rank[ar] += 1
            return True
        
        n = len(edges)+1
        parent = list(range(n))
        rank = [0] * n
        res = []
        for u, v in edges:
            if not union(u, v):
                res = [u, v]
        return res
    
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
        def toCatchall(word, i):
            return word[:i] + '*' + word[i+1:]
        
        if endWord not in wordList:
            return 0
        wordList.append(beginWord)
        graph = defaultdict(list)
        for w in wordList:
            for i in range(len(w)):
                graph[toCatchall(w, i)].append(w)
        visit = set([beginWord])
        q = deque([beginWord])
        res = 0
        while q:
            qLen = len(q)
            res += 1
            for i in range(qLen):
                w = q.popleft()
                if w == endWord:
                    return res
                for j in range(len(w)):
                    pattern = toCatchall(w, j)
                    for nei in graph[pattern]:
                        if nei not in visit:
                            q.append(nei)
                            visit.add(nei)
                    graph[pattern] = []
        return 0

if __name__ == "__main__":
    s = Solution(); hg = GraphHelper()
