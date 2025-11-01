#ifndef DYNAMIC_ARRAY_HPP
#define DYNAMIC_ARRAY_HPP

#include <iostream>
#include <cstddef>

template <typename T>
class DynamicArray {
private:
    T* data;
    size_t _size;
    size_t capacity;

    void resize(size_t new_capacity);

public:
    DynamicArray();
    DynamicArray(size_t initial_size);
    DynamicArray(size_t initial_size, const T& value);
    ~DynamicArray();

    void append(const T& value);
    T pop();
    
    T& operator[](size_t index);
    const T& operator[](size_t index) const;
    T& at(size_t index);
    const T& at(size_t index) const;

    size_t size() const;
    void print() const;
};

#include "DynamicArray.tpp"

#endif
