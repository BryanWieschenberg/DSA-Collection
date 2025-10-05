class Solution:
    def factorial(self, n: int) -> int:
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)

    def fibbonacci(self, n: int) -> int:
        if n <= 1:
            return n
        return self.fibbonacci(n - 1) + self.fibbonacci(n - 2)

    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        return self.climbStairs(n - 1) + self.climbStairs(n - 2)

s = Solution()

# print(s. factorial ( n=5 )) # 120

# print(s. fibbonacci ( n=8 )) # 21

# print(s. climbStairs ( n=8 )) # 34
