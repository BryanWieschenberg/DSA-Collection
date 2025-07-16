from utils import p, e
from typing import List

class Solution:
    # https://leetcode.com/problems/maximum-matching-of-players-with-trainers/description/?envType=daily-question&envId=2025-07-13
    # Time : O(n log n + m log m)
    # Space: O(1)
    def matchPlayersAndTrainers(self, players: List[int], trainers: List[int]) -> int:
        players.sort()
        trainers.sort()
        
        i = j = matches = 0
        
        while i < len(players) and j < len(trainers):
            if players[i] <= trainers[j]:
                matches += 1
                i += 1
                j += 1
            else:
                j += 1 # Trainer too weak, try next trainer
                
        return matches
    # https://leetcode.com/problems/find-the-maximum-length-of-valid-subsequence-i/description
    # Time : O(n)
    # Space: O(1)
    def maximumLength(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return len(nums)

        even_count = sum(1 for num in nums if num % 2 == 0)
        odd_count = len(nums) - even_count

        same_parity_max = max(even_count, odd_count)

        alt_even_first = 0
        expecting_even = True
        for num in nums:
            if (num % 2 == 0) == expecting_even:
                alt_even_first += 1
                expecting_even = not expecting_even

        alt_odd_first = 0
        expecting_odd = True
        for num in nums:
            if (num % 2 == 1) == expecting_odd:
                alt_odd_first += 1
                expecting_odd = not expecting_odd

        alternating_max = max(alt_even_first, alt_odd_first)

        return max(same_parity_max, alternating_max)
    
s = Solution()

# print(s.matchPlayersAndTrainers( [4,7,9], [8,2,5,8] ))

print(s.maximumLength( [1,2,1,1,2,1,2] ))
