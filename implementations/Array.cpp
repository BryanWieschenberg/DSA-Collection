#include <iostream>
#include "DynamicArray.hpp"

using namespace std;

int main() {
    int arr[5] = {1,2,3,4,5};

    cout << "Static array: [";
    for (int i = 0; i < 5; i++) {
        cout << arr[i];
        if (i < sizeof(arr) / sizeof(arr[0]) - 1) cout << ", ";
    }
    cout << "]" << endl;

    DynamicArray<std::string> dynarr(3, "hi");

    for (int i = 1; i <= 10; i++)
        dynarr.append(std::to_string(i));
    
    dynarr.print();
    cout << "Size: " << dynarr.get_size() <<
            ", Capacity: " << dynarr.get_capacity() << endl;

    dynarr.pop();
    dynarr.print();

    dynarr.append(std::to_string(50));
    dynarr.print();
    
    return 0;
}
