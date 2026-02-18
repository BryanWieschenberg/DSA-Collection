from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from Helper import Interval, IntervalHelper
from heapq import *

class Solution:
    # 221
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        res = []
        ns, ne = newInterval
        for i, (s, e) in enumerate(intervals):
            if ne < s:
                res.append([ns, ne])
                return res + intervals[i:]
            elif ns > e:
                res.append([s, e])
            else:
                ns, ne = min(ns, s), max(ne, e)
        res.append([ns, ne])
        return res

    # 222
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()
        res = []
        ns, ne = intervals[0]
        for i, (s, e) in enumerate(intervals[1:]):
            if s > ne:
                res.append([ns, ne])
                ns, ne = s, e
            else:
                ne = max(ne, e)
        res.append([ns, ne])
        return res
    
    # 223
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda i: i[1])
        ne = intervals[0][1]
        res = 0
        for s, e in intervals[1:]:
            if ne > s:
                res += 1
            else:
                ne = e
        return res
    
    # 224
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        intervals.sort(key=lambda i: (i.start, i.end))
        for i in range(1, len(intervals)):
            if intervals[i-1].end > intervals[i].start:
                return False
        return True
        
    # 225
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        starts = sorted(i.start for i in intervals)
        ends = sorted(i.end for i in intervals)
        res = rooms = i = j = 0
        while i < len(starts):
            if starts[i] >= ends[j]:
                rooms -= 1
                j += 1
            rooms += 1
            res = max(res, rooms)
            i += 1
        return res
        
    # 226
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        pass

    # 227
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals.sort()
        h = []
        res = {}
        i = 0
        for q in sorted(queries):
            while i < len(intervals) and intervals[i][0] <= q:
                s, e = intervals[i]
                heappush(h, (e-s+1, e))
                i += 1
            while h and h[0][1] < q:
                heappop(h)
            res[q] = h[0][0] if h else -1
        return [res[q] for q in queries]
    
if __name__ == "__main__":
    s = Solution(); hv = IntervalHelper()
