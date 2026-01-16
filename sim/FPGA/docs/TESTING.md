# Testing Guide

**Comprehensive Testing Procedures for FPGA ALU Implementation**

---

## Table of Contents

- [Overview](#overview)
- [Testbench Structure](#testbench-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Debugging](#debugging)
- [Regression Testing](#regression-testing)

---

## Overview

The FPGA ALU implementation includes comprehensive testbenches covering all 19 operations, edge cases, and flag generation. This guide explains how to run tests, interpret results, and debug issues.

### Test Files

- `testbench/alu_tb.v` - Main testbench with all test suites
- `testbench/test_vectors.v` - Pre-defined test vectors
- `testbench/README.md` - Testbench documentation

---

## Testbench Structure

### Main Testbench (`alu_tb.v`)

The main testbench is organized into test suites:

1. **Arithmetic Operations** - ADD, SUB, INC, DEC
2. **Logic Operations** - AND, OR, XOR, NAND, NOR, XNOR, PASS
3. **Shift Operations** - LSL, LSR, ASR
4. **Special Operations** - REV A, NOT A, NOT B
5. **Flag Generation** - Carry, Zero, Negative flags
6. **Comparison Operation** - CMP with EQUAL, GREAT, LESS flags
7. **Edge Cases** - Overflow, underflow, maximum/minimum values

### Test Helper Functions

The testbench includes helper functions:

- `check_result()` - Verifies operation results
- `check_flag()` - Verifies flag values

### Test Output Format

```
[PASS] Test Name: Expected 0xXX, Got 0xXX
[FAIL] Test Name: Expected 0xXX, Got 0xXX
```

---

## Running Tests

### Using Vivado Simulator

#### Method 1: GUI

1. **Open Vivado**
   ```bash
   vivado
   ```

2. **Create Project**
   - File → New Project
   - Add all source files from `verilog/`
   - Add testbench from `testbench/alu_tb.v`

3. **Run Simulation**
   - Flow → Run Simulation → Run Behavioral Simulation
   - Or: `Ctrl+Shift+R`

4. **View Results**
   - Check console for test results
   - View waveform for signal inspection

#### Method 2: Batch Mode

Create `testbench/run_sim.tcl`:

```tcl
# Create project
create_project alu_test ./alu_test -part xc7a35tftg256-1

# Add source files
add_files {../verilog/circuit/main.v}
add_files {../verilog/arith/Adder.v}
# ... add all other source files ...

# Add testbench
add_files -fileset sim_1 {alu_tb.v}

# Set top module
set_property top alu_tb [get_filesets sim_1]

# Run simulation
launch_simulation
run 10000ns
```

Run:
```bash
cd testbench
vivado -mode batch -source run_sim.tcl
```

### Using ModelSim/QuestaSim

1. **Compile Sources**
   ```tcl
   vlog ../verilog/circuit/main.v
   vlog ../verilog/arith/Adder.v
   # ... compile all modules ...
   vlog alu_tb.v
   ```

2. **Run Simulation**
   ```tcl
   vsim alu_tb
   run -all
   ```

3. **View Results**
   - Check transcript for test results
   - Use waveform viewer for debugging

### Using Verilator (Open Source)

```bash
# Install Verilator (if not installed)
# sudo apt-get install verilator  # Ubuntu/Debian

# Compile
verilator --cc --exe --build alu_tb.v ../verilog/circuit/main.v \
          ../verilog/arith/Adder.v # ... all other modules

# Run
./obj_dir/Valu_tb
```

---

## Test Coverage

### Operation Coverage

| Operation | Test Cases | Status |
|-----------|------------|--------|
| ADD | 4 | ✅ Complete |
| SUB | 3 | ✅ Complete |
| INC | 2 | ✅ Complete |
| DEC | 2 | ✅ Complete |
| AND | 2 | ✅ Complete |
| OR | 1 | ✅ Complete |
| XOR | 2 | ✅ Complete |
| NAND | 1 | ✅ Complete |
| NOR | 1 | ✅ Complete |
| XNOR | 1 | ✅ Complete |
| PASS A | 1 | ✅ Complete |
| PASS B | 1 | ✅ Complete |
| LSL | 2 | ✅ Complete |
| LSR | 1 | ✅ Complete |
| ASR | 2 | ✅ Complete |
| REV A | 2 | ✅ Complete |
| NOT A | 1 | ✅ Complete |
| NOT B | 1 | ✅ Complete |
| CMP | 3 | ✅ Complete |

**Total Test Cases**: 30+

### Flag Coverage

| Flag | Test Cases | Status |
|------|------------|--------|
| Carry (C_OUT) | 5 | ✅ Complete |
| Zero (EQUAL_FL) | 4 | ✅ Complete |
| Negative | Implicit | ✅ Complete |
| Equal (CMP) | 1 | ✅ Complete |
| Greater (CMP) | 1 | ✅ Complete |
| Less (CMP) | 1 | ✅ Complete |

### Edge Case Coverage

- ✅ Overflow conditions (200+100, 255+1)
- ✅ Underflow conditions (23-65, 0-1)
- ✅ Zero results (0+0, 5-5)
- ✅ Maximum values (0xFF operations)
- ✅ Minimum values (0x00 operations)
- ✅ Signed overflow/underflow

---

## Debugging

### Common Issues

#### 1. Test Failures

**Symptom**: Tests report failures

**Debugging Steps**:
1. Check waveform for signal values
2. Verify opcode is correctly set
3. Check control signals (M, INV_OUT, etc.)
4. Verify operand values

**Example Waveform Inspection**:
```
Time: 100ns
A_IN = 0x2A (42)
B_IN = 0x17 (23)
OVERALL = 0x41 (65) ✓
C_OUT = 0 ✓
```

#### 2. X (Unknown) Values

**Symptom**: Signals show 'X' in simulation

**Causes**:
- Uninitialized signals
- Multiple drivers
- Timing violations

**Solutions**:
- Initialize all inputs
- Check for multiple assignments
- Add delays if needed

#### 3. Timing Issues

**Symptom**: Results appear at wrong time

**Solutions**:
- Add appropriate delays (`#10`)
- Check combinational path delays
- Verify clock domain (if applicable)

### Debugging Tools

#### Waveform Viewer

**Vivado**:
- Add signals to waveform
- Use cursors to measure timing
- Use markers for important events

**ModelSim**:
- Use `add wave` command
- Use `run` with time limits
- Use `examine` for signal values

#### Print Statements

Add debug prints in testbench:
```verilog
$display("Time: %t, A=%d, B=%d, Result=%d", $time, A_IN, B_IN, OVERALL);
```

#### Assertions

Add assertions for automatic checking:
```verilog
assert (OVERALL == expected) else $error("Result mismatch");
```

---

## Regression Testing

### Automated Test Suite

Create `testbench/run_regression.sh`:

```bash
#!/bin/bash

echo "Running ALU Regression Tests..."

# Run simulation
vivado -mode batch -source run_sim.tcl > test_results.log

# Check for failures
if grep -q "FAIL" test_results.log; then
    echo "❌ Some tests failed!"
    grep "FAIL" test_results.log
    exit 1
else
    echo "✅ All tests passed!"
    exit 0
fi
```

### Continuous Integration

For CI/CD integration:

```yaml
# .github/workflows/fpga-tests.yml
name: FPGA Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Vivado
        # ... installation steps ...
      - name: Run Tests
        run: |
          cd logisim/FPGA/testbench
          ./run_regression.sh
```

---

## Test Results Interpretation

### Success Criteria

- ✅ All operations produce correct results
- ✅ All flags are correctly set
- ✅ Edge cases handled correctly
- ✅ No X (unknown) values
- ✅ Timing constraints met

### Failure Analysis

When tests fail:

1. **Identify Failure Type**:
   - Result mismatch
   - Flag incorrect
   - Timing violation

2. **Isolate Problem**:
   - Check specific operation
   - Verify inputs
   - Check control signals

3. **Root Cause Analysis**:
   - Review module implementation
   - Check test vector correctness
   - Verify expected values

---

## Adding New Tests

### Test Template

```verilog
// Test: Operation Name
A_IN = 8'd<value>;
B_IN = 8'd<value>;
#10;  // Wait for propagation
check_result(8'd<expected>, OVERALL, "Test Name");
check_flag(1'b<expected>, FLAG_NAME, "Flag Name");
```

### Test Categories

1. **Basic Functionality**: Normal operation cases
2. **Edge Cases**: Boundary conditions
3. **Error Cases**: Invalid inputs (if applicable)
4. **Performance**: Timing verification

---

## Best Practices

### Test Design

- ✅ Test one operation at a time
- ✅ Use meaningful test names
- ✅ Include edge cases
- ✅ Verify flags independently
- ✅ Test both positive and negative results

### Test Maintenance

- ✅ Keep tests up-to-date with design changes
- ✅ Document test assumptions
- ✅ Review test coverage regularly
- ✅ Remove obsolete tests

### Test Documentation

- ✅ Document test purpose
- ✅ Explain expected behavior
- ✅ Note any special conditions
- ✅ Reference specification

---

## References

- [Vivado Simulation User Guide](https://www.xilinx.com/support/documentation/sw_manuals/xilinx2020_1/ug937-vivado-design-suite-simulation.pdf)
- [ModelSim User Guide](https://www.intel.com/content/www/us/en/programmable/documentation/mwh1407287965224.html)
- [SystemVerilog Testbench Guidelines](https://www.verificationacademy.com/)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | TBD | TBD | Initial testing guide |
