import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            colors = ['blue'] * len(arr)
            colors[j], colors[j + 1] = 'green', 'green'
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr, colors
    yield arr, ['blue'] * len(arr)


def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            colors = ['blue'] * len(arr)
            colors[j], colors[j + 1] = 'green', 'green'
            yield arr, colors
            j -= 1
        arr[j + 1] = key
        yield arr, ['blue'] * len(arr)
    yield arr, ['blue'] * len(arr)


def merge_sort(arr, l=0, r=None):
    arr = arr.copy() if l == 0 else arr
    if r is None:
        r = len(arr) - 1

    if l < r:
        m = (l + r) // 2
        yield from merge_sort(arr, l, m)
        yield from merge_sort(arr, m + 1, r)
        yield from merge(arr, l, m, r)
    yield arr, ['blue'] * len(arr)


def merge(arr, l, m, r):
    left = arr[l:m + 1]
    right = arr[m + 1:r + 1]
    i = j = 0
    k = l

    while i < len(left) and j < len(right):
        colors = ['blue'] * len(arr)
        colors[k] = 'green'
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
        yield arr, colors

    while i < len(left):
        arr[k] = left[i]
        colors = ['blue'] * len(arr)
        colors[k] = 'green'
        i += 1
        k += 1
        yield arr, colors

    while j < len(right):
        arr[k] = right[j]
        colors = ['blue'] * len(arr)
        colors[k] = 'green'
        j += 1
        k += 1
        yield arr, colors


def quick_sort(arr, low=0, high=None):
    arr = arr.copy() if low == 0 else arr
    if high is None:
        high = len(arr) - 1

    def partition(low, high):
        pivot = arr[high]
        i = low
        for j in range(low, high):
            colors = ['blue'] * len(arr)
            colors[high] = 'red'
            colors[j] = 'green'
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                colors[i] = 'green'
                yield arr, colors
                i += 1
            yield arr, colors
        arr[i], arr[high] = arr[high], arr[i]
        yield arr, ['blue'] * len(arr)
        return i

    if low < high:
        gen = partition(low, high)
        for state in gen:
            yield state
        pivot_index = (low + high) // 2
        yield from quick_sort(arr, low, pivot_index - 1)
        yield from quick_sort(arr, pivot_index + 1, high)
    yield arr, ['blue'] * len(arr)

def visualize(sort_func, title="Sorting Visualization", size=50, speed=20):
    data = [random.randint(1, 100) for _ in range(size)]
    generator = sort_func(data)

    fig, ax = plt.subplots()
    bars = ax.bar(range(len(data)), data, align="edge")
    ax.set_xlim(0, size)
    ax.set_ylim(0, int(max(data) * 1.1))
    ax.set_title(title)
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    def update(frame):
        arr, colors = frame
        for bar, val, color in zip(bars, arr, colors):
            bar.set_height(val)
            bar.set_color(color)
        text.set_text(f"Ops: {update.cnt}")
        update.cnt += 1
        return (*bars, text)

    update.cnt = 0
    anim = animation.FuncAnimation(
        fig,
        func=update,
        frames=generator,
        interval=speed,
        repeat=False,
        blit=True
    )
    plt.show()

if __name__ == "__main__":
    visualize(bubble_sort, "Bubble Sort", size=50, speed=.5)
    # visualize(insertion_sort, "Insertion Sort", size=40, speed=20)
    # visualize(merge_sort, "Merge Sort", size=40, speed=20)
    # visualize(quick_sort, "Quick Sort", size=40, speed=20)
