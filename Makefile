make all:
	@$(CXX) implementations/Array.cpp -o implementations/DynamicArray.cpp implementations/Array 2> /tmp/make_err.log || (cat /tmp/make_err.log; exit 1)
	@echo "Compiled all implementations"

array:
	@$(CXX) implementations/Array.cpp implementations/DynamicArray.cpp -o implementations/Array 2> /tmp/make_err.log || (cat /tmp/make_err.log; exit 1)
	@./implementations/Array

clean:
	@find implementations -type f -perm -111 ! -name "*.cpp" -delete
	@echo "Cleaned executables"
