from collections import deque
from typing import List, Optional
from HELPER import Node, GraphHelper

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        def dfs(r, c, i):
            if i == len(word):
                return True

            if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] != word[i]:
                return False

            temp = board[r][c]
            board[r][c] = '#'

            found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in directions)

            board[r][c] = temp
            return found

        ROWS, COLS = len(board), len(board[0])
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0): return True

        return False

    def numIslands(self, grid: List[List[str]]) -> int:
        def dfs(r, c):
            if (
                r < 0 or c < 0 or
                r >= ROWS or c >= COLS or
                grid[r][c] == '0'
            ):
                return
            
            grid[r][c] = '0'
            for dr, dc in directions:
                dfs(r + dr, c + dc)
        
        ROWS, COLS = len(grid), len(grid[0])
        directions = ((1,0), (-1,0), (0,1), (0,-1))
        islands = 0

        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == '1':
                    dfs(r, c)
                    islands += 1
        
        return islands
    
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        def dfs(r, c):
            if (
                r < 0 or c < 0 or
                r >= ROWS or c >= COLS or
                not grid[r][c]
            ):
                return 0
            
            grid[r][c] = 0
            area = 0
            for dr, dc in directions:
                area += dfs(r + dr, c + dc)
            
            return area + 1
            
        ROWS, COLS = len(grid), len(grid[0])
        directions = ((1,0), (-1,0), (0,1), (0,-1))
        maxArea = 0

        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c]:
                    maxArea = max(maxArea, dfs(r, c))
        
        return maxArea

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        def dfs(node):
            if node.val in nodes:
                return nodes[node.val]
            new = Node(node.val)
            nodes[node.val] = new
            for neighbor in node.neighbors:
                new.neighbors.append(dfs(neighbor))
            return new

        nodes = {} # key: val, val: node
        return dfs(node) if node else None

    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        def addCell(r, c):
            if (
                min(r, c) < 0 or
                r >= ROWS or c >= COLS or
                (r, c) in visit or grid[r][c] == -1
            ):
                return
            visit.add((r, c))
            q.append((r, c))
                    
        ROWS, COLS = len(grid), len(grid[0])
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        visit = set()
        dist = 0
        q = deque()
        
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 0:
                    q.append((r, c))
                    visit.add((r, c))

        while q:
            for _ in range(len(q)):
                r, c = q.popleft()
                grid[r][c] = dist
                for dr, dc in directions:
                    addCell(r + dr, c + dc)
            dist += 1
        
        print(grid)

    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        ROWS, COLS = len(grid), len(grid[0])
        if grid[0][0] or grid[ROWS - 1][COLS - 1]:
            return -1

        directions = (
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        )

        q = deque([(0, 0, 1)]) # r, c, dist
        visited = set((0, 0))
        
        while q:
            r, c, dist = q.popleft()

            if r == ROWS - 1 and c == COLS - 1:
                return dist

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < ROWS and 0 <= nc < COLS and
                    grid[nr][nc] == 0 and
                    (nr, nc) not in visited
                ):
                    visited.add((nr, nc))
                    q.append((nr, nc, dist + 1))

        return -1

    def orangesRotting(self, grid: List[List[int]]) -> int:
        def exploreCell(r, c):
            if (
                min(r, c) < 0 or
                r >= ROWS or c >= COLS or
                (r, c) in visit or grid[r][c] != 1
            ):
                return
            
            nonlocal freshFruits
            freshFruits -= 1
            visit.add((r, c))
            q.append((r, c))
        
        minutes = 0
        freshFruits = 0
        ROWS, COLS = len(grid), len(grid[0])
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        visit = set()
        q = deque()

        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 1:
                    freshFruits += 1
                elif grid[r][c] == 2:
                    q.append((r, c))
                    visit.add((r, c))

        while q:
            for _ in range(len(q)):
                r, c = q.popleft()
                for dr, dc in directions:
                    exploreCell(r + dr, c + dc)
            if q: minutes += 1
        
        return minutes if freshFruits == 0 else -1
        
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        def dfs(r, c, visit, prevHeight):
            if (
                (r, c) in visit or
                min(r, c) < 0 or
                r >= ROWS or c >= COLS or
                heights[r][c] < prevHeight
            ):
                return
            
            visit.add((r, c))
            for dr, dc in directions:
                dfs(r + dr, c + dc, visit, heights[r][c])
        
        pacific, atlantic = set(), set()
        ROWS, COLS = len(heights), len(heights[0])
        directions = ((1,0),(-1,0),(0,1),(0,-1))
        
        for c in range(COLS):
            dfs(0, c, pacific, heights[0][c])
            dfs(ROWS - 1, c, atlantic, heights[ROWS - 1][c])
        for r in range(ROWS):
            dfs(r, 0, pacific, heights[r][0])
            dfs(r, COLS - 1, atlantic, heights[r][COLS - 1])
        
        return list(pacific & atlantic)
    
    def solve(self, board: List[List[str]]) -> None:
        def dfs(r, c):
            if (
                min(r, c) < 0 or
                r >= ROWS or c >= COLS or
                (r, c) in visit or
                board[r][c] == "X"
            ):
                return
            
            visit.add((r, c))
            for rd, cd in directions:
                dfs(r + rd, c + cd)

        directions = ((1,0),(-1,0),(0,1),(0,-1))
        ROWS, COLS = len(board), len(board[0])
        visit = set()

        for r in range(ROWS):
            dfs(r, 0)
            dfs(r, COLS - 1)
        for c in range(COLS):
            dfs(0, c)
            dfs(ROWS - 1, c)
        
        print(visit)
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == "O" and (r, c) not in visit:
                    board[r][c] == "X"
        
        print(board)

s = Solution()
h = GraphHelper()

# print( s. exist ( board=[
#     ["A","B","C","E"],
#     ["S","F","C","S"],
#     ["A","D","E","E"]
# ], word="ABCCED" )) # True

# print( s. numIslands ( grid=[
#     ["0","1","1","1","0"],
#     ["0","1","0","1","0"],
#     ["1","1","0","0","0"],
#     ["0","0","0","0","0"]
# ] )) # 1

# print( s. maxAreaOfIsland ( grid=[
#     [0,1,1,0,1],
#     [1,0,1,0,1],
#     [0,1,1,0,1],
#     [0,1,0,0,1]
# ] )) # 6

# h.printGraph(h.toGraph( adjList=[
#     [2,4],
#     [1,3],
#     [1,4],
#     [1,3]
# ] ))

# s. islandsAndTreasure ( grid=[
#     [2147483647,-1,0,2147483647],
#     [2147483647,2147483647,2147483647,-1],
#     [2147483647,-1,2147483647,-1],
#     [0,-1,2147483647,2147483647]
# ] ) # [
#     #     [3,-1,0,1],
#     #     [2,2,1,-1],
#     #     [1,-1,2,-1],
#     #     [0,-1,3,4]
#     # ]

# print( s. shortestPathBinaryMatrix ( grid=[
#     [0,1,0],
#     [1,0,0],
#     [1,1,0]
# ] )) # 3

# print( s. orangesRotting ( grid=[
#     [1,1,0],
#     [0,1,1],
#     [0,1,2]
# ] )) # 4

# print( s. pacificAtlantic ( heights=[
#   [4,2,7,3,4],
#   [7,4,6,4,7],
#   [6,3,5,3,6]
# ] )) # [[0,2],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0]]

s. solve ( board=[
  ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","O","O","X"],
  ["X","X","X","O"]
] ) # [
    #     ["X","X","X","X"],
    #     ["X","X","X","X"],
    #     ["X","X","X","X"],
    #     ["X","X","X","O"]
    # ]
