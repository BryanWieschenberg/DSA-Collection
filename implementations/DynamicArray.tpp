#include "DynamicArray.hpp"

template <typename T>
DynamicArray<T>::DynamicArray() :
    data(nullptr), size(0), capacity(0) {}

template <typename T>
DynamicArray<T>::DynamicArray(size_t initial_size) :
    data(new T[initial_size]), size(initial_size), capacity(initial_size)
{
    for (size_t i = 0; i < size; ++i)
        data[i] = T();
}

template <typename T>
DynamicArray<T>::DynamicArray(size_t initial_size, const T& value) :
    data(new T[initial_size]), size(initial_size), capacity(initial_size)
{
    for (size_t i = 0; i < size; ++i)
        data[i] = value;
}

template <typename T>
DynamicArray<T>::~DynamicArray() {
    delete[] data;
}

template <typename T>
void DynamicArray<T>::resize(size_t new_capacity) {
    T* new_data = new T[new_capacity];
    for (size_t i = 0; i < size; i++)
        new_data[i] = data[i];

    delete[] data;
    data = new_data;
    capacity = new_capacity;
}

template <typename T>
void DynamicArray<T>::append(const T& value) {
    if (size == capacity) {
        size_t new_cap = (capacity == 0) ? 1 : capacity * 2;
        resize(new_cap);
    }
    data[size++] = value;
}

template <typename T>
T DynamicArray<T>::pop() {
    if (size == 0)
        throw std::out_of_range("Pop from empty array");
    return data[--size];
}

template <typename T>
T& DynamicArray<T>::operator[](size_t index) {
    return data[index];
}

template <typename T>
const T& DynamicArray<T>::operator[](size_t index) const {
    return data[index];
}

template <typename T>
size_t DynamicArray<T>::get_size() const {
    return size;
}

template <typename T>
size_t DynamicArray<T>::get_capacity() const {
    return capacity;
}

template <typename T>
void DynamicArray<T>::print() const {
    std::cout << "[";
    for (size_t i = 0; i < size; i++) {
        std::cout << data[i];
        if (i < size - 1) std::cout << ", ";
    }
    std::cout << "]" << std::endl;
}
