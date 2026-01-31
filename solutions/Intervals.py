from sys import path; from os import path as ospath; path.append(ospath.dirname(ospath.dirname(__file__)))
from typing import List
from Helper import Interval, IntervalHelper

class Solution:
    # 221
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        pass

    # 222
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        pass

    # 223
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        pass

    # 224
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        pass

    # 225
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        pass
    
    # 226
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        pass

    # 227
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        pass

if __name__ == "__main__":
    s = Solution(); hv = IntervalHelper()
