#include <iostream>
#include <cstddef>
#include <queue>
#include <vector>
#include <DynamicArray.hpp>

template <typename T>
BinaryTree<T>::BinaryTree() : root(nullptr) {}

template <typename T>
TreeNode<T>* toTree(const T arr[], size_t size) {
    if (size == 0) return nullptr;
    root = new TreeNode<T>(arr[0]);

    std::queue<TreeNode<T>*> q;
    q.push(root);
    size_t i = 1;

    while (i < size && !q.empty()) {
        TreeNode<T>* curr = q.front();
        q.pop();

        if (i < size) curr->left = new TreeNode<T>(arr[i++]);
        if (i < size) curr->right = new TreeNode<T>(arr[i++]);

        if (curr->left) q.push(curr->left);
        if (curr->right) q.push(curr->right);
    }

    return root;
}

template <typename T>
TreeNode<T>* toTree(const std::vector<T>& vec) {
    if (vec.empty()) return nullptr;
    root = new TreeNode<T>(vec[0]);

    std::queue<TreeNode<T>*> q;
    q.push(root);
    size_t i = 1;

    while (i < vec.size() && !q.empty()) {
        TreeNode<T>* curr = q.front();
        q.pop();

        if (i < vec.size()) curr->left = new TreeNode<T>(vec[i++]);
        if (i < vec.size()) curr->right = new TreeNode<T>(vec[i++]);

        if (curr->left) q.push(curr->left);
        if (curr->right) q.push(curr->right);
    }

    return root;
}

template <typename T>
TreeNode<T>* toTree(const DynamicArray<T>& arr) {
    size_t n = arr.get_size();
    if (n == 0) return nullptr;
    root = new TreeNode<T>(arr[0]);

    std::queue<TreeNode<T>*> q;
    q.push(root);
    size_t i = 1;

    while (i < n && !q.empty()) {
        TreeNode<T>* curr = q.front();
        q.pop();

        if (i < n) curr->left = new TreeNode<T>(arr[i++]);
        if (i < n) curr->right = new TreeNode<T>(arr[i++]);

        if (curr->left) q.push(curr->left);
        if (curr->right) q.push(curr->right);
    }

    return root;
}

template <typename T>
void printTree(const TreeNode<T>* root) const {
    if (root == nullptr) return;

    printTree(root->left);
    std::cout << root->value << " ";
    printTree(root->right);
}
