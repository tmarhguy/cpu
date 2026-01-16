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

**Logical Operations**
- Same ALU will handle logical operations
- Integrated design approach

</td>
</tr>
</table>

---

<div align="center">

## Control Signal

</div>

<table>
<tr>
<td width="50%">

**4-Bit Control Signal**
- Allows $2^{4} = 16$ possible operations
- Flexible operation encoding

**Control Line Logic**
- 1 if Sub, else 0 (for ADD/SUB operations)
- Direct control signal mapping

</td>
<td width="50%">

**Control Signal Values**
- **ADD:** `00000000` (8-bit)
- **SUB:** `11111111` (8-bit)
- XOR gate control pattern

</td>
</tr>
</table>

---

<div align="center">

## Test Cases from Design

</div>

<table>
<tr>
<td width="50%">

### Carry Circuit Simulation

**Inputs**
- A = 1
- B = 0
- C = 1
- Binary: `101`

**Expected Output**
- Carry = 1

</td>
<td width="50%">

### Sum Circuit Simulation

**Inputs**
- A = 1
- B = 0
- C = 0
- Binary: `100`

**Expected Output**
- Sum = 1

</td>
</tr>
</table>

---

<div align="center">

## File Format

</div>

Test vectors are stored in **JSON format** for easy parsing by firmware test runners.

---

<div align="center">

## Test Categories

</div>

<table>
<tr>
<td width="50%">

### `add_sub.json`
Arithmetic operation test vectors

**Coverage**
- ADD operations
- SUB operations
- Edge cases:
  - Overflow conditions
  - Underflow conditions
  - Zero results

</td>
<td width="50%">

### `logic_ops.json`
Logic operation test vectors

**Operations**
- AND, OR
- NAND, NOR
- XOR, XNOR
- PASS, NOT

</td>
</tr>
</table>

---

<div align="center">

## Test Vector Format

</div>

Each JSON file contains an array of test vectors. The `opcode` field is a 5-bit binary string matching `spec/opcode/opcode_table.md`.

```json
[
  {
    "test_name": "ADD_01",
    "A": 42,
    "B": 23,
    "opcode": "00000",
    "expected_result": 65,
    "expected_flags": {
      "carry": false,
      "overflow": false,
      "zero": false,
      "negative": false
    }
  }
]
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

Run the test runner against the JSON vectors and export results for CI consumption:

```bash
python3 tools/run_tests.py --vectors-dir test --output-dir results
```

Expected output:

```text
PASS add_sub.json: 4/4
Summary: 4 passed, 0 failed
Wrote results to results/test_results.json and results/test_results.csv
```

Test vectors can be loaded by the firmware test runner for automated validation and regression testing.

Run the reference validator (uses the opcode table definitions):

```bash
python3 test/run_vectors.py
```

To validate a specific file:

```bash
python3 test/run_vectors.py test/add_sub.json
```
