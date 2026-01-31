import random

class RealSorter:
    @staticmethod
    def selection(nums):
        n = len(nums)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if nums[j] < nums[min_idx]:
                    min_idx = j
            if min_idx != i:
                nums[i], nums[min_idx] = nums[min_idx], nums[i]

    @staticmethod
    def insertion(nums):
        for i in range(1, len(nums)):
            key = nums[i]
            j = i - 1
            while j >= 0 and nums[j] > key:
                nums[j + 1] = nums[j]
                j -= 1
            nums[j + 1] = key

    @staticmethod
    def bubble(nums):
        n = len(nums)
        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    swapped = True
            if not swapped:
                break

    @staticmethod
    def bogo(nums):
        def is_sorted(a):
            return all(a[i] <= a[i + 1] for i in range(len(a) - 1))
        while not is_sorted(nums):
            random.shuffle(nums)

    @staticmethod
    def merge(nums):
        n = len(nums)
        if n <= 1:
            return
        tmp = [0] * n
        def sort(left, right):
            if right - left <= 1:
                return
            mid = (left + right) // 2
            sort(left, mid)
            sort(mid, right)
            merge_range(left, mid, right)
        def merge_range(left, mid, right):
            i, j, k = left, mid, left
            while i < mid and j < right:
                if nums[i] <= nums[j]:
                    tmp[k] = nums[i]
                    i += 1
                else:
                    tmp[k] = nums[j]
                    j += 1
                k += 1
            while i < mid:
                tmp[k] = nums[i]
                i += 1
                k += 1
            while j < right:
                tmp[k] = nums[j]
                j += 1
                k += 1
            nums[left:right] = tmp[left:right]
        sort(0, n)

    @staticmethod
    def quick(nums):
        def _quick(lo, hi):
            if lo >= hi:
                return
            pivot = nums[hi]
            i = lo
            for j in range(lo, hi):
                if nums[j] < pivot:
                    if i != j:
                        nums[i], nums[j] = nums[j], nums[i]
                    i += 1
            if i != hi:
                nums[i], nums[hi] = nums[hi], nums[i]
            _quick(lo, i - 1)
            _quick(i + 1, hi)
        _quick(0, len(nums) - 1)

    @staticmethod
    def radix(nums):
        if not nums:
            return
        max_val = max(nums)
        exp = 1
        n = len(nums)
        out = [0] * n
        while max_val // exp > 0:
            count = [0] * 10
            for v in nums:
                count[(v // exp) % 10] += 1
            for i in range(1, 10):
                count[i] += count[i - 1]
            for i in range(n - 1, -1, -1):
                d = (nums[i] // exp) % 10
                count[d] -= 1
                out[count[d]] = nums[i]
            nums[:] = out
            exp *= 10

    @staticmethod
    def tim(nums):
        n = len(nums)
        MIN_RUN = 32
        MIN_GALLOP = 7
        def insertion_sort(left, right):
            for i in range(left + 1, right):
                key = nums[i]
                j = i - 1
                while j >= left and nums[j] > key:
                    nums[j + 1] = nums[j]
                    j -= 1
                nums[j + 1] = key
        def gallop_left(key, arr, start):
            step = 1
            idx = start
            while idx < len(arr) and arr[idx] <= key:
                idx += step
                step <<= 1
            lo = start
            hi = min(idx, len(arr))
            while lo < hi:
                mid = (lo + hi) // 2
                if arr[mid] <= key:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
        def gallop_right(key, arr, start):
            step = 1
            idx = start
            while idx < len(arr) and arr[idx] < key:
                idx += step
                step <<= 1
            lo = start
            hi = min(idx, len(arr))
            while lo < hi:
                mid = (lo + hi) // 2
                if arr[mid] < key:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
        def merge(left, mid, right):
            L = nums[left:mid]
            R = nums[mid:right]
            i = j = 0
            k = left
            winL = winR = 0
            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    nums[k] = L[i]
                    i += 1
                    winL += 1
                    winR = 0
                else:
                    nums[k] = R[j]
                    j += 1
                    winR += 1
                    winL = 0
                k += 1
                if winL >= MIN_GALLOP:
                    stop = gallop_left(R[j], L, i)
                    while i < stop:
                        nums[k] = L[i]
                        i += 1
                        k += 1
                    winL = 0
                elif winR >= MIN_GALLOP:
                    stop = gallop_right(L[i], R, j)
                    while j < stop:
                        nums[k] = R[j]
                        j += 1
                        k += 1
                    winR = 0
            while i < len(L):
                nums[k] = L[i]
                i += 1
                k += 1
            while j < len(R):
                nums[k] = R[j]
                j += 1
                k += 1
        for start in range(0, n, MIN_RUN):
            end = min(start + MIN_RUN, n)
            insertion_sort(start, end)
        size = MIN_RUN
        while size < n:
            for left in range(0, n, 2 * size):
                mid = min(left + size, n)
                right = min(left + 2 * size, n)
                if mid < right:
                    merge(left, mid, right)
            size *= 2

    @staticmethod
    def heap(nums):
        n = len(nums)
        if n <= 1:
            return
        def sift_down(start, end):
            root = start
            while True:
                child = 2 * root + 1
                if child > end:
                    return
                if child + 1 <= end and nums[child] < nums[child + 1]:
                    child += 1
                if nums[root] < nums[child]:
                    nums[root], nums[child] = nums[child], nums[root]
                    root = child
                else:
                    return
        for start in range(n // 2 - 1, -1, -1):
            sift_down(start, n - 1)
        for end in range(n - 1, 0, -1):
            nums[0], nums[end] = nums[end], nums[0]
            sift_down(0, end - 1)

    @staticmethod
    def bitonic(nums):
        n = len(nums)
        if n <= 1:
            return
        if n & (n - 1) != 0:
            raise ValueError("Bitonic sort requires array size to be a power of two")
        def compare_and_swap(i, j, direction):
            if (nums[i] > nums[j]) == direction:
                nums[i], nums[j] = nums[j], nums[i]
        def bitonic_merge(lo, cnt, direction):
            if cnt > 1:
                k = cnt // 2
                for i in range(lo, lo + k):
                    compare_and_swap(i, i + k, direction)
                bitonic_merge(lo, k, direction)
                bitonic_merge(lo + k, k, direction)
        def bitonic_sort(lo, cnt, direction):
            if cnt > 1:
                k = cnt // 2
                bitonic_sort(lo, k, True)
                bitonic_sort(lo + k, k, False)
                bitonic_merge(lo, cnt, direction)
        bitonic_sort(0, n, True)

    @staticmethod
    def comb(nums):
        n = len(nums)
        if n <= 1:
            return
        gap = n
        shrink = 1.3
        swapped = True
        while gap > 1 or swapped:
            gap = int(gap / shrink)
            if gap < 1:
                gap = 1
            swapped = False
            for i in range(0, n - gap):
                j = i + gap
                if nums[i] > nums[j]:
                    nums[i], nums[j] = nums[j], nums[i]
                    swapped = True

    @staticmethod
    def cycle(nums):
        n = len(nums)
        if n <= 1:
            return
        for cycle_start in range(n - 1):
            item = nums[cycle_start]
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if nums[i] < item:
                    pos += 1
            if pos == cycle_start:
                continue
            while item == nums[pos]:
                pos += 1
            nums[pos], item = item, nums[pos]
            while pos != cycle_start:
                pos = cycle_start
                for i in range(cycle_start + 1, n):
                    if nums[i] < item:
                        pos += 1
                while item == nums[pos]:
                    pos += 1
                nums[pos], item = item, nums[pos]

    @staticmethod
    def pancake(nums):
        n = len(nums)
        if n <= 1:
            return
        def flip(k):
            i, j = 0, k
            while i < j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1
        for size in range(n, 1, -1):
            max_idx = 0
            for i in range(1, size):
                if nums[i] > nums[max_idx]:
                    max_idx = i
            if max_idx != size - 1:
                if max_idx != 0:
                    flip(max_idx)
                flip(size - 1)

    @staticmethod
    def cocktail_shaker(nums):
        n = len(nums)
        if n <= 1:
            return
        start = 0
        end = n - 1
        swapped = True
        while swapped:
            swapped = False
            for i in range(start, end):
                if nums[i] > nums[i + 1]:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end, start, -1):
                if nums[i - 1] > nums[i]:
                    nums[i - 1], nums[i] = nums[i], nums[i - 1]
                    swapped = True
            start += 1

    @staticmethod
    def shell(nums):
        n = len(nums)
        if n <= 1:
            return
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = nums[i]
                j = i
                while j >= gap and nums[j - gap] > temp:
                    nums[j] = nums[j - gap]
                    j -= gap
                nums[j] = temp
            gap //= 2

    @staticmethod
    def gravity(nums):
        n = len(nums)
        if n <= 1:
            return
        max_val = max(nums)
        if max_val <= 0:
            return
        level_counts = [0] * max_val
        for v in nums:
            for h in range(v):
                level_counts[h] += 1
        nums[:] = [0] * n
        for col in range(n - 1, -1, -1):
            height = 0
            for h in range(max_val):
                if level_counts[h] > 0:
                    level_counts[h] -= 1
                    height += 1
            nums[col] = height

    @staticmethod
    def odd_even(nums):
        n = len(nums)
        if n <= 1:
            return
        sorted_flag = False
        while not sorted_flag:
            sorted_flag = True
            for i in range(0, n - 1, 2):
                if nums[i] > nums[i + 1]:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    sorted_flag = False
            for i in range(1, n - 1, 2):
                if nums[i] > nums[i + 1]:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    sorted_flag = False

    @staticmethod
    def flash(nums):
        n = len(nums)
        if n <= 1:
            return
        m = int(0.45 * n)
        if m < 2:
            return
        min_val = min(nums)
        max_val = max(nums)
        if min_val == max_val:
            return
        classes = [0] * m
        scale = (m - 1) / (max_val - min_val)
        for i in range(n):
            k = int(scale * (nums[i] - min_val))
            classes[k] += 1
        for i in range(1, m):
            classes[i] += classes[i - 1]
        move = 0
        j = 0
        k = m - 1
        while move < n:
            while j > classes[k] - 1:
                j += 1
                if j >= n:
                    break
                k = int(scale * (nums[j] - min_val))
            if j >= n:
                break
            flash_val = nums[j]
            while j != classes[k]:
                k = int(scale * (flash_val - min_val))
                classes[k] -= 1
                dst = classes[k]
                nums[dst], flash_val = flash_val, nums[dst]
                move += 1
        for i in range(1, n):
            key = nums[i]
            j = i - 1
            while j >= 0 and nums[j] > key:
                nums[j + 1] = nums[j]
                j -= 1
            nums[j + 1] = key

class VisualSorter:
    @staticmethod
    def selection(nums):
        n = len(nums)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if nums[j] < nums[min_idx]:
                    min_idx = j
                yield min_idx, j
            if min_idx != i:
                nums[i], nums[min_idx] = nums[min_idx], nums[i]
                yield i, min_idx

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
    def bogo(nums):
        def is_sorted(a):
            return all(a[i] <= a[i+1] for i in range(len(a)-1))
        while not is_sorted(nums):
            random.shuffle(nums)
            yield range(len(nums))

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
            for offset, val in enumerate(merged):
                idx = left + offset
                arr[idx] = val
                yield idx, idx
        yield from sort(nums, 0, len(nums))

    @staticmethod
    def quick(nums):
        def _quick(lo, hi):
            if lo >= hi:
                return
            pivot = nums[hi]
            i = lo
            for j in range(lo, hi):
                if nums[j] < pivot:
                    if i != j:
                        nums[i], nums[j] = nums[j], nums[i]
                        yield i, j
                    i += 1
            if i != hi:
                nums[i], nums[hi] = nums[hi], nums[i]
                yield i, hi
            yield from _quick(lo, i - 1)
            yield from _quick(i + 1, hi)
        if len(nums) > 1:
            yield from _quick(0, len(nums) - 1)

    @staticmethod
    def radix(nums):
        if not nums:
            return
        max_val = max(nums)
        exp = 1
        n = len(nums)
        while max_val // exp > 0:
            buckets = [[] for _ in range(10)]
            for i in range(n):
                digit = (nums[i] // exp) % 10
                buckets[digit].append(nums[i])
                yield i, i
            idx = 0
            for b in range(10):
                for val in buckets[b]:
                    nums[idx] = val
                    yield idx, idx
                    idx += 1
            exp *= 10

    @staticmethod
    def tim(nums):
        n = len(nums)
        MIN_RUN = 32
        MIN_GALLOP = 7
        def insertion_sort(left, right):
            for i in range(left + 1, right):
                key = nums[i]
                j = i - 1
                while j >= left and nums[j] > key:
                    nums[j + 1] = nums[j]
                    yield j + 1, j
                    j -= 1
                nums[j + 1] = key
                yield j + 1, j + 1
        def gallop_left(key, arr, start):
            step = 1
            idx = start
            while idx < len(arr) and arr[idx] <= key:
                idx += step
                step <<= 1
            lo = start
            hi = min(idx, len(arr))
            while lo < hi:
                mid = (lo + hi) // 2
                if arr[mid] <= key:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
        def gallop_right(key, arr, start):
            step = 1
            idx = start
            while idx < len(arr) and arr[idx] < key:
                idx += step
                step <<= 1
            lo = start
            hi = min(idx, len(arr))
            while lo < hi:
                mid = (lo + hi) // 2
                if arr[mid] < key:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
        def merge(left, mid, right):
            L = nums[left:mid]
            R = nums[mid:right]
            i = j = 0
            k = left
            winL = winR = 0
            while i < len(L) and j < len(R):
                yield left + i, mid + j
                if L[i] <= R[j]:
                    nums[k] = L[i]
                    i += 1
                    winL += 1
                    winR = 0
                else:
                    nums[k] = R[j]
                    j += 1
                    winR += 1
                    winL = 0
                yield k, k
                k += 1
                if winL >= MIN_GALLOP:
                    stop = gallop_left(R[j], L, i)
                    while i < stop:
                        nums[k] = L[i]
                        yield k, k
                        i += 1
                        k += 1
                    winL = 0
                elif winR >= MIN_GALLOP:
                    stop = gallop_right(L[i], R, j)
                    while j < stop:
                        nums[k] = R[j]
                        yield k, k
                        j += 1
                        k += 1
                    winR = 0
            while i < len(L):
                nums[k] = L[i]
                yield k, k
                i += 1
                k += 1
            while j < len(R):
                nums[k] = R[j]
                yield k, k
                j += 1
                k += 1
        for start in range(0, n, MIN_RUN):
            end = min(start + MIN_RUN, n)
            yield from insertion_sort(start, end)
        size = MIN_RUN
        while size < n:
            for left in range(0, n, 2 * size):
                mid = min(left + size, n)
                right = min(left + 2 * size, n)
                if mid < right:
                    yield from merge(left, mid, right)
            size *= 2

    @staticmethod
    def heap(nums):
        n = len(nums)
        if n <= 1:
            return
        def swap(i, j):
            nums[i], nums[j] = nums[j], nums[i]
            yield i, j
        def heapify(size, root):
            while True:
                largest = root
                left = 2 * root + 1
                right = 2 * root + 2
                if left < size and nums[left] > nums[largest]:
                    largest = left
                if right < size and nums[right] > nums[largest]:
                    largest = right
                if largest == root:
                    return
                yield from swap(root, largest)
                root = largest
        for i in range(n // 2 - 1, -1, -1):
            yield from heapify(n, i)
        for end in range(n - 1, 0, -1):
            yield from swap(0, end)
            yield from heapify(end, 0)

    @staticmethod
    def bitonic(nums):
        n = len(nums)
        if n & (n - 1) != 0:
            raise ValueError("Bitonic sort requires array size to be a power of two")
        def swap(i, j):
            nums[i], nums[j] = nums[j], nums[i]
            yield i, j
        def compare_and_swap(i, j, direction):
            if (nums[i] > nums[j]) == direction:
                yield from swap(i, j)
            else:
                yield i, j
        def bitonic_merge(lo, cnt, direction):
            if cnt > 1:
                k = cnt // 2
                for i in range(lo, lo + k):
                    yield from compare_and_swap(i, i + k, direction)
                yield from bitonic_merge(lo, k, direction)
                yield from bitonic_merge(lo + k, k, direction)
        def bitonic_sort(lo, cnt, direction):
            if cnt > 1:
                k = cnt // 2
                yield from bitonic_sort(lo, k, True)
                yield from bitonic_sort(lo + k, k, False)
                yield from bitonic_merge(lo, cnt, direction)
        yield from bitonic_sort(0, n, True)

    @staticmethod
    def comb(nums):
        n = len(nums)
        if n <= 1:
            return
        gap = n
        shrink = 1.3
        swapped = True
        while gap > 1 or swapped:
            gap = int(gap / shrink)
            if gap < 1:
                gap = 1
            swapped = False
            for i in range(n - gap):
                j = i + gap
                if nums[i] > nums[j]:
                    nums[i], nums[j] = nums[j], nums[i]
                    swapped = True
                    yield i, j
                else:
                    yield i, j

    @staticmethod
    def cycle(nums):
        n = len(nums)
        if n <= 1:
            return
        for cycle_start in range(n - 1):
            item = nums[cycle_start]
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if nums[i] < item:
                    pos += 1
                yield cycle_start, i
            if pos == cycle_start:
                continue
            while item == nums[pos]:
                pos += 1
            if pos != cycle_start:
                nums[pos], item = item, nums[pos]
                yield pos, cycle_start
            while pos != cycle_start:
                pos = cycle_start
                for i in range(cycle_start + 1, n):
                    if nums[i] < item:
                        pos += 1
                    yield cycle_start, i
                while item == nums[pos]:
                    pos += 1
                nums[pos], item = item, nums[pos]
                yield pos, cycle_start

    @staticmethod
    def pancake(nums):
        n = len(nums)
        if n <= 1:
            return
        def flip(k):
            i, j = 0, k
            while i < j:
                nums[i], nums[j] = nums[j], nums[i]
                yield i, j
                i += 1
                j -= 1
        for size in range(n, 1, -1):
            max_idx = 0
            for i in range(1, size):
                if nums[i] > nums[max_idx]:
                    max_idx = i
                yield max_idx, i
            if max_idx != 0:
                yield from flip(max_idx)
            yield from flip(size - 1)

    @staticmethod
    def cocktail_shaker(nums):
        n = len(nums)
        if n <= 1:
            return
        start = 0
        end = n - 1
        swapped = True
        while swapped:
            swapped = False
            for i in range(start, end):
                if nums[i] > nums[i + 1]:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    swapped = True
                    yield i, i + 1
                else:
                    yield i, i + 1
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end, start, -1):
                if nums[i - 1] > nums[i]:
                    nums[i - 1], nums[i] = nums[i], nums[i - 1]
                    swapped = True
                    yield i - 1, i
                else:
                    yield i - 1, i
            start += 1

    @staticmethod
    def shell(nums):
        n = len(nums)
        if n <= 1:
            return
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = nums[i]
                j = i
                while j >= gap and nums[j - gap] > temp:
                    nums[j] = nums[j - gap]
                    yield j, j - gap
                    j -= gap
                nums[j] = temp
                yield j, i
            gap //= 2

    @staticmethod
    def gravity(nums):
        n = len(nums)
        if n <= 1:
            return
        max_val = max(nums)
        level_counts = [0] * max_val
        for i in range(n):
            for h in range(nums[i]):
                level_counts[h] += 1
                yield i, i
        for i in range(n):
            nums[i] = 0
            yield i, i
        for col in range(n - 1, -1, -1):
            height = 0
            for h in range(max_val):
                if level_counts[h] > 0:
                    level_counts[h] -= 1
                    height += 1
                    nums[col] = height
                    yield col, col

    @staticmethod
    def odd_even(nums):
        n = len(nums)
        if n <= 1:
            return
        sorted_flag = False
        while not sorted_flag:
            sorted_flag = True
            for i in range(0, n - 1, 2):
                if nums[i] > nums[i + 1]:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    sorted_flag = False
                    yield i, i + 1
                else:
                    yield i, i + 1
            for i in range(1, n - 1, 2):
                if nums[i] > nums[i + 1]:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    sorted_flag = False
                    yield i, i + 1
                else:
                    yield i, i + 1

    @staticmethod
    def flash(nums):
        n = len(nums)
        if n <= 1:
            return
        m = int(0.45 * n)
        if m < 2:
            return
        min_val = min(nums)
        max_val = max(nums)
        if min_val == max_val:
            return
        classes = [0] * m
        for i in range(n):
            k = int((m - 1) * (nums[i] - min_val) / (max_val - min_val))
            classes[k] += 1
            yield i, i
        for i in range(1, m):
            classes[i] += classes[i - 1]
        move = 0
        j = 0
        k = m - 1
        while move < n:
            while j > classes[k] - 1:
                j += 1
                k = int((m - 1) * (nums[j] - min_val) / (max_val - min_val))
                yield j, j
            flash = nums[j]
            while j != classes[k]:
                k = int((m - 1) * (flash - min_val) / (max_val - min_val))
                classes[k] -= 1
                dst = classes[k]
                nums[dst], flash = flash, nums[dst]
                move += 1
                yield dst, j
        for i in range(1, n):
            key = nums[i]
            j = i - 1
            while j >= 0 and nums[j] > key:
                nums[j + 1] = nums[j]
                yield j + 1, j
                j -= 1
            nums[j + 1] = key
            yield j + 1, j + 1
