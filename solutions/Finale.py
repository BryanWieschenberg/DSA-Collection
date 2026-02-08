from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List, Optional, Tuple
from Helper import ListNode, ListHelper, TreeNode, TreeHelper, TrieNode, TrieHelper, Node, GraphHelper, Interval, IntervalHelper

class Solution:
    def shortestUniquelyBalancedSubarray(self, colors: List[int], c: int) -> List[int]:
        pass

    def bestMaskedRotation(self, s: str, t: str, mask: str) -> List[int]:
        pass

    def quotaReverseBlocks(self, head: Optional[ListNode], p: int) -> Optional[ListNode]:
        pass

    def nextHigherUnderCap(self, h: List[int], cap: List[int]) -> List[int]:
        pass
    
    def minPaletteChange(self, grid: List[str], start: Tuple[int, int], end: Tuple[int, int]) -> List[int]:
        pass

    def countRemovalsToBalance(self, root: Optional[TreeNode]) -> int:
        pass

    class RollerMedian:
        def __init__(self):
            pass

        def add(self, x: int) -> None:
            pass

        def discard(self, x: int) -> None:
            pass

        def median(self) -> Optional[int]:
            pass
    
    class PrefixOracle:
        def __init__(self, words: List[str], scores: List[str]):
            pass

        def best(self, prefix: str) -> str:
            pass

        def add(self, word: str, score: int) -> None:
            pass

        def remove(self, word: str) -> None:
            pass
    
    def firstRainbowComponent(self, n: int, colors: List[int], c: int, edges: List[Tuple[int, int]]) -> int:
        pass

    def minOddSpectrumPartition(self, s: str, k: int) -> int:
        pass

if __name__ == "__main__":
    s = Solution()
