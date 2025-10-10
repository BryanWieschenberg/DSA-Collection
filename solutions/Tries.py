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
        
s = Solution()
h = TrieHelper()

h.printTrie(h.toTrie(["balls", "abba", "babble", "breast", "abbington", "abuela"]))

# prefixTree = s.PrefixTree()
# prefixTree.insert("apple")
# print(prefixTree.search("apple")) # return True
# print(prefixTree.search("app")) # return False
# print(prefixTree.startsWith("app")) # return True
