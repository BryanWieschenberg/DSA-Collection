from typing import List
from HELPER import TrieNode, TrieHelper

class Solution:
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
            def dfs(node, j):
                curr = node

                for i in range(j, len(word)):
                    c = word[i]
                    if c == '.':
                        for c in curr.children.values():
                            if dfs(c, i+1): return True
                        return False
                    else:
                        if c not in curr.children:
                            return False
                        curr = curr.children[c]
                        
                return curr.end

            return dfs(self.root, 0)

    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        def addWord(root, word):
            curr = root
            for w in word:
                if w not in curr.children:
                    curr.children[w] = TrieNode()
                curr = curr.children[w]
            curr.end = True

        def dfs(r, c, node, word):
            if (
                r < 0 or c < 0 or
                r >= ROWS or c >= COLS or
                board[r][c] not in node.children
            ):
                return
            
            temp = board[r][c]
            board[r][c] = '#'

            node = node.children[temp]
            word += temp
            if node.end: res.add(word)

            dfs(r-1, c, node, word)
            dfs(r+1, c, node, word)
            dfs(r, c-1, node, word)
            dfs(r, c+1, node, word)
            
            board[r][c] = temp

        root = TrieNode()
        for w in words:
            addWord(root, w)

        ROWS, COLS = len(board), len(board[0])
        res = set()

        for row in range(ROWS):
            for col in range(COLS):
                dfs(row, col, root, "")
        
        return list(res)

s = Solution()
h = TrieHelper()

# h.printTrie(h.toTrie(["apple", "app", "apricot"]))

# prefixTree = s.PrefixTree()
# prefixTree.insert("apple")
# print(prefixTree.search("apple")) # True
# print(prefixTree.search("app")) # False
# print(prefixTree.startsWith("app")) # True

# wordDictionary = s.WordDictionary()
# wordDictionary.addWord("bad")
# wordDictionary.addWord("dad")
# wordDictionary.addWord("mad")
# print(wordDictionary.search("pad")) # False
# print(wordDictionary.search("bad")) # True
# print(wordDictionary.search(".ad")) # True
# print(wordDictionary.search("b..")) # True

print( s. findWords ( board=[
    ["o","a","a","n"],
    ["e","t","a","e"],
    ["i","h","k","r"],
    ["i","f","l","v"]
], words=["oath","pea","eat","rain"] ))
