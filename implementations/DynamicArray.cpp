#include "DynamicArray.hpp"

DynamicArray::DynamicArray() : data(nullptr), size(0), capacity(0) {}

DynamicArray::~DynamicArray() {
    delete[] data;
}

void DynamicArray::resize(size_t new_capacity) {
    int* new_data = new int[new_capacity];
    for (size_t i = 0; i < size; i++)
        new_data[i] = data[i];
    
        delete[] data;
        data = new_data;
        capacity = new_capacity;
}

void DynamicArray::append(int value) {
    if (size == capacity) {
        size_t new_cap = (capacity == 0) ? 1 : capacity * 2;
        resize(new_cap);
    }
    data[size++] = value;
}

void DynamicArray::pop() {
    if (size > 0)
        size--;
}

int& DynamicArray::operator[](size_t index) {
    return data[index];
}

const int& DynamicArray::operator[](size_t index) const {
    return data[index];
}

size_t DynamicArray::get_size() const {
    return size;
}

size_t DynamicArray::get_capacity() const {
    return capacity;
}

void DynamicArray::print() const {

    std::cout << "[";
    for (size_t i = 0; i < size; i++) {
        std::cout << data[i];
        if (i < size - 1) std::cout << ", ";
    }
    std::cout << "]" << std::endl;
}