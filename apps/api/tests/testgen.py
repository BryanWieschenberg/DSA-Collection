from random import randint, choice
from typing import List, Literal

Difficulty = Literal["Easy", "Medium", "Hard", "Extreme"]


class TestGen:
    class DynamicArray:
        def __init__(self, capacity: int):
            self.capacity = capacity
            self.length = 0
            self.arr = [0] * self.capacity

        def get(self, i: int) -> int:
            return self.arr[i]

        def set(self, i: int, val: int) -> None:
            self.arr[i] = val

        def pushback(self, val: int) -> None:
            if self.length == self.capacity:
                self.resize()
            self.arr[self.length] = val
            self.length += 1

        def popback(self) -> int:
            if self.length > 0:
                self.length -= 1
            return self.arr[self.length]

        def resize(self) -> None:
            self.capacity = 2 * self.capacity
            new_arr = [0] * self.capacity
            for i in range(self.length):
                new_arr[i] = self.arr[i]
            self.arr = new_arr

        def getSize(self) -> int:
            return self.length

        def getCapacity(self) -> int:
            return self.capacity

    def __init__(self):
        self.id = 4
        self.name = "Design Dynamic Array (Resizable Array)"
        self.difficulty: Difficulty = "Easy"
        self.code = "class DynamicArray:\n    def __init__(self, capacity: int):\n        \n\n    def get(self, i: int) -> int:\n        \n\n    def set(self, i: int, val: int) -> None:\n        \n\n    def pushback(self, val: int) -> None:\n        \n\n    def popback(self) -> int:\n        \n\n    def resize(self) -> None:\n        \n\n    def getSize(self) -> int:\n        \n\n    def getCapacity(self) -> int:\n        "
        self.description = "Design a resizable array class named `DynamicArray` to manage a list of integers dynamically.\n\nThe class should implement the following functionality:\n\n* `DynamicArray(capacity)` initializes the array with a starting capacity of `capacity` (always greater than zero).\n* `get(i)` retrieves the value at index `i`.\n* `set(i, val)` replaces the value at index `i` with `val`.\n* `pushback(val)` appends `val` to the end of the array, automatically doubling the capacity via `resize()` if the array is full.\n* `popback()` removes and returns the last element of the array.\n* `resize()` doubles the current capacity of the array, copying all existing elements over.\n* `getSize()` returns the current number of elements.\n* `getCapacity()` returns the total capacity of the array."
        self.constraints = [
            "`1 <= capacity <= 100`",
            "`-1000 <= val <= 1000`",
            "`0 <= i < size` for `get` and `set` calls.",
            "At most `5000` method calls in total."
        ]

    def get_public_cases(self) -> List[List]:
        return [
            [
                ["DynamicArray", [1]],
                ["pushback", [10]],
                ["getSize", []],
                ["getCapacity", []]
            ],
            [
                ["DynamicArray", [2]],
                ["pushback", [1]],
                ["pushback", [2]],
                ["pushback", [3]],
                ["getSize", []],
                ["getCapacity", []]
            ]
        ]

    def _generate_case(self, initial_capacity: int, num_ops: int) -> List:
        ops = [["DynamicArray", [initial_capacity]]]
        current_size = 0
        current_capacity = initial_capacity
        for _ in range(num_ops - 1):
            if current_size == 0:
                op = choice(["pushback", "getCapacity", "getSize"])
            else:
                op = choice(["pushback", "popback", "get", "set", "getSize", "getCapacity"])

            if op == "pushback":
                val = randint(-1000, 1000)
                ops.append(["pushback", [val]])
                if current_size == current_capacity:
                    current_capacity *= 2
                current_size += 1
            elif op == "popback":
                ops.append(["popback", []])
                current_size -= 1
            elif op == "get":
                idx = randint(0, current_size - 1)
                ops.append(["get", [idx]])
            elif op == "set":
                idx = randint(0, current_size - 1)
                val = randint(-1000, 1000)
                ops.append(["set", [idx, val]])
            elif op == "getSize":
                ops.append(["getSize", []])
            elif op == "getCapacity":
                ops.append(["getCapacity", []])
        return ops

    def get_private_cases(self) -> List[List]:
        cases = []
        cases.append(self._generate_case(1, 2))
        cases.append(self._generate_case(100, 2))
        cases.append(self._generate_case(1, 5000))
        cases.append(self._generate_case(100, 5000))
        cases.append(self._generate_case(5, 50))
        cases.append(self._generate_case(10, 100))
        cases.append(self._generate_case(50, 500))
        cases.append(self._generate_case(100, 1000))
        cases.append(self._generate_case(10, 1000))
        cases.append(self._generate_case(25, 2500))
        cases.append(self._generate_case(50, 4000))
        return cases
