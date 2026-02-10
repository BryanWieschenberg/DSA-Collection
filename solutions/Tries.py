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
                curr = curr.children.setdefault(c, TrieNode())
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
                curr = curr.children.setdefault(c, TrieNode())
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
        def dfs(node, r, c):
            if (
                r < 0 or r >= R or
                c < 0 or c >= C or
                board[r][c] == '.' or
                board[r][c] not in node.children
            ):
                return
            char = board[r][c]
            nxt = node.children[char]
            if nxt.word is not None:
                res.append(nxt.word)
                nxt.word = None
            board[r][c] = '.'
            for dr, dc in dirs:
                dfs(nxt, r+dr, c+dc)
            board[r][c] = char
            if not nxt.children and nxt.word is None:
                del node.children[char]
        
        root = TrieNode()
        for w in words:
            curr = root
            for c in w:
                curr = curr.children.setdefault(c, TrieNode())
            curr.word = w
        R, C = len(board), len(board[0])
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        res = []
        for r in range(R):
            for c in range(C):
                dfs(root, r, c)
        return res

if __name__ == "__main__":
    s = Solution(); hi = TrieHelper()
