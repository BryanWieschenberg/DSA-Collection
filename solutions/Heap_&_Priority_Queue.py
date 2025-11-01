from collections import defaultdict, deque
from typing import Counter, List
import heapq

class Solution:
    class KthLargest:
        def __init__(self, k: int, nums: List[int]):
            self.minHeap = nums
            self.k = k
            heapq.heapify(self.minHeap)
            while len(self.minHeap) > k:
                heapq.heappop(self.minHeap)

        def add(self, val: int) -> int:
            heapq.heappush(self.minHeap, val)
            if len(self.minHeap) > self.k:
                heapq.heappop(self.minHeap)
            return self.minHeap[0]

    def lastStoneWeight(self, stones: List[int]) -> int:
        heap = [-stone for stone in stones]
        heapq.heapify(heap)
        while len(heap) >= 2:
            first = heapq.heappop(heap)
            second = heapq.heappop(heap)

            if first != second:
                heapq.heappush(heap, -abs(first - second))
        return -heap[0] if heap else 0
    
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []
        for x, y in points:
            dist = -(x ** 2 + y ** 2)
            heapq.heappush(heap, (dist, x, y))
            if len(heap) > k:
                heapq.heappop(heap)
        res = []
        for _ in range(k):
            _, x, y = heapq.heappop(heap)
            res.append([x, y])
        return res
    
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for i in range(len(nums)):
            heapq.heappush(heap, nums[i])
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]

    def leastInterval(self, tasks: List[str], n: int) -> int:
        count = Counter(tasks)
        maxHeap = [-cnt for cnt in count.values()]
        heapq.heapify(maxHeap)

        time = 0
        q = deque() # (-cnt, tilTilUseAgain)
        while maxHeap or q:
            time += 1
            if not maxHeap:
                time = q[0][1]
            else:
                cnt = heapq.heappop(maxHeap) + 1
                if cnt:
                    q.append((cnt, time + n))
            if q and q[0][1] == time:
                heapq.heappush(maxHeap, q.popleft()[0])
        return time

    class Twitter:
        def __init__(self):
            self.tweets = defaultdict(list) # userId -> [time, tweetId]
            self.following = defaultdict(set) # followerId -> followeeIds
            self.time = 0
            
        def postTweet(self, userId: int, tweetId: int) -> None:
            self.tweets[userId].append([self.time, tweetId])
            self.time -= 1

        def getNewsFeed(self, userId: int) -> List[int]:
            res = []
            heap = []
            users = self.following[userId] | {userId} # combines user followers with user
            
            for userId in users:
                for tweetData in self.tweets[userId][-10:]: # [-10:] retrieves 10 most recent
                    heapq.heappush(heap, tweetData)
            
            for _ in range(min(10, len(heap))):
                _, tweetId = heapq.heappop(heap)
                res.append(tweetId)
            
            return res

        def follow(self, followerId: int, followeeId: int) -> None:
            if followerId != followeeId:
                self.following[followerId].add(followeeId)

        def unfollow(self, followerId: int, followeeId: int) -> None:
            if followeeId in self.following[followerId]:
                self.following[followerId].remove(followeeId)

    class MedianFinder:
        def __init__(self):
            self.heapS = [] # maxheap all nums < heapL
            self.heapL = [] # minheap all nums > heapS

        def addNum(self, num: int) -> None:
            heapq.heappush(self.heapS, -num)

            if self.heapS and self.heapL and (-self.heapS[0] > self.heapL[0]):
                val = -heapq.heappop(self.heapS)
                heapq.heappush(self.heapL, val)

            if len(self.heapS) > len(self.heapL) + 1:
                val = -heapq.heappop(self.heapS)
                heapq.heappush(self.heapL, val)
            elif len(self.heapS) < len(self.heapL):
                val = heapq.heappop(self.heapL)
                heapq.heappush(self.heapS, -val)

        def findMedian(self) -> float:
            if len(self.heapS) > len(self.heapL):
                return -self.heapS[0]
            elif len(self.heapS) < len(self.heapL):
                return self.heapL[0]
            else:
                return (-self.heapS[0] + self.heapL[0]) / 2

s = Solution()

# kthLargest = s.KthLargest(3, [1, 2, 3, 3])
# print(kthLargest.add(4)) # 3
# print(kthLargest.add(5)) # 3
# print(kthLargest.add(1)) # 3
# print(kthLargest.add(6)) # 4
# print(kthLargest.add(2)) # 4

# print( s. lastStoneWeight ( stones=[2,3,6,2,4] )) # 1

# print( s. kClosest ( points=[[0,2],[2,2]], k=1 )) # [[0,2]]

# print( s. findKthLargest ( nums=[2,3,1,5,4], k=2 )) # 4

# print( s. leastInterval ( tasks=["B","B","B","A","C"], n=3 )) # 4

# twitter = s.Twitter()
# twitter.postTweet(1, 10)
# twitter.postTweet(2, 20)
# print(twitter.getNewsFeed(1)) # [10]
# print(twitter.getNewsFeed(2)) # [20]
# twitter.follow(1, 2)
# print(twitter.getNewsFeed(1)) # [20, 10]
# print(twitter.getNewsFeed(2)) # [20]
# twitter.unfollow(1, 2)
# print(twitter.getNewsFeed(1)) # [10]

# medianFinder = s.MedianFinder()
# medianFinder.addNum(1)
# print(medianFinder.findMedian()) # 1.0
# medianFinder.addNum(3)
# print(medianFinder.findMedian()) # 2.0
# medianFinder.addNum(2)
# print(medianFinder.findMedian()) # 2.0
