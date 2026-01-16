# ALU Test Suite

> Industry-Standard Testing Framework for 8-bit ALU

---

## Quick Start

### Fastest Way (No Dependencies Required)

**Quick Test (1,900 tests):**
```bash
# From project root
./run_tests.sh

# Or
python3 test/test_alu.py

# Or
make test-quick
```

**Exhaustive Test (1,247,084 tests):**
```bash
# From project root
./run_tests.sh exhaustive
```

**Output (Exhaustive):**

```
Summary: 1247084 passed, 0 failed
Success Rate: 100.0%
Duration: 9.3 seconds

Per-operation: 65,636 tests × 19 operations = 1,247,084 total
```

**Output (Quick):**

```
Summary: 1900 passed, 0 failed
Success Rate: 100.0%
Duration: < 1 second

Per-operation: 100 tests × 19 operations = 1,900 total
```

---

## Test Methods

### Method 1: Shell Script (Recommended)

```bash
./run_tests.sh              # Quick mode: 1,900 tests (demo.json)
./run_tests.sh exhaustive   # Exhaustive mode: 1,247,084 tests (exhaustive.json)
./run_tests.sh pytest       # With pytest (requires install)
./run_tests.sh verbose      # Verbose output
./run_tests.sh coverage     # With coverage report
./run_tests.sh install      # Install dependencies
./run_tests.sh help         # Show help
```

### Method 2: Direct Python

```bash
# Quick test (1,900 tests from demo.json)
python3 test/test_alu.py

# Exhaustive test (1,247,084 tests from exhaustive.json)
python3 test/scripts/run_json_tests.py test/vectors/exhaustive.json
```

### Method 3: Makefile

```bash
make test-quick             # Quick mode
make test                   # With pytest
make test-verbose           # Verbose output
make test-coverage          # With coverage
make install                # Install dependencies
make clean                  # Clean artifacts
```

### Method 4: pytest (Advanced)

```bash
# Install first
pip3 install pytest

# Run all tests
cd test && pytest test_alu.py -v

# Run specific category
pytest test_alu.py::TestArithmetic -v

# Run specific test
pytest test_alu.py::TestArithmetic::test_add_simple -v
```

---

## Test Coverage

### 1,247,084 Exhaustive Tests

65,636 tests per operation × 19 operations:

| Opcode | Operation | Tests  | Status |
| ------ | --------- | ------ | ------ |
| 00000  | ADD       | 65,636 | Pass   |
| 00001  | SUB       | 65,636 | Pass   |
| 00010  | INC A     | 65,636 | Pass   |
| 00011  | DEC A     | 65,636 | Pass   |
| 00100  | LSL       | 65,636 | Pass   |
| 00101  | LSR       | 65,636 | Pass   |
| 00110  | ASR       | 65,636 | Pass   |
| 00111  | REV A     | 65,636 | Pass   |
| 01000  | NAND      | 65,636 | Pass   |
| 01001  | NOR       | 65,636 | Pass   |
| 01010  | XOR       | 65,636 | Pass   |
| 01011  | PASS A    | 65,636 | Pass   |
| 01100  | PASS B    | 65,636 | Pass   |
| 01101  | AND       | 65,636 | Pass   |
| 01110  | OR        | 65,636 | Pass   |
| 01111  | XNOR      | 65,636 | Pass   |
| 10000  | CMP       | 65,636 | Pass   |
| 10001  | NOT A     | 65,636 | Pass   |
| 10010  | NOT B     | 65,636 | Pass   |

### Manual Unit Tests

Organized by category:

- **TestArithmetic** - 6 tests (ADD, SUB, INC, DEC)
- **TestLogic** - 6 tests (AND, OR, XOR, NAND, NOR, XNOR)
- **TestShift** - 4 tests (LSL, LSR, ASR)
- **TestSpecial** - 6 tests (PASS, NOT, REV, CMP)
- **TestFlags** - 4 tests (Zero, Negative, Carry, Overflow)

**Total: 1,247,084 exhaustive tests + manual unit tests**

---

## Test Structure

```
test/
├── test_alu.py                 # Main test file (pytest-compatible)
├── vectors/                    # Test vector files
│   ├── demo.json              # 1,900 demonstration test vectors
│   ├── exhaustive.json        # 1,247,084 exhaustive test vectors (generated)
│   └── README.md              # Test vector documentation
├── scripts/                    # Test generation and execution scripts
│   ├── generate_exhaustive_tests.py  # Generate exhaustive test vectors
│   ├── run_json_tests.py      # Alternative JSON test runner
│   └── README.md              # Script documentation
├── cpp/                        # C++ Verilator testbench
│   ├── alu_tb.cpp             # C++ testbench implementation
│   ├── Makefile               # Build configuration
│   └── README.md              # C++ testbench documentation
├── requirements.txt           # Test dependencies (optional)
├── README.md                  # This file
├── TESTING_GUIDE.md           # Detailed testing guide
└── INDUSTRY_STANDARD_TESTING.md  # Industry testing approaches
```

**See also:**
- [Test Scripts](scripts/README.md) - Test generation and execution scripts
- [Test Vectors](vectors/README.md) - Test vector files and format
- [C++ Testbench](cpp/README.md) - Verilator-based hardware testbench

---

## 💻 Usage Examples

### Run All Tests

```bash
./run_tests.sh
# or
python3 test/test_alu.py
```

### Run with pytest

```bash
cd test
pytest test_alu.py -v
```

Output:

```
test_alu.py::test_load_vectors PASSED                              [  0%]
test_alu.py::test_alu_operation[ADD_TEST_001_A00_B00] PASSED      [  0%]
test_alu.py::test_alu_operation[ADD_TEST_002_A01_B5F] PASSED      [  0%]
...
test_alu.py::TestArithmetic::test_add_simple PASSED               [ 99%]
test_alu.py::TestFlags::test_overflow_flag PASSED                 [100%]

======================== 1925 passed in 2.45s ==========================
```

### Run Specific Operation

```bash
# Test only ADD operations
pytest test_alu.py -k "ADD_TEST" -v

# Test only arithmetic operations
pytest test_alu.py::TestArithmetic -v
```

### Run with Coverage

```bash
./run_tests.sh coverage
# or
cd test && pytest test_alu.py --cov --cov-report=html
```

### Stop on First Failure

```bash
cd test && pytest test_alu.py -x
```

---

## Installation

### No Installation Required (Quick Mode)

The tests run standalone without any dependencies:

```bash
python3 test/test_alu.py
```

### Optional: Install pytest for Advanced Features

```bash
# Install dependencies
pip3 install pytest

# Or use the installer
./run_tests.sh install
# or
make install
```

---

## ✅ What's Tested

### Operations

- ✅ All 19 ALU operations
- ✅ Edge cases (0x00, 0xFF, 0x7F, 0x80)
- ✅ Boundary values
- ✅ Random values
- ✅ Bit patterns

### Flags

- ✅ Carry flag (arithmetic overflow, shift operations)
- ✅ Zero flag (result is zero)
- ✅ Overflow flag (signed arithmetic overflow)
- ✅ Negative flag (MSB set)

### Correctness

- ✅ Result values
- ✅ Flag generation
- ✅ Edge case handling
- ✅ Bit-level accuracy

---

## Test Results

![Test Results](../media/testing/test_passed.png)
*All 1.24 million test vectors passing (65,636 tests × 19 operations)*

**Latest Run:**

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                   ALL 1,247,084 TESTS PASSED (100%)                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

Total Tests:  1,247,084 (exhaustive)
✅ Passed:    1,247,084 (100.0%)
❌ Failed:    0 (0.0%)
⏱️  Duration:  9.3 seconds

Per-operation: 65,636 tests × 19 operations
```

**Evidence:** Exhaustive test suite validates all operations across complete input space.

See test execution output above for detailed results.

---

## Troubleshooting

### "pytest not found"

**Solution:** Use quick mode (no dependencies):

```bash
python3 test/test_alu.py
```

Or install pytest:

```bash
pip3 install pytest
```

### "No module named 'pytest'"

**Solution:** The test file auto-detects and works without pytest:

```bash
python3 test/test_alu.py
```

### "Test vectors not found"

**Solution:** Make sure you're in the project root:

```bash
cd /path/to/alu-core
python3 test/test_alu.py
```

---

## 📚 Documentation

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive testing guide
- **[vectors/demo.json](vectors/demo.json)** - 1,900 test vectors

---

## For Developers

### Adding New Tests

```python
# test_alu.py

def test_my_new_operation():
    """Test description"""
    result, flags = alu.execute('00000', 5, 3)
    assert result == 8
    assert flags['zero'] == False
```

### Running Specific Tests

```bash
# Run one test
pytest test_alu.py::test_my_new_operation -v

# Run tests matching pattern
pytest test_alu.py -k "arithmetic" -v
```

### Debugging Failed Tests

```bash
# Show local variables
pytest test_alu.py -l

# Enter debugger on failure
pytest test_alu.py --pdb
```

---

## 🚀 CI/CD Integration

### GitHub Actions

```yaml
name: ALU Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: python3 test/test_alu.py
```

### GitLab CI

```yaml
test:
  script:
    - python3 test/test_alu.py
```

No dependencies required!

---

## Summary

**1.24M+ exhaustive tests**  
**100% pass rate**  
**9.3 second execution**  
**No dependencies required**  
**Multiple ways to run**  
**pytest compatible**  
**CI/CD ready**  
**Production ready**

**Start testing now:**

```bash
./run_tests.sh
```
