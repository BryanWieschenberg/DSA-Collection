import random

class Sorter:
    @staticmethod
    def bubble(nums):
        for i in range(len(nums)-1):
            swapped = False
            for j in range(len(nums)-1-i):
                if nums[j] > nums[j+1]:
                    nums[j], nums[j+1] = nums[j+1], nums[j]
                    swapped = True
                yield j, j+1
            if not swapped: break

    @staticmethod
    def selection(nums):
        for i in range(len(nums)-1):
            minID = i
            for j in range(i+1, len(nums)):
                yield j, minID
                if nums[j] < nums[minID]:
                    minID = j
            if minID != i:
                nums[i], nums[minID] = nums[minID], nums[i]
                yield j, minID

    @staticmethod
    def insertion(nums):
        for i in range(1, len(nums)):
            key = nums[i]
            j = i - 1
            while j >= 0 and nums[j] > key:
                nums[j + 1] = nums[j]
                yield j, j + 1
                j -= 1
            nums[j + 1] = key
            yield j + 1, i

    @staticmethod
    def merge(nums):
        def sort(arr, left, right):
            if right - left <= 1:
                return
            mid = (left + right) // 2
            yield from sort(arr, left, mid)
            yield from sort(arr, mid, right)
            yield from merger(arr, left, mid, right)

        def merger(arr, left, mid, right):
            merged = []
            i, j = left, mid
            while i < mid and j < right:
                yield i, j
                if arr[i] <= arr[j]:
                    merged.append(arr[i])
                    i += 1
                else:
                    merged.append(arr[j])
                    j += 1
            merged.extend(arr[i:mid])
            merged.extend(arr[j:right])
            arr[left:right] = merged
            for k in range(left, right):
                yield k, k

        yield from sort(nums, 0, len(nums))

    @staticmethod
    def quick(nums):
        def partition(l, r):
            if l >= r:
                return
            pivot = nums[(l+r) // 2]
            i, j = l, r
            while i <= j:
                while nums[i] < pivot:
                    yield i, pivot
                    i += 1
                while nums[j] > pivot:
                    yield j, pivot
                    j -= 1
                if i <= j:
                    nums[i], nums[j] = nums[j], nums[i]
                    yield i, j, pivot
                    i += 1
                    j -= 1
            yield from partition(l, j)
            yield from partition(i, r)

        yield from partition(0, len(nums)-1)
        yield 0,

    @staticmethod
    def radix(nums):
        def counting(nums, exp):
            n = len(nums)
            output = [0] * n
            count = [0] * 10

            for i in range(n):
                index = (nums[i] // exp) % 10
                count[index] += 1
                yield i, i

            for i in range(1, 10):
                count[i] += count[i - 1]

            for i in range(n - 1, -1, -1):
                index = (nums[i] // exp) % 10
                output[count[index] - 1] = nums[i]
                count[index] -= 1
                yield i, count[index]

            for i in range(n):
                nums[i] = output[i]
                yield i, i
        if len(nums) == 0:
            return
        max_val = max(nums)
        exp = 1

        while max_val // exp > 0:
            yield from counting(nums, exp)
            exp *= 10

    @staticmethod
    def bogo(nums):
        def is_sorted(a): return all(a[i] <= a[i+1] for i in range(len(a)-1))

        while not is_sorted(nums):
            random.shuffle(nums)
            yield 0, len(nums) - 1
