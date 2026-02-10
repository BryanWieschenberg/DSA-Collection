from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from collections import defaultdict, deque, Counter
from heapq import *

class Solution:
    # 110
    class KthLargest:
        def __init__(self, k: int, nums: List[int]):
            self.h = []
            self.k = k
            for n in nums:
                self.add(n)

        def add(self, val: int) -> int:
            if len(self.h) < self.k:
                heappush(self.h, val)
            elif val > self.h[0]:
                heapreplace(self.h, val)
            return self.h[0]

    # 111
    def lastStoneWeight(self, stones: List[int]) -> int:
        stones = [-s for s in stones]
        heapify(stones)
        while len(stones) > 1:
            x = -heappop(stones)
            y = -heappop(stones)
            if x != y:
                heappush(stones, -(x - y))
        return -stones[0] if stones else 0
    
    # 112
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        h = []
        for x, y in points:
            dist = -(x**2 + y**2)
            heappush(h, (dist, x, y))
            if len(h) > k:
                heappop(h)
        return [[x, y] for _, x, y in h]
        return nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2) # Idiomatic alternative

    # 113
    def findKthLargest(self, nums: List[int], k: int) -> int:
        h = []
        for n in nums:
            if len(h) < k:
                heappush(h, n)
            elif n > h[0]:
                heapreplace(h, n)
        return h[0]

    # 114
    def leastInterval(self, tasks: List[str], n: int) -> int:
        cts = Counter(tasks)
        h = [-c for c in cts.values()]
        heapify(h)
        time = 0
        q = deque()
        while h or q:
            if h:
                time += 1
                ct = 1 + heappop(h)
                if ct: q.append((ct, time + n))
            else:
                time = q[0][1]
            if q and q[0][1] == time:
                heappush(h, q.popleft()[0])
        return time

    # 115
    class Twitter:
        def __init__(self):
            self.time = 0
            self.tweets = defaultdict(list) # userId: [(ct, tweetId), ..]
            self.followees = defaultdict(set) # userId: set(followeeId, ..)

        def postTweet(self, userId: int, tweetId: int) -> None:
            self.tweets[userId].append((self.time, tweetId))
            self.time += 1

        def getNewsFeed(self, userId: int) -> List[int]:
            h, res = [], []
            users = self.followees[userId] | {userId}
            for u in users:
                if self.tweets[u]:
                    tweets = self.tweets[u]
                    i = len(tweets)-1
                    time, tid = tweets[i]
                    heappush(h, (-time, tid, u, i-1))
            while h and len(res) < 10:
                _, tid, u, i = heappop(h)
                res.append(tid)
                if i >= 0:
                    time, tid = self.tweets[u][i]
                    heappush(h, (-time, tid, u, i-1))
            return res

        def follow(self, followerId: int, followeeId: int) -> None:
            self.followees[followerId].add(followeeId)

        def unfollow(self, followerId: int, followeeId: int) -> None:
            self.followees[followerId].discard(followeeId)

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
            self.lo = [] # max heap of lower half, always =len(h) or len(h)+1
            self.hi = [] # min heap of higher half

        def addNum(self, num: int) -> None:
            heappush(self.lo, -num)
            heappush(self.hi, -heappop(self.lo))
            if len(self.hi) > len(self.lo):
                heappush(self.lo, -heappop(self.hi))

        def findMedian(self) -> float:
            if len(self.lo) > len(self.hi):
                return -self.lo[0]
            return (-self.lo[0] + self.hi[0]) / 2
    
    # 121
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        pass

if __name__ == "__main__":
    s = Solution()
