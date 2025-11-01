#include <iostream>
#include "DynamicArray.hpp"

int main() {
    int arr[5] = {1,2,3,4,5};

    std::cout << "Static array: [";
    for (int i = 0; i < 5; i++) {
        std::cout << arr[i];
        if (i < sizeof(arr) / sizeof(arr[0]) - 1) std::cout << ", ";
    }
    std::cout << "]" << std::endl;

    DynamicArray<std::string> dynarr(3, "hi");

    for (int i = 1; i <= 10; i++)
        dynarr.append(std::to_string(i));
    
    dynarr.print();
    std::cout << "Size: " << dynarr.size() << std::endl;

    dynarr.pop();
    dynarr.print();

    dynarr.append("50");
    dynarr.print();
    
    return 0;
}
