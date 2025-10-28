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

h.printGraph(h.toGraph( adjList=[
    [2,4],
    [1,3],
    [1,4],
    [1,3]
] ))
