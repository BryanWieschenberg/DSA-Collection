from HELPER import TrieNode, TrieHelper

class Solution:
    class PrefixTree:
        def __init__(self):
            pass

        def insert(self, word: str) -> None:
            pass

        def search(self, word: str) -> bool:
            pass

        def startsWith(self, prefix: str) -> bool:
            pass
        
s = Solution()
h = TrieHelper()

h.printTrie(h.toTrie(["balls", "abba", "babble", "breast", "abbington", "abuela"]))


# prefixTree = s.PrefixTree()
# prefixTree.insert("apple")
# print(prefixTree.search("apple")) # return True
# print(prefixTree.search("app")) # return False
# print(prefixTree.startsWith("app")) # return True
