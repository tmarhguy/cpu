.PHONY: test test-verbose test-coverage test-quick install clean help

# Default target
help:
	@echo "ALU Test Makefile"
	@echo "================="
	@echo ""
	@echo "Available targets:"
	@echo "  make test          - Run all tests with pytest"
	@echo "  make test-verbose  - Run tests with verbose output"
	@echo "  make test-quick    - Run tests without pytest (faster)"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make install       - Install test dependencies"
	@echo "  make clean         - Clean test artifacts"
	@echo ""

# Install test dependencies
install:
	@echo "Installing test dependencies..."
	pip3 install -r test/requirements.txt
	@echo "Dependencies installed"

# Run tests with pytest (standard way)
test:
	@echo "Running ALU tests with pytest..."
	cd test && pytest test_alu.py -v --tb=short

# Run tests with verbose output
test-verbose:
	@echo "Running ALU tests with full output..."
	cd test && pytest test_alu.py -vv --tb=long

# Run tests without pytest (quick mode)
test-quick:
	@echo "Running ALU tests (quick mode)..."
	python3 test/test_alu.py

# Run tests with coverage
test-coverage:
	@echo "Running ALU tests with coverage..."
	cd test && pytest test_alu.py --cov --cov-report=html --cov-report=term

# Clean test artifacts
clean:
	@echo "Cleaning test artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned"
