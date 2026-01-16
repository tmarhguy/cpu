# ALU Quick Reference Card

**One-Page Reference for 8-Bit ALU Operations**

---

## Operations (19 Total)

### Arithmetic (8)
| Op | Code | Operation | Result |
|----|------|-----------|--------|
| ADD | 0 | A + B | Sum |
| SUB | 1 | A - B | 2's complement |
| INC | 2 | A + 1 | Increment |
| DEC | 3 | A - 1 | Decrement |
| LSL | 4 | A << 1 | Shift left |
| LSR | 5 | A >> 1 | Shift right (logical) |
| ASR | 6 | A >> 1 | Shift right (arithmetic) |
| REV | 7 | Reverse A | Bit reversed |

### Logic (8)
| Op | Code | Operation | Result |
|----|------|-----------|--------|
| NAND | 8 | A NAND B | ~(A & B) |
| NOR | 9 | A NOR B | ~(A \| B) |
| XOR | 10 | A XOR B | A ^ B |
| PASS A | 11 | Pass A | A |
| PASS B | 12 | Pass B | B |
| AND | 13 | A AND B | A & B |
| OR | 14 | A OR B | A \| B |
| XNOR | 15 | A XNOR B | ~(A ^ B) |

### Special (3)
| Op | Code | Operation | Result |
|----|------|-----------|--------|
| CMP | 16 | Compare A, B | Flags only |
| NOT A | 17 | Invert A | ~A |
| NOT B | 18 | Invert B | ~B |

---

## Flags

| Flag | Name | Description |
|------|------|-------------|
| C_OUT | Carry | Arithmetic overflow/underflow |
| EQUAL_FL | Zero | Result = 0 or A = B (CMP) |
| GREAT_FL | Greater | A > B (CMP only) |
| LESS_FL | Less | A < B (CMP only) |

---

## Ports

### Inputs
- `A_IN[7:0]` - Operand A
- `B_IN[7:0]` - Operand B
- `logisimClockTree0[4:0]` - Clock/opcode (internal)

### Outputs
- `OVERALL[7:0]` - Final result
- `SUM[7:0]` - Arithmetic result
- `LOGIC_OUT[7:0]` - Logic result
- `C_OUT` - Carry flag
- `EQUAL_FL` - Zero/Equal flag
- `GREAT_FL` - Greater flag
- `LESS_FL` - Less flag

---

## Common Operations

```verilog
// ADD: 42 + 23 = 65
A_IN = 8'd42;
B_IN = 8'd23;
// Set opcode to 0

// SUB: 65 - 23 = 42
A_IN = 8'd65;
B_IN = 8'd23;
// Set opcode to 1

// AND: 0xAA & 0x55 = 0x00
A_IN = 8'hAA;
B_IN = 8'h55;
// Set opcode to 13

// XOR: 0xAA ^ 0x55 = 0xFF
A_IN = 8'hAA;
B_IN = 8'h55;
// Set opcode to 10
```

---

## Test Commands

```bash
# Run simulation
cd testbench
vivado -mode batch -source run_sim.tcl

# Synthesize
cd scripts
vivado -mode batch -source synthesize.tcl
```

---

## File Locations

- **Source**: `verilog/circuit/main.v`
- **Testbench**: `testbench/alu_tb.v`
- **Docs**: `docs/`
- **Scripts**: `scripts/`

---

**Version**: 1.0 | **Last Updated**: 2024
