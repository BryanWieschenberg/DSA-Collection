#ifndef BINARY_TREE_HPP
#define BINARY_TREE_HPP

#include <cstddef>
#include <vector>
#include "DynamicArray.hpp"

template <typename T>
class TreeNode {
public:
    T value;
    TreeNode* left;
    TreeNode* right;

    TreeNode(const T& val) :
        value(val), left(nullptr), right(nullptr) {}
};

template <typename T>
class BinaryTree {
private:
    TreeNode<T>* root;

public:
    BinaryTree() : root(nullptr) {}

    TreeNode<T>* toTree(const T arr[], size_t size);
    TreeNode<T>* toTree(const std::vector<T>& vec);
    TreeNode<T>* toTree(const DynamicArray<T>& arr);

    void printTree(const TreeNode<T>* node) const;
};

#include "BinaryTree.tpp"
#endif
