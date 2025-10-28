#include <iostream>
#include "DynamicArray.hpp"

using namespace std;

int main() {
    int arr[5] = {1,2,3,4,5};

    cout << "[";
    for (int i = 0; i < 5; i++) {
        cout << arr[i];
        if (i < sizeof(arr) / sizeof(arr[0]) - 1) cout << ", ";
    }
    cout << "]" << endl;

    DynamicArray dynarr;

    for (int i = 1; i <= 10; i++)
        dynarr.append(i);
    
    dynarr.print();
    cout << "Size: " << dynarr.get_size() <<
            ", Capacity: " << dynarr.get_capacity() << endl;

    dynarr.pop();
    dynarr.print();

    dynarr.append(50);
    dynarr.print();
    
    return 0;
}