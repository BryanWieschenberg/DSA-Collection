TWO_SUM = {
    "id": 1,
    "slug": "two-sum",
    "title": "Two Sum",
    "difficulty": "Easy",
    "description": (
        'Given an array of integers <code>nums</code> and an integer '
        '<code>target</code>, return <em>indices of the two numbers such '
        'that they add up to <code>target</code></em>.\n\n'
        'You may assume that each input would have <strong>exactly one '
        'solution</strong>, and you may not use the same element twice.\n\n'
        'You can return the answer in any order.'
    ),
    "examples": [
        {
            "id": 1,
            "input": "nums = [2,7,11,15], target = 9",
            "output": "[0,1]",
            "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1].",
        },
        {
            "id": 2,
            "input": "nums = [3,2,4], target = 6",
            "output": "[1,2]",
            "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2].",
        },
    ],
    "constraints": [
        "<code>2 &lt;= nums.length &lt;= 10<sup>4</sup></code>",
        "<code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code>",
        "<code>-10<sup>9</sup> &lt;= target &lt;= 10<sup>9</sup></code>",
        "<strong>Only one valid answer exists.</strong>",
    ],
    "starter_code": (
        "class Solution:\n"
        "    def twoSum(self, nums: list[int], target: int) -> list[int]:\n"
        "        # Write your solution here\n"
        "        pass\n"
    ),
    # Each test case: the arguments to pass and the expected return value.
    # The runner will inject these into the user's code.
    "test_cases": [
        {"args": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]},
        {"args": {"nums": [3, 2, 4], "target": 6}, "expected": [1, 2]},
        {"args": {"nums": [3, 3], "target": 6}, "expected": [0, 1]},
    ],
    # Human-readable versions for display
    "test_cases_display": [
        {"input": "nums = [2,7,11,15], target = 9", "expected": "[0, 1]"},
        {"input": "nums = [3,2,4], target = 6", "expected": "[1, 2]"},
        {"input": "nums = [3,3], target = 6", "expected": "[0, 1]"},
    ],
}
