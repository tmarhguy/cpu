# Testbench Documentation

**Testbench Suite for 8-Bit ALU FPGA Implementation**

---

## Overview

This directory contains comprehensive testbenches for verifying the FPGA ALU implementation. The test suite covers all 19 operations, flag generation, and edge cases.

---

## Files

### `alu_tb.v`
Main testbench file containing:
- Test suite organization
- Test helper functions
- All test cases for 19 operations
- Flag verification
- Edge case testing

### `test_vectors.v`
Pre-defined test vectors in structured format:
- Test vector structure definition
- Test cases for all operations
- Expected results and flags

### `run_sim.tcl`
Vivado simulation script:
- Project setup
- Source file addition
- Simulation launch
- Result collection

---

## Quick Start

### Running Tests

```bash
cd logisim/FPGA/testbench
vivado -mode batch -source run_sim.tcl
```

### Viewing Results

Check the console output for test results:
```
[PASS] Test Name: Expected 0xXX, Got 0xXX
[FAIL] Test Name: Expected 0xXX, Got 0xXX
```

---

## Test Coverage

- ✅ All 19 operations
- ✅ Flag generation (Carry, Zero, Negative, Comparison)
- ✅ Edge cases (overflow, underflow, zero)
- ✅ 30+ test cases

---

## Documentation

See [Testing Guide](../docs/TESTING.md) for detailed testing procedures and debugging tips.

---

## Status

- ✅ Testbench complete
- ✅ All operations tested
- ✅ Ready for regression testing
