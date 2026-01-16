# Test Vectors

> Test vector files for ALU verification

This directory contains JSON test vector files used for automated ALU testing.

---

## Overview

**Purpose:** Store test vectors for ALU operations

**Contents:**
- `demo.json` - Demonstration test vectors (1,900 tests)
- `exhaustive.json` - Exhaustive test vectors (1,247,084 tests, generated)

---

## Test Vector Files

### `demo.json`

**Purpose:** Representative test cases for quick verification

**Statistics:**
- **Tests:** 1,900 (100 per operation)
- **Size:** ~25KB
- **Operations:** All 19 ALU operations
- **Coverage:** Edge cases, common values, boundary conditions

**Contents:**
- 100 carefully selected test cases per operation
- Covers edge cases: 0x00, 0xFF, 0x7F, 0x80
- Includes common arithmetic and logic operations
- Representative sampling of full input space

**Use cases:**
- Quick verification during development
- CI/CD regression testing
- Fast iteration and debugging
- Demonstrating test coverage

**Generation:** Pre-generated, stored in repository

---

### `exhaustive.json`

**Purpose:** Complete exhaustive test coverage (all 256×256 combinations)

**Statistics:**
- **Tests:** 1,247,084 (65,636 per operation × 19 operations)
- **Size:** ~650MB (too large for git)
- **Coverage:** Complete 8-bit input space
- **Operations:** All 19 ALU operations

**Contents:**
- All possible 8-bit input combinations (256×256 per operation)
- Complete coverage of input space
- Every A/B combination tested
- All edge cases automatically included

**Use cases:**
- Final verification before hardware deployment
- Complete coverage analysis
- Finding rare corner case bugs
- Validation for critical operations

**Generation:**
```bash
cd test/scripts
python3 generate_exhaustive_tests.py
```

**Note:** Not stored in repository due to size. Generate when needed for exhaustive testing.

---

## Test Vector Format

Each test vector is a JSON object:

```json
{
  "test_name": "ADD_TEST_001",
  "opcode": "00000",
  "A": 42,
  "B": 23,
  "expected_result": 65,
  "expected_flags": {
    "carry": false,
    "zero": false,
    "overflow": false,
    "negative": false
  }
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `test_name` | string | Unique test identifier |
| `opcode` | string | 5-bit opcode (binary string) |
| `A` | integer | First operand (0-255) |
| `B` | integer | Second operand (0-255) |
| `expected_result` | integer | Expected output (0-255) |
| `expected_flags` | object | Expected flag values |

### Flag Format

```json
{
  "carry": bool,      // Carry flag (unsigned overflow)
  "zero": bool,       // Zero flag (result == 0)
  "overflow": bool,   // Overflow flag (signed overflow)
  "negative": bool    // Negative flag (MSB == 1)
}
```

---

## Coverage Statistics

### Demo Test Vectors (`demo.json`)

| Operation | Tests | Coverage |
|-----------|-------|----------|
| ADD | 100 | Representative |
| SUB | 100 | Representative |
| ... (all 19) | 100 each | Representative |
| **Total** | **1,900** | **Selected cases** |

### Exhaustive Test Vectors (`exhaustive.json`)

| Operation | Tests | Coverage |
|-----------|-------|----------|
| ADD | 65,636 | Complete (256×256) |
| SUB | 65,636 | Complete (256×256) |
| ... (all 19) | 65,636 each | Complete (256×256) |
| **Total** | **1,247,084** | **Complete input space** |

---

## Using Test Vectors

### With `test_alu.py` (pytest-compatible)

```bash
cd test
python3 test_alu.py  # Uses vectors/demo.json by default
```

### With `run_json_tests.py` (standalone)

```bash
# Run demo vectors
python3 scripts/run_json_tests.py vectors/demo.json

# Run exhaustive vectors
python3 scripts/run_json_tests.py vectors/exhaustive.json
```

### With pytest

```bash
cd test
pytest test_alu.py -v  # Uses vectors/demo.json
```

---

## Generating Exhaustive Vectors

**Why generate exhaustively?**

Manually writing 256×256 test combinations for 19 operations would require:
- 1,247,084 individual test cases
- Months of manual work
- High error rate from human mistakes

**Automated generation:**
- Complete in ~30 seconds
- 100% accurate (computed by golden model)
- Consistent format
- No human errors

**How to generate:**
```bash
cd test/scripts
python3 generate_exhaustive_tests.py

# Output: ../vectors/exhaustive.json
# Time: ~30 seconds
# Size: ~650MB
```

---

## File Sizes

| File | Size | Tests | Status |
|------|------|-------|--------|
| `demo.json` | ~25KB | 1,900 | In repository |
| `exhaustive.json` | ~650MB | 1,247,084 | Generated (not in git) |

**Note:** `exhaustive.json` is too large for git. Generate locally when needed for complete verification.

---

## Test Coverage

### Demo Vectors (`demo.json`)

Covers:
- Edge cases (0x00, 0xFF, 0x7F, 0x80)
- Common arithmetic operations
- Logic operation patterns
- Boundary conditions
- Overflow/underflow cases

**Use for:** Development, CI/CD, quick checks

### Exhaustive Vectors (`exhaustive.json`)

Covers:
- All 256×256 input combinations per operation
- Complete 8-bit input space
- Every possible test case
- All edge cases automatically

**Use for:** Final verification, complete validation

---

**Last Updated:** 2026-01-16  
**See Also:** [Test Scripts](../scripts/README.md) | [Test Suite](../README.md)
