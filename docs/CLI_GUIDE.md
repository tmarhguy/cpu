# ALU Command Line Interface Guide

**Professional CLI tool for executing 8-bit ALU operations**

The `alu_cli.py` tool provides an interactive command-line interface for testing and demonstrating ALU operations. It supports multiple input/output formats and is designed for both educational use and hardware integration.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Input Formats](#input-formats)
- [Output Formats](#output-formats)
- [Operation Reference](#operation-reference)
- [Advanced Features](#advanced-features)
- [Examples](#examples)
- [FPGA Integration](#fpga-integration)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
# Make executable (first time only)
chmod +x alu_cli.py

# Run a simple addition
./alu_cli.py ADD 42 23

# List all available operations
./alu_cli.py --list

# Get help
./alu_cli.py --help
```

---

## Installation

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses standard library only)

### Setup

```bash
# Clone the repository
git clone https://github.com/tmarhguy/cpu.git
cd cpu

# Make CLI executable
chmod +x alu_cli.py

# Test installation
./alu_cli.py --list
```

---

## Basic Usage

### Command Syntax

```bash
./alu_cli.py <OPERATION> <A> <B> [OPTIONS]
```

**Parameters:**
- `OPERATION`: ALU operation name (ADD, SUB, AND, XOR, etc.)
- `A`: First operand (0-255)
- `B`: Second operand (0-255)

**Options:**
- `--hex`: Interpret inputs as hexadecimal
- `--binary`: Interpret inputs as binary
- `--format <type>`: Output format (decimal, hex, binary, all)
- `--mode <mode>`: Execution mode (simulation, fpga)
- `--list`: List all operations
- `--quiet`: Minimal output (result only)
- `--help`: Show help message

### Basic Examples

```bash
# Addition
./alu_cli.py ADD 42 23

# Subtraction
./alu_cli.py SUB 100 35

# Logical AND
./alu_cli.py AND 255 15

# Logical XOR
./alu_cli.py XOR 170 85
```

---

## Input Formats

### Decimal (Default)

```bash
./alu_cli.py ADD 42 23
```

### Hexadecimal

**Option 1: Auto-detect with 0x prefix**
```bash
./alu_cli.py XOR 0xAA 0x55
```

**Option 2: Explicit --hex flag**
```bash
./alu_cli.py --hex XOR AA 55
```

### Binary

**Option 1: Auto-detect with 0b prefix**
```bash
./alu_cli.py AND 0b11110000 0b00001111
```

**Option 2: Explicit --binary flag**
```bash
./alu_cli.py --binary AND 11110000 00001111
```

---

## Output Formats

### Decimal (Default)

```bash
./alu_cli.py ADD 42 23
```

**Output:**
```
======================================================================
ALU Operation: ADD
======================================================================
Category:    Arithmetic
Expression:  A + B
Description: Addition

Inputs:
  A =  42
  B =  23

Result:
  OUT =  65

Flags:
  Carry (C):    0 (CLEAR)
  Zero (Z):     0 (CLEAR)
  Negative (N): 0 (CLEAR)
  Overflow (V): 0 (CLEAR)
======================================================================
```

### Hexadecimal

```bash
./alu_cli.py --format hex XOR 0xAA 0x55
```

**Output:**
```
======================================================================
ALU Operation: XOR
======================================================================
Category:    Logic
Expression:  A ^ B
Description: XOR gate

Inputs:
  A = 0xAA
  B = 0x55

Result:
  OUT = 0xFF

Flags:
  Carry (C):    0 (CLEAR)
  Zero (Z):     0 (CLEAR)
  Negative (N): 1 (SET)
  Overflow (V): 0 (CLEAR)
======================================================================
```

### Binary

```bash
./alu_cli.py --format binary AND 0xF0 0x0F
```

**Output:**
```
Inputs:
  A = 0b11110000
  B = 0b00001111

Result:
  OUT = 0b00000000
```

### All Formats

```bash
./alu_cli.py --format all SUB 100 35
```

**Output:**
```
Inputs:
  A = 100 (0x64, 0b01100100)
  B =  35 (0x23, 0b00100011)

Result:
  OUT =  65 (0x41, 0b01000001)
```

### Quiet Mode (Result Only)

```bash
./alu_cli.py --quiet ADD 42 23
```

**Output:**
```
65
```

---

## Operation Reference

### Arithmetic Operations (8)

| Operation | Opcode | Expression | Description |
|-----------|--------|------------|-------------|
| ADD       | 00000  | A + B      | Addition |
| SUB       | 00001  | A - B      | Subtraction (2's complement) |
| INC       | 00010  | A + 1      | Increment A |
| DEC       | 00011  | A - 1      | Decrement A |
| LSL       | 00100  | A << 1     | Logical shift left |
| LSR       | 00101  | A >> 1     | Logical shift right |
| ASR       | 00110  | A >> 1 (sign) | Arithmetic shift right |
| REV       | 00111  | reverse(A) | Reverse bit order |

### Logic Operations (8)

| Operation | Opcode | Expression | Description |
|-----------|--------|------------|-------------|
| NAND      | 01000  | ~(A & B)   | NAND gate |
| NOR       | 01001  | ~(A \| B)  | NOR gate |
| XOR       | 01010  | A ^ B      | XOR gate |
| PASSA     | 01011  | A          | Pass A through |
| PASSB     | 01100  | B          | Pass B through |
| AND       | 01101  | A & B      | AND gate |
| OR        | 01110  | A \| B     | OR gate |
| XNOR      | 01111  | ~(A ^ B)   | XNOR gate |

### Special Operations (3)

| Operation | Opcode | Expression | Description |
|-----------|--------|------------|-------------|
| CMP       | 10000  | A - B (flags) | Compare (flags only) |
| NOTA      | 10001  | ~A         | Invert A |
| NOTB      | 10010  | ~B         | Invert B |

---

## Advanced Features

### List All Operations

```bash
./alu_cli.py --list
```

**Output:**
```
======================================================================
Available ALU Operations (19 total)
======================================================================

Arithmetic Operations:
----------------------------------------------------------------------
  ADD      [00000]  A + B                  Addition
  SUB      [00001]  A - B                  Subtraction (2's complement)
  INC      [00010]  A + 1                  Increment A
  DEC      [00011]  A - 1                  Decrement A

Logic Operations:
----------------------------------------------------------------------
  NAND     [01000]  ~(A & B)               NAND gate
  AND      [01101]  A & B                  AND gate
  ...

======================================================================
Usage Examples:
  ./alu_cli.py ADD 42 23
  ./alu_cli.py --hex XOR 0xAA 0x55
  ./alu_cli.py --binary AND 11110000 00001111
  ./alu_cli.py --format all SUB 100 35
======================================================================
```

### Chaining Operations (Bash)

```bash
# Store result in variable
RESULT=$(./alu_cli.py --quiet ADD 42 23)
echo "Result: $RESULT"

# Chain operations
A=42
B=23
SUM=$(./alu_cli.py --quiet ADD $A $B)
DOUBLE=$(./alu_cli.py --quiet ADD $SUM $SUM)
echo "42 + 23 = $SUM, doubled = $DOUBLE"
```

### Batch Processing

```bash
# Process multiple operations
for op in ADD SUB AND OR XOR; do
    echo "$op: $(./alu_cli.py --quiet $op 0xFF 0x0F)"
done
```

---

## Examples

### Example 1: Basic Arithmetic

```bash
./alu_cli.py ADD 42 23
```

**Use case:** Simple addition demonstration

### Example 2: Hexadecimal Bitwise Operations

```bash
./alu_cli.py --hex --format hex XOR 0xAA 0x55
```

**Use case:** Bitwise XOR with hex input/output

### Example 3: Binary Logic Gates

```bash
./alu_cli.py --binary --format binary AND 11110000 00001111
```

**Use case:** Visualize AND gate operation at bit level

### Example 4: Comparison Operation

```bash
./alu_cli.py CMP 100 50
```

**Use case:** Compare two values, check flags

### Example 5: Shift Operations

```bash
./alu_cli.py --format all LSL 0x05
```

**Use case:** Logical shift left, see all representations

### Example 6: Overflow Detection

```bash
./alu_cli.py ADD 200 100
```

**Use case:** Demonstrate 8-bit overflow (result wraps to 44)

### Example 7: 2's Complement Subtraction

```bash
./alu_cli.py SUB 10 20
```

**Use case:** Show 2's complement for negative results

### Example 8: Bit Reversal

```bash
./alu_cli.py --hex --format binary REV 0xB1 0
```

**Use case:** Reverse bit order (0xB1 → 0x8D)

---

## FPGA Integration

### Future Feature

The CLI is designed to support FPGA hardware execution:

```bash
# Simulation mode (current)
./alu_cli.py --mode simulation ADD 42 23

# FPGA mode (future)
./alu_cli.py --mode fpga --port /dev/ttyUSB0 ADD 42 23
```

### Implementation Plan

1. **Serial Communication:** Send opcode and operands via UART
2. **Result Readback:** Receive result and flags from FPGA
3. **Automatic Detection:** Auto-detect connected FPGA
4. **Performance Comparison:** Compare simulation vs. hardware timing

### Protocol Design

```
Command Format (to FPGA):
  [5-bit opcode][8-bit A][8-bit B] = 21 bits

Response Format (from FPGA):
  [8-bit result][4-bit flags] = 12 bits
```

---

## Troubleshooting

### Common Issues

#### Issue: "Command not found"

**Solution:**
```bash
# Make executable
chmod +x alu_cli.py

# Or run with python3
python3 alu_cli.py ADD 42 23
```

#### Issue: "Could not import ALU8Bit"

**Solution:**
```bash
# Ensure you're in the project root directory
cd /path/to/cpu

# Check test_alu.py exists
ls test/test_alu.py
```

#### Issue: "Operand out of 8-bit range"

**Solution:**
```bash
# Values must be 0-255
./alu_cli.py ADD 42 23    # OK
./alu_cli.py ADD 300 23   # ERROR: 300 > 255
```

#### Issue: "Unknown operation"

**Solution:**
```bash
# List valid operations
./alu_cli.py --list

# Use correct operation name (case-insensitive)
./alu_cli.py ADD 42 23    # OK
./alu_cli.py add 42 23    # OK
./alu_cli.py PLUS 42 23   # ERROR: Unknown operation
```

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Unknown operation" | Invalid operation name | Use `--list` to see valid operations |
| "Out of 8-bit range" | Value > 255 or < 0 | Use values 0-255 |
| "Could not import" | Missing test_alu.py | Run from project root directory |
| "Invalid literal" | Malformed number | Check input format (hex needs 0x prefix) |

---

## Integration with Test Suite

### Comparison with Test Suite

The CLI uses the same golden model as the test suite:

```bash
# CLI execution
./alu_cli.py ADD 42 23

# Test suite execution
./run_tests.sh              # Quick test (1,900 tests)
./run_tests.sh exhaustive   # Exhaustive test (1,247,084 tests)
```

Both use `test/test_alu.py::ALU8Bit` class.

### Verification Workflow

1. **Develop operation** in `test_alu.py`
2. **Test with CLI** for quick verification
3. **Run full test suite** for comprehensive coverage
4. **Deploy to FPGA** (future)

---

## Performance

### Execution Time

- **Simulation mode:** < 10ms per operation
- **FPGA mode:** < 1ms per operation (future)

### Throughput

- **CLI overhead:** ~5ms (Python startup)
- **Operation execution:** < 1ms
- **Total:** ~6ms per invocation

For high-throughput testing, use the batch test suite instead.

---

## Contributing

### Adding New Operations

1. Add operation to `test_alu.py::ALU8Bit`
2. Add opcode mapping to `alu_cli.py::ALUInterface.OPCODE_MAP`
3. Add operation info to `alu_cli.py::ALUInterface.OPERATION_INFO`
4. Update this documentation

### Improving the CLI

- Add interactive mode (REPL)
- Add operation history
- Add result comparison
- Add timing measurements
- Improve error messages

---

## Related Documentation

- [OPCODE_TABLE.md](OPCODE_TABLE.md) - Complete operation reference
- [VERIFICATION.md](VERIFICATION.md) - Test methodology
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [GETTING_STARTED.md](GETTING_STARTED.md) - Project setup

---

## Support

**Questions or issues?**

- Open an issue: [github.com/tmarhguy/cpu/issues](https://github.com/tmarhguy/cpu/issues)
- Email: tmarhguy@gmail.com | tmarhguy@seas.upenn.edu
- Twitter: [@marhguy_tyrone](https://twitter.com/marhguy_tyrone)
- Instagram: [@tmarhguy](https://instagram.com/tmarhguy)
- Substack: [@tmarhguy](https://tmarhguy.substack.com)
- Documentation: [docs/](.)

---

**Document Information**

**Author:** Tyrone Marhguy  
**Last Updated:** January 2026  
**Version:** 1.0  
**Project:** 8-Bit Discrete Transistor ALU

---

**Quick Reference Card**

```bash
# Basic usage
./alu_cli.py <OP> <A> <B>

# Input formats
./alu_cli.py ADD 42 23              # Decimal
./alu_cli.py --hex XOR 0xAA 0x55    # Hexadecimal
./alu_cli.py --binary AND 11110000 00001111  # Binary

# Output formats
--format decimal    # 65
--format hex        # 0x41
--format binary     # 0b01000001
--format all        # 65 (0x41, 0b01000001)

# Utilities
--list              # List operations
--quiet             # Result only
--help              # Show help
```
