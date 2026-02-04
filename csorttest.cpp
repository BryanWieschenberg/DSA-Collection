#include <iostream>
#include <chrono>
#include <cstdlib>
#include <random>

// Swap helper
static inline void swap(int &a, int &b) {
    int t = a;
    a = b;
    b = t;
}

// Partition (Lomuto)
int partition(int *a, int low, int high) {
    int pivot = a[high];
    int i = low - 1;

    for (int j = low; j < high; ++j) {
        if (a[j] <= pivot) {
            ++i;
            swap(a[i], a[j]);
        }
    }
    swap(a[i + 1], a[high]);
    return i + 1;
}

// Normal recursive quicksort
void quicksort(int *a, int low, int high) {
    if (low < high) {
        int p = partition(a, low, high);
        quicksort(a, low, p - 1);
        quicksort(a, p + 1, high);
    }
}

void shuffle(int *a, int n) {
    static std::mt19937 rng(std::random_device{}());
    for (int i = n - 1; i > 0; --i) {
        std::uniform_int_distribution<int> dist(0, i);
        int j = dist(rng);
        swap(a[i], a[j]);
    }
}

int main() {
    const int N = 1000000000; // 1 billion
    int *arr = new int[N];

    for (int i = 0; i < N; ++i) {
        arr[i] = i;
    }

    shuffle(arr, N);


    std::cout << "Clock starting..." << std::endl;
    auto start = std::chrono::high_resolution_clock::now();
    quicksort(arr, 0, N - 1);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Time: " << elapsed.count() << " seconds\n";

    delete[] arr;
    return 0;
}
