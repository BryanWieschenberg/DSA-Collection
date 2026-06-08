import random
from typing import List


class TestGen:
    class Solution:
        def hasDuplicate(self, nums: List[int]) -> bool:
            return len(set(nums)) != len(nums)

    def __init__(self):
        random.seed(42)
        self.MIN_VAL = -(10**9)
        self.MAX_VAL = 10**9
        self.MAX_LEN = 10**5

    def generate_uniform_random(self, size: int, force_duplicate: bool) -> List[int]:
        if not force_duplicate:
            return random.sample(range(self.MIN_VAL, self.MAX_VAL), size)
        else:
            nums = [random.randint(self.MIN_VAL, self.MAX_VAL) for _ in range(size)]
            if size > 1:
                idx1, idx2 = random.sample(range(size), 2)
                nums[idx2] = nums[idx1]
            return nums

    def generate_worst_case_unique(self) -> List[int]:
        start = random.randint(self.MIN_VAL, self.MAX_VAL - self.MAX_LEN)
        nums = list(range(start, start + self.MAX_LEN))
        random.shuffle(nums)
        return nums

    def generate_worst_case_late_duplicate(self) -> List[int]:
        nums = self.generate_worst_case_unique()
        nums[-1] = nums[0]
        return nums

    def generate_high_frequency(self) -> List[int]:
        size = random.randint(self.MAX_LEN // 2, self.MAX_LEN)
        target = random.randint(self.MIN_VAL, self.MAX_VAL)
        nums = [target] * size

        for _ in range(size // 10):
            idx = random.randint(0, size - 1)
            nums[idx] = random.randint(self.MIN_VAL, self.MAX_VAL)
        return nums

    def get_cases(self) -> List[List[int]]:
        test_cases = []
        for size in [10, 1000, 50000]:
            test_cases.append(self.generate_uniform_random(size, force_duplicate=True))
            test_cases.append(self.generate_uniform_random(size, force_duplicate=False))
        test_cases.append(self.generate_worst_case_unique())
        test_cases.append(self.generate_worst_case_late_duplicate())

        test_cases.append(self.generate_high_frequency())
        return test_cases
