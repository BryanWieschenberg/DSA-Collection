from random import randint, sample, shuffle
from typing import List, Literal

Difficulty = Literal["Easy", "Medium", "Hard", "Extreme"]


class TestGen:
    class Solution:
        @staticmethod  # only make staticmethod if not a class implementation problem
        def hasDuplicate(nums: List[int]) -> bool:
            return len(set(nums)) != len(nums)

    def __init__(self):
        self.id: int = 2
        self.name: str = "Contains Duplicates"
        self.difficulty: Difficulty = "easy"
        self.code: str = "hasDuplicate(nums: List[int]) -> bool"
        self.description: str = "Given an integer list `nums`, return `True` if any value appears at least twice in the list, and return `False` if every element is distinct."
        self.constraints: List[str] = [
            "`1 <= nums.length <= 10^5`",
            "`-10^9 <= nums[i] <= 10^9`",
        ]

        # Constraints
        self.NUMS_MIN_LEN = 1
        self.NUMS_MAX_LEN = 10**5
        self.NUMS_MIN_VAL = -(10**9)
        self.NUMS_MAX_VAL = 10**9

        # OPTIONAL: custom TLE/MLE limits
        # self.time_limit = 1000
        # self.memory_limit = 128

    def _generate_uniform_random(self, size: int, force_duplicate: bool) -> List[int]:
        if not force_duplicate:
            return sample(range(self.NUMS_MIN_VAL, self.NUMS_MAX_VAL), size)
        else:
            nums = [randint(self.NUMS_MIN_VAL, self.NUMS_MAX_VAL) for _ in range(size)]
            if size > 1:
                idx1, idx2 = sample(range(size), 2)
                nums[idx2] = nums[idx1]
            return nums

    def _generate_worst_case_unique(self) -> List[int]:
        start = randint(self.NUMS_MIN_VAL, self.NUMS_MAX_VAL - self.NUMS_MAX_LEN)
        nums = list(range(start, start + self.NUMS_MAX_LEN))
        shuffle(nums)
        return nums

    def _generate_worst_case_late_duplicate(self) -> List[int]:
        nums = self._generate_worst_case_unique()
        nums[-1] = nums[0]
        return nums

    def _generate_high_frequency(self) -> List[int]:
        size = randint(self.NUMS_MAX_LEN // 2, self.NUMS_MAX_LEN)
        target = randint(self.NUMS_MIN_VAL, self.NUMS_MAX_VAL)
        nums = [target] * size
        for _ in range(size // 10):
            idx = randint(0, size - 1)
            nums[idx] = randint(self.NUMS_MIN_VAL, self.NUMS_MAX_VAL)
        return nums

    def get_public_cases(self) -> List[List[int]]:
        cases = []
        cases.append([1, 2, 3, 1])
        cases.append([1, 2, 3, 4])
        return cases

    def get_private_cases(self) -> List[List[int]]:
        cases = []
        for size in [10, 1000, 50000]:
            cases.append(self._generate_uniform_random(size, force_duplicate=True))
            cases.append(self._generate_uniform_random(size, force_duplicate=False))
        cases.append(self._generate_worst_case_unique())
        cases.append(self._generate_worst_case_late_duplicate())
        cases.append(self._generate_high_frequency())
        return cases
