# Makefile for C++ ALU Testbench
# Industry-standard build system

CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wall -Wextra
TARGET = alu_tb
SRC = alu_tb.cpp

.PHONY: all clean test test-demo test-exhaustive help

all: $(TARGET)

$(TARGET): $(SRC)
	@echo "Compiling C++ testbench..."
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)
	@echo "✅ Build complete: ./$(TARGET)"

test: $(TARGET) test-demo

test-demo: $(TARGET)
	@echo ""
	@echo "Running quick test suite (1,900 tests)..."
	@echo "=========================================="
	./$(TARGET) ../vectors/demo.json

test-exhaustive: $(TARGET)
	@echo ""
	@echo "Running exhaustive test suite (722,944 tests)..."
	@echo "================================================="
	./$(TARGET) ../vectors/exhaustive.json

clean:
	@echo "Cleaning build artifacts..."
	rm -f $(TARGET)
	@echo "✅ Clean complete"

help:
	@echo "C++ ALU Testbench Makefile"
	@echo "=========================="
	@echo ""
	@echo "Targets:"
	@echo "  make          - Build the testbench"
	@echo "  make test     - Run quick tests (1,900 tests)"
	@echo "  make test-exhaustive - Run all tests (722,944 tests)"
	@echo "  make clean    - Remove build artifacts"
	@echo "  make help     - Show this help"
	@echo ""
	@echo "Usage:"
	@echo "  ./alu_tb [options] [test_file]"
	@echo "  ./alu_tb -v ../vectors/demo.json"
	@echo ""
