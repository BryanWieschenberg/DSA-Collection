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
        print(count)
        maxHeap = [-cnt for cnt in count.values()]
        heapq.heapify(maxHeap)
        print(maxHeap)
            
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

print( s. leastInterval ( tasks=["B","B","B","A","C"], n=3 )) # 4
