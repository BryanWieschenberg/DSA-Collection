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
            pass

        def addWord(self, word: str) -> None:
            pass

        def search(self, word: str) -> bool:
            pass

    # 141
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        pass

    # 142
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        pass

if __name__ == "__main__":
    s = Solution(); hi = TrieHelper()
