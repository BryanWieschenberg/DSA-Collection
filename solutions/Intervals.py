from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from Helper import Interval, IntervalHelper

class Solution:
    # 221
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        res = []
        i, n = 0, len(intervals)
        while i < n and intervals[i][1] < newInterval[0]:
            res.append(intervals[i])
            i += 1
        s, e = newInterval
        while i < n and intervals[i][0] <= e:
            s = min(s, intervals[i][0])
            e = max(e, intervals[i][1])
            i += 1
        res.append([s, e])
        while i < n:
            res.append(intervals[i])
            i += 1
        return res

    # 222
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda i: i[0])
        i = 0
        res = []
        while i < len(intervals):
            s, e = intervals[i]
            while i < len(intervals) and intervals[i][0] <= e:
                s = min(s, intervals[i][0])
                e = max(e, intervals[i][1])
                i += 1
            res.append([s, e])
        return res
    
    # 223
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda i: (i[1], i[0]))
        prevEnd = intervals[0][1]
        res = 0
        for s, e in intervals[1:]:
            if s < prevEnd:
                res += 1
            else:
                prevEnd = e
        return res
    
    # 224
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        if not intervals:
            return True
        intervals.sort(key=lambda i: (i.start, i.end))
        e = intervals[0].end
        for i in range(1, len(intervals)):
            if intervals[i].start < e:
                return False
            e = intervals[i].end
        return True
    
    # 225
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        time = []
        for i in intervals:
            time.append((i.start, 1))
            time.append((i.end, -1))
        time.sort(key=lambda x: (x[0], x[1]))
        res = ct = 0
        for t in time:
            ct += t[1]
            res = max(res, ct)
        return res
        
    # 226
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        pass

    # 227
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        pass

if __name__ == "__main__":
    s = Solution(); hv = IntervalHelper()
