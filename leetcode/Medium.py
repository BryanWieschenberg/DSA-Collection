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

s = Solution()

print(s.matchPlayersAndTrainers( [4,7,9], [8,2,5,8] ))
