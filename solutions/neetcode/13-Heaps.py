from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(ospath.dirname(__file__))))
from typing import List, Optional
from collections import defaultdict, deque, Counter
from heapq import *


class Solution:
    # 184
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

    # 185
    def lastStoneWeight(self, stones: List[int]) -> int:
        stones = [-s for s in stones]
        heapify(stones)
        while len(stones) > 1:
            x = -heappop(stones)
            y = -heappop(stones)
            if x != y:
                heappush(stones, -(x - y))
        return -stones[0] if stones else 0
    
    # 186
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        h = []
        for x, y in points:
            dist = -(x**2 + y**2)
            heappush(h, (dist, x, y))
            if len(h) > k:
                heappop(h)
        return [[x, y] for _, x, y in h]
        return nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)

    # 187
    def findKthLargest(self, nums: List[int], k: int) -> int:
        h = []
        for n in nums:
            if len(h) < k:
                heappush(h, n)
            elif n > h[0]:
                heapreplace(h, n)
        return h[0]

    # 188
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

    # 189
    class MinHeap:
        def __init__(self):
            self.h = []

        def _get_parent(self, i):
            return (i-1) // 2
        
        def _get_left_child(self, i):
            return i*2 + 1
        
        def _get_right_child(self, i):
            return i*2 + 2

        def _sift_up(self, i):
            par = self._get_parent(i)
            if i > 0 and self.h[i] < self.h[par]:
                self.h[i], self.h[par] = self.h[par], self.h[i]
                self._sift_up(par)

        def _sift_down(self, i):
            smallest = i
            l = self._get_left_child(i)
            r = self._get_right_child(i)
            if l < len(self.h) and self.h[l] < self.h[smallest]:
                smallest = l
            if r < len(self.h) and self.h[r] < self.h[smallest]:
                smallest = r
            if smallest != i:
                self.h[i], self.h[smallest] = self.h[smallest], self.h[i]
                self._sift_down(smallest)

        def push(self, val: int) -> None:
            self.h.append(val)
            self._sift_up(len(self.h)-1)

        def pop(self) -> Optional[int]:
            if not self.h:
                return None
            if len(self.h) == 1:
                return self.h.pop()
            self.h[0], self.h[len(self.h)-1] = self.h[len(self.h)-1], self.h[0]
            root = self.h.pop()
            self._sift_down(0)
            return root

        def peek(self) -> Optional[int]:
            return self.h[0] if self.h else None

        def __len__(self) -> int:
            return len(self.h)

    # 190
    class Twitter:
        def __init__(self):
            self.time = 0
            self.tweets = defaultdict(list)
            self.followees = defaultdict(set)

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

    # 191
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        pass

    # 192
    def reorganizeString(self, s: str) -> str:
        pass

    # 193
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        pass

    # 194
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        pass

    # 195
    class MedianFinder:
        def __init__(self):
            self.lo = []
            self.hi = []

        def addNum(self, num: int) -> None:
            heappush(self.lo, -num)
            heappush(self.hi, -heappop(self.lo))
            if len(self.hi) > len(self.lo):
                heappush(self.lo, -heappop(self.hi))

        def findMedian(self) -> float:
            if len(self.lo) > len(self.hi):
                return -self.lo[0]
            return (-self.lo[0] + self.hi[0]) / 2
    
    # 196
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        pass


if __name__ == "__main__":
    s = Solution()
