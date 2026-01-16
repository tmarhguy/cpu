#!/bin/bash
#
# ALU Test Runner Script
# Usage: ./run_tests.sh [options]
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                          ALU TEST RUNNER                                   ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print section headers
print_header() {
    echo -e "\n${YELLOW}=== $1 ===${NC}\n"
}

# Function to print success
print_success() {
    echo -e "${GREEN}[PASS] $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}[FAIL] $1${NC}"
}

# Parse arguments
MODE="${1:-quick}"

case "$MODE" in
    quick)
        print_header "Running Quick Tests (No Dependencies)"
        python3 test/test_alu.py
        ;;

    exhaustive)
        print_header "Running Exhaustive Vector Tests"
        echo -n "Starting in "
        for i in 3 2 1; do
            echo -n "$i... "
            sleep 1
        done
        echo ""
        python3 tools/run_tests.py --vectors-dir test/vectors --output-dir results
        ;;

    
    pytest)
        print_header "Running Tests with pytest"
        if command -v pytest &> /dev/null || command -v pytest3 &> /dev/null; then
            cd test && pytest test_alu.py -v
        else
            print_error "pytest not installed. Install with: pip3 install pytest"
            echo -e "${YELLOW}Falling back to quick mode...${NC}\n"
            python3 test/test_alu.py
        fi
        ;;
    
    verbose)
        print_header "Running Tests with Verbose Output"
        if command -v pytest &> /dev/null || command -v pytest3 &> /dev/null; then
            cd test && pytest test_alu.py -vv
        else
            print_error "pytest not installed. Install with: pip3 install pytest"
            echo -e "${YELLOW}Falling back to quick mode...${NC}\n"
            python3 test/test_alu.py
        fi
        ;;
    
    coverage)
        print_header "Running Tests with Coverage"
        if command -v pytest &> /dev/null || command -v pytest3 &> /dev/null; then
            cd test && pytest test_alu.py --cov --cov-report=term --cov-report=html
            print_success "Coverage report generated in test/htmlcov/index.html"
        else
            print_error "pytest and pytest-cov required. Install with:"
            echo "  pip3 install pytest pytest-cov"
            exit 1
        fi
        ;;
    
    install)
        print_header "Installing Test Dependencies"
        pip3 install -r test/requirements.txt
        print_success "Dependencies installed"
        ;;
    
    help|--help|-h)
        echo "Usage: ./run_tests.sh [mode]"
        echo ""
        echo "Modes:"
        echo "  quick       - Run tests without pytest (default, no dependencies)"
        echo "  exhaustive  - Run exhaustive JSON vector tests"
        echo "  pytest      - Run tests with pytest (requires pytest)"
        echo "  verbose   - Run tests with verbose output (requires pytest)"
        echo "  coverage  - Run tests with coverage report (requires pytest & pytest-cov)"
        echo "  install   - Install test dependencies"
        echo "  help      - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh              # Quick mode (no dependencies)"
        echo "  ./run_tests.sh pytest       # Standard pytest"
        echo "  ./run_tests.sh verbose      # Verbose output"
        echo "  ./run_tests.sh coverage     # With coverage report"
        echo ""
        ;;
    
    *)
        print_error "Unknown mode: $MODE"
        echo "Run './run_tests.sh help' for usage information"
        exit 1
        ;;
esac

exit 0
