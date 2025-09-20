from collections import Counter, defaultdict
import itertools
import math


# ---------------- ITERATION ----------------

# enumerate - adds a counter to an iterable and returns it as an enumerate object
# Time: O(n), Space: O(1)
nums = [10, 20, 30]
# for i, val in enumerate(nums):
    # print(i, val)  # 0 10 | 1 20 | 2 30

# zip
# Time: O(min(n, m)), Space: O(1)
a, b = [1, 2, 3], ['x', 'y', 'z']
# for x, y in zip(a, b):
    # print(x, y)  # 1 x | 2 y | 3 z

# reversed
# Time: O(n) iteration, Space: O(1)
# print(list(reversed(a)))  # [3, 2, 1]

# any / all
# Time: O(n) worst, Space: O(1)
# print(any([0, 0, 1]))  # True
# print(all([1, 2, 3]))  # True


# ---------------- LISTS ----------------

# sort
# Time: O(n log n), Space: O(n)
arr = [3, 1, 2]
arr.sort()
# print(arr)  # [1, 2, 3]

# slicing
# Time: O(k), Space: O(k)
# print(arr[::-1])  # [3, 2, 1]

# sum, max, min
# Time: O(n), Space: O(1)
# print(sum(arr), max(arr), min(arr))  # 6 3 1


# ---------------- DICTIONARIES ----------------

# get
# Time: O(1) average, Space: O(1)
d = {"a": 1, "b": 2}
# print(d.get("c", 0))  # 0

# items
# Time: O(n) iterate, Space: O(1)
# for k, v in d.items():
#     print(k, v)  # a 1 | b 2

# Counter
# Time: O(n), Space: O(k) where k = unique items
cnt = Counter("leetcode")
# print(cnt)  # Counter({'e': 3, 'l': 1, 't': 1, 'c': 1, 'o': 1, 'd': 1})

# defaultdict
# Time: O(1) avg access, Space: O(n)
dd = defaultdict(list)
dd["x"].append(1)
# print(dd)  # defaultdict(<class 'list'>, {'x': [1]})


# ---------------- SETS ----------------

s1, s2 = {1, 2, 3}, {2, 3, 4}
# print(s1 & s2)  # {2, 3}  (intersection)
# print(s1 | s2)  # {1, 2, 3, 4} (union)
# print(s1 - s2)  # {1} (difference)


# ---------------- MATH ----------------

# divmod
# Time: O(1), Space: O(1)
# print(divmod(7, 3))  # (2, 1)

# pow with mod
# Time: O(log y), Space: O(1)
# print(pow(2, 10, 1000))  # 24

# gcd/lcm
# Time: O(log(min(a, b))), Space: O(1)
# print(math.gcd(12, 18), math.lcm(12, 18))  # 6 36


# ---------------- ITERTOOLS ----------------

# permutations
# Time: O(nPr), Space: O(r)
# print(list(itertools.permutations([1, 2], 2)))  # [(1, 2), (2, 1)]

# combinations
# Time: O(nCr), Space: O(r)
# print(list(itertools.combinations([1, 2, 3], 2)))  # [(1, 2), (1, 3), (2, 3)]

# product
# Time: O(len(a)*len(b)), Space: O(1)
# print(list(itertools.product([1, 2], ['a', 'b']))) # [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]


# ---------------- STRINGS ----------------

# ord / chr
# Time: O(1), Space: O(1)
# print(ord('a'), chr(97))  # 97 a

# split / join
# Time: O(n), Space: O(n)
s = "a b c".split()
# print(s)  # ['a', 'b', 'c']
# print("".join(s))  # abc

# isalpha
# isdigit - 
# isdigit - 
# Time: O(n), Space: O(1)
# print("abc".isalpha(), "123".isdigit(), "abc123".isalnum())  # True True True
# print("abc!".isalpha(), "abc!".isdigit(), "abc 123".isalnum())  # False False False

# reverse string
# Time: O(n), Space: O(n)
# print("hello"[::-1])  # olleh


# ---------------- BINARY OPERATIONS ----------------

print(5 & 3)    # AND: 101 & 011 = 001 = 1
print(5 | 3)    # OR: 101 | 011 = 111 = 7
print(5 ^ 3)    # XOR: 101 ^ 011 = 110 = 6
print(~5)       # NOT: -(5+1) = -6
print(5 << 1)   # LEFT SHIFT: 101 << 1 = 1010 = 10
print(5 >> 1)   # RIGHT SHIFT: 101 >> 1 = 10 = 2
