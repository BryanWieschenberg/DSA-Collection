from typing import List
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

s = Solution()

kthLargest = s.KthLargest(3, [1, 2, 3, 3])
print(kthLargest.add(4)) # 3
print(kthLargest.add(5)) # 3
print(kthLargest.add(1)) # 3
print(kthLargest.add(6)) # 4
print(kthLargest.add(2)) # 4
