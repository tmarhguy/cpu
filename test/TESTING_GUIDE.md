# ALU Testing Guide

**Standard Testing Framework for 8-bit ALU**

This directory contains industry-standard tests using pytest, compatible with CI/CD pipelines.

---

## Quick Start

### Option 1: Using Makefile (Recommended)

```bash
# Install dependencies
make install

# Run tests
make test

# Run with more detail
make test-verbose

# Quick test without pytest
make test-quick
```

### Option 2: Direct pytest

```bash
# Install pytest
pip3 install pytest

# Run all tests
cd test
pytest test_alu.py -v

# Run specific test class
pytest test_alu.py::TestArithmetic -v

# Run specific test
pytest test_alu.py::TestArithmetic::test_add_simple -v
```

### Option 3: Standalone Python

```bash
# No dependencies required
python3 test/test_alu.py
```

---

## Test Structure

### Test File: `test_alu.py`

- **1,900 parametrized tests** from `vectors/demo.json`
- **Manual unit tests** organized by operation type
- **Pytest compatible** with industry standards
- **Standalone capable** (can run without pytest)

### Test Organization

```
test/
├── test_alu.py           # Main test file (pytest compatible)
├── vectors/
│   └── demo.json         # 1,900 test vectors
├── requirements.txt      # Test dependencies
├── TESTING_GUIDE.md     # This file
```

---

## Running Tests

### All Tests

```bash
# Standard pytest run
pytest test_alu.py -v

# Output:
# test_alu.py::test_load_vectors PASSED
# test_alu.py::test_alu_operation[ADD_TEST_001_A00_B00] PASSED
# test_alu.py::test_alu_operation[ADD_TEST_002_A01_B5F] PASSED
# ... (1900 tests)
# test_alu.py::TestArithmetic::test_add_simple PASSED
# ... (manual tests)
```

### By Operation Category

```bash
# Arithmetic operations only
pytest test_alu.py::TestArithmetic -v

# Logic operations only
pytest test_alu.py::TestLogic -v

# Shift operations only
pytest test_alu.py::TestShift -v

# Special operations only
pytest test_alu.py::TestSpecial -v

# Flag tests only
pytest test_alu.py::TestFlags -v
```

### Specific Tests

```bash
# Test a specific operation
pytest test_alu.py -k "test_add" -v

# Test all ADD operations
pytest test_alu.py -k "ADD_TEST" -v

# Test a specific test case
pytest test_alu.py::test_alu_operation[ADD_TEST_001_A00_B00] -v
```

### With Coverage

```bash
# Run with coverage report
pytest test_alu.py --cov --cov-report=html --cov-report=term

# View coverage in browser
open htmlcov/index.html
```

### Stop on First Failure

```bash
# Stop at first failure for debugging
pytest test_alu.py -x -v
```

### Parallel Execution (Fast)

```bash
# Install pytest-xdist
pip3 install pytest-xdist

# Run tests in parallel
pytest test_alu.py -n auto
```

---

## Test Categories

### 1. Parametrized Tests (1,900 tests)

These tests load all test vectors from `demo.json` and run them:

```python
@pytest.mark.parametrize("test_data", load_test_vectors(), ...)
def test_alu_operation(test_data):
    # Tests each operation with 100 test cases
    ...
```

**Coverage:**
- 100 tests per operation × 19 operations = 1,900 tests
- Edge cases, boundaries, patterns, random values
- Full flag verification

### 2. Unit Tests

Organized by operation type for better readability:

#### `TestArithmetic`
- `test_add_simple` - Basic addition
- `test_add_overflow` - Addition with carry
- `test_sub_simple` - Basic subtraction
- `test_sub_underflow` - Subtraction with borrow
- `test_inc` - Increment operation
- `test_dec` - Decrement operation

#### `TestLogic`
- `test_and` - AND operation
- `test_or` - OR operation
- `test_xor` - XOR operation
- `test_nand` - NAND operation
- `test_nor` - NOR operation
- `test_xnor` - XNOR operation

#### `TestShift`
- `test_lsl` - Logical shift left
- `test_lsl_carry` - LSL with carry out
- `test_lsr` - Logical shift right
- `test_asr` - Arithmetic shift right (sign preserving)

#### `TestSpecial`
- `test_pass_a` - Pass through A
- `test_pass_b` - Pass through B
- `test_not_a` - NOT A
- `test_not_b` - NOT B
- `test_rev_a` - Reverse bits
- `test_cmp` - Compare operation

#### `TestFlags`
- `test_zero_flag` - Zero flag generation
- `test_negative_flag` - Negative flag generation
- `test_carry_flag` - Carry flag generation
- `test_overflow_flag` - Overflow flag generation

---

## Output Formats

### Standard Output

```bash
pytest test_alu.py -v

# Output:
# ========================== test session starts ==========================
# collected 1925 items
#
# test_alu.py::test_load_vectors PASSED                           [  0%]
# test_alu.py::test_alu_operation[ADD_TEST_001_A00_B00] PASSED   [  0%]
# ...
# ========================== 1925 passed in 2.45s =========================
```

### Summary Only

```bash
pytest test_alu.py --tb=no -q

# Output:
# .....................................................................
# 1925 passed in 2.30s
```

### Failed Tests Only

```bash
pytest test_alu.py --tb=short

# Shows only failures with compact traceback
```

### JUnit XML (for CI/CD)

```bash
pytest test_alu.py --junit-xml=test-results.xml
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: ALU Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install pytest
      - name: Run tests
        run: cd test && pytest test_alu.py -v
```

### GitLab CI

```yaml
# .gitlab-ci.yml
test:
  image: python:3.9
  script:
    - pip install pytest
    - cd test && pytest test_alu.py -v
```

---

## Test Results

### Expected Output

```
✅ All 1,900 parametrized tests
✅ All manual unit tests
✅ 100% pass rate
✅ All flags verified
✅ All operations validated
```

### Performance

- **Total Tests:** ~1,925 tests
- **Execution Time:** ~2-3 seconds
- **Parallel Execution:** ~1 second with `-n auto`

---

## Troubleshooting

### pytest not found

```bash
pip3 install pytest
# or
make install
```

### Import errors

```bash
# Make sure you're in the test directory or project root
cd test
pytest test_alu.py

# Or use full path
pytest /path/to/test/test_alu.py
```

### Test vectors not found

```bash
# Ensure demo.json exists
ls test/vectors/demo.json

# Re-run from project root
cd alu-core
pytest test/test_alu.py
```

---

## Advanced Usage

### Custom Test Markers

Add markers to tests:

```python
@pytest.mark.slow
@pytest.mark.arithmetic
def test_add_comprehensive():
    ...
```

Run marked tests:

```bash
pytest test_alu.py -m arithmetic
```

### Debugging Failed Tests

```bash
# Run with pdb debugger
pytest test_alu.py --pdb

# Show local variables on failure
pytest test_alu.py -l
```

### Generate Test Report

```bash
# Install pytest-html
pip3 install pytest-html

# Generate HTML report
pytest test_alu.py --html=report.html --self-contained-html
```

---

## Best Practices

1. **Run tests before commit**
   ```bash
   make test
   ```

2. **Use descriptive test names**
   - Tests are self-documenting
   - Easy to identify failures

3. **Organize tests by category**
   - Easier navigation
   - Better organization

4. **Check coverage regularly**
   ```bash
   make test-coverage
   ```

5. **Integrate with CI/CD**
   - Automated testing
   - Early bug detection

---

## Summary

This testing framework provides:

✅ **Industry-standard pytest compatibility**  
✅ **1,900+ comprehensive tests**  
✅ **Multiple ways to run (pytest, make, python)**  
✅ **CI/CD ready**  
✅ **Well-organized test structure**  
✅ **100% test coverage**

**Ready for production use!**
