from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from Helper import TrieNode, TrieHelper

class Solution:
    # 139
    class PrefixTree:
        def __init__(self):
            self.root = TrieNode()

        def insert(self, word: str) -> None:
            curr = self.root
            for c in word:
                if c not in curr.children:
                    curr.children[c] = TrieNode()
                curr = curr.children[c]
            curr.end = True

        def search(self, word: str) -> bool:
            curr = self.root
            for c in word:
                if c not in curr.children:
                    return False
                curr = curr.children[c]
            return curr.end

        def startsWith(self, prefix: str) -> bool:
            curr = self.root
            for c in prefix:
                if c not in curr.children:
                    return False
                curr = curr.children[c]
            return True
    
    # 140
    class WordDictionary:
        def __init__(self):
            self.root = TrieNode()

        def addWord(self, word: str) -> None:
            curr = self.root
            for c in word:
                if c not in curr.children:
                    curr.children[c] = TrieNode()
                curr = curr.children[c]
            curr.end = True

        def search(self, word: str) -> bool:
            def dfs(i, node):
                if i == len(word):
                    return node.end
                if word[i] == '.':
                        return any(dfs(i+1, node.children[c]) for c in node.children)
                elif word[i] in node.children:
                    return dfs(i+1, node.children[word[i]])
                return False
            
            return dfs(0, self.root)
    
    # 141
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        pass

    # 142
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        def addWords():
            for w in words:
                node = root
                for c in w:
                    if c not in node.children:
                        node.children[c] = TrieNode()
                    node = node.children[c]
                node.word = w
        
        def dfs(r, c, node):
            char = board[r][c]
            if char not in node.children:
                return
            nxt = node.children[char]
            if nxt.word:
                res.append(nxt.word)
                nxt.word = None
            board[r][c] = '#'
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and board[nr][nc] != '#':
                    dfs(nr, nc, nxt)
            board[r][c] = char
            if not nxt.children:
                del node.children[char]

        root = TrieNode()
        addWords()
        R, C = len(board), len(board[0])
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        res = []
        for r in range(R):
            for c in range(C):
                dfs(r, c, root)
        return res

if __name__ == "__main__":
    s = Solution(); hi = TrieHelper()
