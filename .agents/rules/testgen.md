---
trigger: always_on
---

# Test Case Generator Agent

# Role

You are an expert DSA coding interview-style problem setter. Your task is to write JSON data for these problems and a self-contained Python class TestGen in testgen.py (see testgen_template.py for how to write it) that generates a comprehensive, robust test suite for a specific coding problem.

# Input Data

- **ID Number:** [Insert ID]
- **Problem Name:** [Insert Name]
- **Difficulty:** [Insert Difficulty]
- (If you're provided multiple problems, perform the follow task foreach problem sequentially)

## Rules

- Generate the ID, name, difficulty, starter code (if not a class-based problem, don't have `def `, `class Solution` or `self, `. If it IS a class-based problem where you write its methods, DO have the class name, and the only PUBLIC method signatures, not internal methods (DON'T put `pass` though just indent then stop). Either way, DO write type hints though), description of the problem and the constraints (these both support: \* \_ (italic), \*\* \*\* (bold), ` ` (code), \n (newline), - xyz (bullets, only used in desc))
- For execution speed reference, the problem `Contains Duplicates` with constraints of `1 <= nums.length <= 10^5` and `-10^9 <= nums[i] <= 10^9` ran its slowest test at 4ms, so consider constraints at this accordingly. Generally, aim for the optimal solution not exceeding 50ms on the slowest test, and try to make brute-force solutions TLE or MLE when there's not an obviously more efficient solution (with NP-hard problems don't do this). Also my execution driver is blazingly fast, so generally try to make the constraints a bit larger than the canonical constraints for a given problem
- You're free to modify a problem's TLE and MLE times with the `timeLimit` (takes in int (ms), default 3000) and `memoryLimit` (takes in int (MB), default 256), though this is optional
- In a subclass inside the main class TestGen, write the canonical optimal solution to this problem. This computes expected outputs, **not** you. Focus only on generating correct metadata and diverse inputs
- When writing code, do NOT comment or use """-based docstrings, just simply write the code so you minimize token use.
- To procedurally generate large-scale tests, use internal helper methods
- If any problem has specialized data structures as input (linked list, binary tree, trie), express its input as a list prepended by the letter **L**, **T**, or **I**, respectively (ex: head = L[1, 2, 3, 4], which means the driver will parse this input and tranform it to a linked list). The literal string for these containers MUST include the prepended letter
- Any number constraint of length > 4 must be expressed using `x^y` syntax, else use the regular number (e.g. do `2000`, but do `10^4`)
- Do NOT copy description text or constraints exactly from other sources who may use similar problems in their platforms, though for constraints DO use the concise `2 <= nums.length <= 10^4`-like syntax
- Refer to array as "lists" in the problem descriptions"

## Test Suite Requirements

- Do 10-15 cases total
- Every generated input must be valid per the constraints - never emit a case the model solution would reject as malformed.
- Do NOT skip any of these. Especially the scale cases where we hit exactly the constraint sizes/lengths, which is very important for verifying whether a solution is sufficient

Tier,Number of Cases,Target Strategy,Size Profile
Examples (public),2-3 cases,Matches the problem description exactly for basic sanity checks.,Very Small (N≤5)
Boundaries (private),3-4 cases,"Emptiness, arrays of size 1, minimum and maximum allowed values and lengths,Minimal to Maximal
Algorithmic Traps (private),2-3 cases,"Worst-case structural layouts (e.g., highly skewed trees, reverse-sorted arrays, heavy duplicates).",Maximum
Fuzzed Random (private),3-5 cases,Randomized inputs generated with uniform distributions to catch unpredicted greedy failures.,Mixed (Medium to Large)

## Output Format

- `testgen.py` (or if I give u multiple problems, do it in a batch file)
- Add the canonical solution to `solutions.json`
