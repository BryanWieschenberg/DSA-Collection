from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
import heapq

class Solution:
    # 110
    class KthLargest:
        def __init__(self, k: int, nums: List[int]):
            pass

        def add(self, val: int) -> int:
            pass

    # 111
    def lastStoneWeight(self, stones: List[int]) -> int:
        pass

    # 112
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        pass

    # 113
    def findKthLargest(self, nums: List[int], k: int) -> int:
        pass

    # 114
    def leastInterval(self, tasks: List[str], n: int) -> int:
        pass

    # 115
    class Twitter:
        def __init__(self):
            pass

        def postTweet(self, userId: int, tweetId: int) -> None:
            pass

        def getNewsFeed(self, userId: int) -> List[int]:
            pass

        def follow(self, followerId: int, followeeId: int) -> None:
            pass

        def unfollow(self, followerId: int, followeeId: int) -> None:
            pass

    # 116
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        pass

    # 117
    def reorganizeString(self, s: str) -> str:
        pass

    # 118
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        pass

    # 119
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        pass

    # 120
    class MedianFinder:
        def __init__(self):
            self.low = [] # max heap
            self.high = [] # min heap

        def addNum(self, num: int) -> None:
            heapq.heappush(self.low, -num)
            heapq.heappush(self.high, -heapq.heappop(self.low))
            if len(self.high) > len(self.low):
                heapq.heappush(self.low, -heapq.heappop(self.high))

        def findMedian(self) -> float:
            if len(self.low) > len(self.high):
                return -self.low[0]
            return (-self.low[0] + self.high[0]) / 2
    
    # 121
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        pass

if __name__ == "__main__":
    s = Solution()
