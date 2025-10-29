all:
	@$(CXX) $(CXXFLAGS) implementations/Array.cpp -o implementations/Array 2> /tmp/make_err.log || (cat /tmp/make_err.log; exit 1)
	@echo "Implementations successfully compiled"

array:
	@$(CXX) $(CXXFLAGS) implementations/Array.cpp -o implementations/Array 2> /tmp/make_err.log || (cat /tmp/make_err.log; exit 1)
	@./implementations/Array

clean:
	@rm -f implementations/Array
	@echo "Cleaned executables"
