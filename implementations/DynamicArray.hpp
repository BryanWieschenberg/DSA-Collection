#ifndef DYNAMIC_ARRAY_HPP
#define DYNAMIC_ARRAY_HPP

#include <iostream>
#include <cstddef>

class DynamicArray {
private:
    int* data;
    size_t size;
    size_t capacity;

    void resize(size_t new_capacity);

public:
    DynamicArray();
    ~DynamicArray();

    void append(int value);
    void pop();
    int& operator[](size_t index);
    const int& operator[](size_t index) const;

    size_t get_size() const;
    size_t get_capacity() const;
    void print() const;
};

#endif
