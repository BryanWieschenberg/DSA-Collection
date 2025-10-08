class Solution:
    def factorial(self, n: int) -> int:
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)

    def fib(self, n: int) -> int:
        if n <= 1:
            return n
        return self.fib(n - 1) + self.fib(n - 2)

    def climbStairs(self, n: int) -> int:
        def helper(k):
            if k in cache:
                return cache[k]
            cache[k] = helper(k - 1) + helper(k - 2)
            return cache[k]

        cache = {1: 1, 2: 2}
        return helper(n)

s = Solution()

# print(s. factorial ( n=5 )) # 120

# print(s. fibbonacci ( n=8 )) # 21

# print(s. climbStairs ( n=8 )) # 34
