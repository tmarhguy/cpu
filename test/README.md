<div align="center">

# Test Vectors

**Comprehensive test vectors for ALU validation and verification**

</div>

---

<div align="center">

## Operations

</div>

<table>
<tr>
<td width="50%">

### Current Operations

**ADD**
- Operation: $A + B$
- Direct addition

**SUB**
- Operation: $A - B$
- Implementation: $A + (-B)$ using 2's complement

</td>
<td width="50%">

### Future Operations

**MUL**
- Multiplication operation
- Planned for future implementation

**DIV**
- Division operation
- Planned for future implementation

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

```json
{
  "test_name": "ADD_01",
  "A": 42,
  "B": 23,
  "opcode": "0000",
  "expected_result": 65,
  "expected_flags": {
    "carry": false,
    "overflow": false,
    "zero": false,
    "negative": false
  }
}
```

---

<div align="center">

## Usage

</div>

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
