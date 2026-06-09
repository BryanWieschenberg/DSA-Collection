import random
from typing import List, Literal

Difficulty = Literal["Easy", "Medium", "Hard", "Extreme"]


class TestGen:
    class Solution:
        @staticmethod
        def removeDuplicatesII(nums: List[int]) -> int:
            if len(nums) <= 2:
                return len(nums)
            k = 2
            for i in range(2, len(nums)):
                if nums[i] != nums[k - 2]:
                    nums[k] = nums[i]
                    k += 1
            return k

    def __init__(self):
        self.id: int = 43
        self.name: str = "Remove Duplicates from Sorted Array II"
        self.difficulty: Difficulty = "Medium"
        self.code: str = "removeDuplicatesII(nums: List[int]) -> int"
        self.description: str = "Remove duplicates in-place from a sorted integer array `nums` such that each unique element is allowed to appear at most two times. Return the number of elements `k` in the modified array."
        self.constraints: List[str] = [
            "`1 <= nums.length <= 3 * 10^4`",
            "`-10^4 <= nums[i] <= 10^4`",
            "`nums` is sorted in non-decreasing order."
        ]

    def _gen_fuzz(self, size: int, unique_ratio: float) -> List[int]:
        num_unique = max(1, int(size * unique_ratio))
        unique_vals = [random.randint(-10000, 10000) for _ in range(num_unique)]
        nums = [random.choice(unique_vals) for _ in range(size)]
        nums.sort()
        return nums

    def get_public_cases(self) -> List[List[int]]:
        return [
            [1, 1, 1, 2, 2, 3],
            [0, 0, 1, 1, 1, 1, 2, 3, 3]
        ]

    def get_private_cases(self) -> List[List[int]]:
        cases = [
            [1],
            [1, 1],
            [1, 1, 1],
            [1, 1, 1, 1],
            [1, 2, 3, 4, 5],
            [-10000] * 30000,
            list(range(-5000, 5000)) * 3,
            self._gen_fuzz(100, 0.1),
            self._gen_fuzz(1000, 0.5),
            self._gen_fuzz(30000, 0.01),
            self._gen_fuzz(30000, 0.8),
            sorted([random.randint(-10000, 10000) for _ in range(30000)])
        ]
        for i in range(len(cases)):
            cases[i].sort()
        return cases
