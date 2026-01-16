# Test Generation Scripts

> Scripts for generating and running exhaustive test vectors for the 8-bit ALU

This directory contains automation scripts for test vector generation and execution.

---

## Overview

**Purpose:** Automate test vector generation and execution for the ALU

**Why these scripts exist:**
- Manually writing 256×256 test combinations for 19 operations = 1,247,084 tests is infeasible
- Automated generation ensures complete coverage of input space
- Systematic testing validates all operations across all possible inputs

---

## Scripts

### `generate_exhaustive_tests.py`

**Purpose:** Generate exhaustive test vectors (256×256 combinations per operation)

**What it does:**
- Generates all 65,536 test combinations (256×256) for each of 19 operations
- Creates JSON test vector files with expected results and flags
- Total output: 1,247,084 test vectors (65,636 tests × 19 operations)

**Usage:**
```bash
# Generate exhaustive test vectors
cd test/scripts
python3 generate_exhaustive_tests.py

# Output: vectors/exhaustive.json (16M+ lines, ~650MB)
```

**Why it exists:**
Writing 1.24 million test vectors manually would be:
- Time-consuming (months of work)
- Error-prone (human errors in test cases)
- Infeasible (impractical for verification)

**Automated generation ensures:**
- Complete coverage (all 256×256 input combinations)
- Consistent format (same JSON structure)
- Accurate results (computed by golden model)
- Fast generation (~30 seconds to generate 1.24M vectors)

---

### `run_json_tests.py`

**Purpose:** Execute tests from JSON test vector files

**What it does:**
- Loads test vectors from JSON file
- Executes each test using ALU simulation
- Compares actual vs. expected results and flags
- Provides detailed pass/fail statistics

**Usage:**
```bash
# Run demo test vectors
python3 scripts/run_json_tests.py vectors/demo.json

# Run exhaustive test vectors
python3 scripts/run_json_tests.py vectors/exhaustive.json

# Default: runs vectors/demo.json if no file specified
python3 scripts/run_json_tests.py
```

**Features:**
- Accepts any JSON test vector file as argument
- Detailed per-operation statistics
- Execution time and throughput metrics
- Useful for running specific test sets

**Note:** This is a standalone runner. For pytest-compatible testing, use `test_alu.py` in the parent directory.

---

## Test Vector Files

### `vectors/demo.json`

**Purpose:** Demonstration test vectors (1,900 tests)

**Contents:**
- 100 tests per operation (19 operations)
- Representative test cases covering:
  - Edge cases (0x00, 0xFF, 0x7F, 0x80)
  - Common values
  - Boundary conditions

**Size:** ~25KB, ~1,900 tests  
**Use case:** Quick verification, CI/CD, development

**Generation:** Pre-generated, stored in repository

---

### `vectors/exhaustive.json`

**Purpose:** Complete exhaustive test vectors (1,247,084 tests)

**Contents:**
- All 256×256 input combinations for each operation
- Complete coverage of 8-bit input space
- 65,636 tests per operation × 19 operations

**Size:** ~650MB, ~16 million lines  
**Use case:** Full verification, final validation

**Generation:** Run `generate_exhaustive_tests.py` to create  
**Note:** Not stored in repository (too large). Generate when needed.

---

## Workflow

### Generating Test Vectors

```bash
cd test/scripts

# Generate exhaustive test vectors
python3 generate_exhaustive_tests.py

# Output: ../vectors/exhaustive.json
# Time: ~30 seconds
# Size: ~650MB
```

### Running Tests

**Option 1: Use pytest-compatible runner**
```bash
cd test
python3 test_alu.py  # Runs vectors/demo.json
```

**Option 2: Use standalone JSON runner**
```bash
cd test
python3 scripts/run_json_tests.py vectors/demo.json
python3 scripts/run_json_tests.py vectors/exhaustive.json
```

**Option 3: Use pytest framework**
```bash
cd test
pytest test_alu.py -v
```

---

## Technical Details

### Test Vector Format

```json
{
  "test_name": "ADD_TEST_001",
  "opcode": "00000",
  "A": 0x2A,
  "B": 0x17,
  "expected_result": 0x41,
  "expected_flags": {
    "carry": false,
    "zero": false,
    "overflow": false,
    "negative": false
  }
}
```

### Generation Algorithm

For each operation:
1. Iterate A from 0 to 255 (256 values)
2. Iterate B from 0 to 255 (256 values)
3. Compute expected result using golden model
4. Calculate expected flags
5. Output JSON test vector

**Total:** 256 × 256 × 19 = 1,247,084 test vectors

---

## Performance

| Metric | Value |
|--------|-------|
| **Generation Time** | ~30 seconds |
| **Exhaustive File Size** | ~650MB |
| **Test Count** | 1,247,084 |
| **Execution Time** | ~9.3 seconds |
| **Throughput** | ~134,000 tests/second |

---

## Related Files

- **[test_alu.py](../test_alu.py)** - Main pytest-compatible test suite
- **[vectors/demo.json](../vectors/demo.json)** - Demonstration test vectors
- **[vectors/exhaustive.json](../vectors/exhaustive.json)** - Exhaustive test vectors (generated)

---

**Last Updated:** 2026-01-16
