# Complete Opcode Reference

**Detailed specification of all 19 ALU operations**

This document provides complete implementation details, truth tables, and examples for every opcode.

---

## Opcode Encoding

**5-bit opcode:** FUNC[4:0] allows 32 operations (0-31)
- **Implemented:** 19 operations (0-18)
- **Reserved:** 13 operations (19-31) for future expansion

### Encoding Structure

| Bits [4:3] | Category | Opcodes | Operations |
|------------|----------|---------|------------|
| `00` | Arithmetic & Shift | 0-7 | ADD, SUB, INC, DEC, LSL, LSR, ASR, REV |
| `01` | Logic | 8-15 | NAND, NOR, XOR, PASS A/B, AND, OR, XNOR |
| `10` | Special | 16-18 | CMP, NOT A, NOT B |
| `11` | **Reserved** | 19-31 | Future operations |

---

## Complete Opcode Table

| Decimal | Binary | Mnemonic | Operation | Type | Flags | Implementation |
|---------|--------|----------|-----------|------|-------|----------------|
| **0** | 00000 | ADD | A + B | Arithmetic | ✓ | Direct adder |
| **1** | 00001 | SUB | A - B | Arithmetic | ✓ | A + ~B + 1 |
| **2** | 00010 | INC | A + 1 | Arithmetic | ✓ | A + 1 |
| **3** | 00011 | DEC | A - 1 | Arithmetic | ✓ | A + ~0 + 1 |
| **4** | 00100 | LSL | A << 1 | Shift | ✓ | Logical left |
| **5** | 00101 | LSR | A >> 1 | Shift | ✓ | Logical right |
| **6** | 00110 | ASR | A >> 1 | Shift | ✓ | Arithmetic right |
| **7** | 00111 | REV | Reverse(A) | Special | ✓ | Bit reversal |
| **8** | 01000 | NAND | ~(A & B) | Logic | ✓ | Base operation |
| **9** | 01001 | NOR | ~(A \| B) | Logic | ✓ | Base operation |
| **10** | 01010 | XOR | A ^ B | Logic | ✓ | Base operation |
| **11** | 01011 | PASSA | A | Logic | ✓ | Pass through |
| **12** | 01100 | PASSB | B | Logic | ✓ | Pass through |
| **13** | 01101 | AND | A & B | Logic | ✓ | NAND + INV_OUT |
| **14** | 01110 | OR | A \| B | Logic | ✓ | NOR + INV_OUT |
| **15** | 01111 | XNOR | ~(A ^ B) | Logic | ✓ | XOR + INV_OUT |
| **16** | 10000 | CMP | Compare | Special | ✓ | A - B (flags only) |
| **17** | 10001 | NOTA | ~A | Logic | ✓ | PASSA + INV_OUT |
| **18** | 10010 | NOTB | ~B | Logic | ✓ | PASSB + INV_OUT |
| **19-31** | - | - | **Reserved** | - | - | Future use |

---

## Arithmetic Operations

### ADD (Opcode 0)

**Function:** OUT = A + B

**Truth Table (1-bit):**

| A | B | Cin | Sum | Cout |
|---|---|-----|-----|------|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

**Boolean:**
- Sum = A ⊕ B ⊕ Cin
- Cout = AB + Cin(A ⊕ B)

**8-bit Examples:**

| A (hex) | B (hex) | Result (hex) | LESS | EQUAL | POSITIVE | COUT |
|---------|---------|--------------|------|-------|----------|------|
| 0x2A | 0x17 | 0x41 (65) | 0 | 0 | 1 | 0 |
| 0xFF | 0x01 | 0x00 (0) | 0 | 0 | 0 | 1 |
| 0x7F | 0x01 | 0x80 (128) | 0 | 0 | 1 | 0 |

**Control signals:**
- M = 0 (ADD mode, B passes unchanged)
- MUX_SEL = 0 (select arithmetic unit)
- INV_OUT = 0 (no inversion)

**Implementation:** 8-bit ripple-carry adder, 336T

---

### SUB (Opcode 1)

**Function:** OUT = A - B (using 2's complement)

**Implementation:** OUT = A + ~B + 1

**8-bit Examples:**

| A (hex) | B (hex) | Result (hex) | LESS | EQUAL | POSITIVE | COUT |
|---------|---------|--------------|------|-------|----------|------|
| 0x64 | 0x23 | 0x41 (65) | 0 | 0 | 1 | 1 |
| 0x00 | 0x01 | 0xFF (-1) | 1 | 0 | 0 | 0 |
| 0x05 | 0x05 | 0x00 (0) | 0 | 1 | 0 | 1 |

**Control signals:**
- M = 1 (SUB mode, B inverted by XOR)
- Cin = 1 (M routes to first adder carry-in for +1)
- MUX_SEL = 0 (select arithmetic unit)
- INV_OUT = 0 (no post-MUX inversion)

**2's Complement Logic:**
```
A - B = A + (-B)
      = A + (~B + 1)
      = A + (B XOR 1) + Cin(1)
```

**Implementation:** Reuses adder with B XOR array, 336T + 96T = 432T total

---

### INC (Opcode 2) / DEC (Opcode 3)

**INC Function:** OUT = A + 1
- Implementation: A + 0x01, M=0
- Use case: Loop counters, address increment

**DEC Function:** OUT = A - 1
- Implementation: A + 0xFF + 1, M=1
- Use case: Loop counters, address decrement

---

## Logic Operations

### Base Operations (No Inversion)

#### NAND (Opcode 8)

**Function:** OUT = ~(A & B)

**Truth Table:**

| A | B | OUT |
|---|---|-----|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**Control:** MUX_SEL=1, LOGIC_SEL=000, INV_OUT=0

**Transistor Cost:** 8 × 4T = 32T (8-bit NAND array)

#### NOR (Opcode 9)

**Function:** OUT = ~(A | B)

**Truth Table:**

| A | B | OUT |
|---|---|-----|
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 0 |

**Control:** MUX_SEL=1, LOGIC_SEL=001, INV_OUT=0

**Transistor Cost:** 8 × 4T = 32T

#### XOR (Opcode 10)

**Function:** OUT = A ^ B

**Truth Table:**

| A | B | OUT |
|---|---|-----|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**8-bit Example:**
```
A = 0xAA (10101010)
B = 0x55 (01010101)
OUT = 0xFF (11111111)
```

**Control:** MUX_SEL=1, LOGIC_SEL=010, INV_OUT=0

**Transistor Cost:** 8 × 12T = 96T

---

### Derived Operations (With INV_OUT)

#### AND (Opcode 13)

**Function:** OUT = A & B

**Implementation:** NOT(NAND(A, B))

**Truth Table:**

| A | B | OUT |
|---|---|-----|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**Control:** MUX_SEL=1, LOGIC_SEL=000 (NAND), INV_OUT=1

**Transistor Cost:** 32T (NAND) + 16T (inverter) = 48T total, but inverter is shared

**Key insight:** Global inverter enables AND without dedicated AND gates

#### OR (Opcode 14)

**Function:** OUT = A | B

**Implementation:** NOT(NOR(A, B))

**Control:** MUX_SEL=1, LOGIC_SEL=001 (NOR), INV_OUT=1

#### XNOR (Opcode 15)

**Function:** OUT = ~(A ^ B) = (A == B) bitwise

**Implementation:** NOT(XOR(A, B))

**Control:** MUX_SEL=1, LOGIC_SEL=010 (XOR), INV_OUT=1

**8-bit Example:**
```
A = 0xAA (10101010)
B = 0x55 (01010101)
OUT = 0x00 (00000000)
```

---

## Shift Operations

### LSL - Logical Shift Left (Opcode 4)

**Function:** OUT = A << 1, fill LSB with 0

**Example:**
```
A =   0b10110001 (0xB1 = 177)
OUT = 0b01100010 (0x62 = 98)
COUT = 1 (MSB shifted out)
```

**Use:** Multiply by 2 (unsigned)

### LSR - Logical Shift Right (Opcode 5)

**Function:** OUT = A >> 1, fill MSB with 0

**Example:**
```
A =   0b10110001 (0xB1 = 177)
OUT = 0b01011000 (0x58 = 88)
COUT = 1 (LSB shifted out)
```

**Use:** Divide by 2 (unsigned)

### ASR - Arithmetic Shift Right (Opcode 6)

**Function:** OUT = A >> 1, preserve sign bit (MSB)

**Example:**
```
A =   0b10110001 (0xB1 = -79 signed)
OUT = 0b11011000 (0xD8 = -40 signed)
COUT = 1 (LSB shifted out)
```

**Use:** Divide by 2 (signed, preserves sign)

**Sign extension:**
- If A[7] = 0: OUT[7] = 0 (positive remains positive)
- If A[7] = 1: OUT[7] = 1 (negative remains negative)

---

## Special Operations

### CMP - Compare (Opcode 16)

**Function:** Compare A and B, set flags, discard result

**Flags set:**
- LESS = 1 if A < B
- EQUAL = 1 if A == B
- POSITIVE = (A - B) > 0
- COUT = carry from subtraction

**Example:**
```
A = 0x10 (16), B = 0x20 (32)
LESS = 1 (16 < 32)
EQUAL = 0 (16 ≠ 32)
```

**Usage pattern:**
```
CMP A, B
→ Check EQUAL flag for equality
→ Check LESS flag for less than
→ If LESS=0 and EQUAL=0: A > B
```

**Implementation:** Performs A - B internally, result not output

### REV - Reverse Bits (Opcode 7)

**Function:** Reverse bit order of A

**Bit mapping:**
```
A[7] → OUT[0]
A[6] → OUT[1]
A[5] → OUT[2]
A[4] → OUT[3]
A[3] → OUT[4]
A[2] → OUT[5]
A[1] → OUT[6]
A[0] → OUT[7]
```

**Example:**
```
A =   0b10110001 (0xB1)
OUT = 0b10001101 (0x8D)
```

**Use:** Bit manipulation, endianness conversion

### PASS A/B (Opcodes 11/12)

**Function:** Pass operand through unchanged

**PASS A:** OUT = A  
**PASS B:** OUT = B

**Use:** 
- Base for NOT A/NOT B operations
- Operand selection
- Testing individual inputs

### NOT A/B (Opcodes 17/18)

**Function:** Bitwise inversion

**NOT A:** OUT = ~A (PASS A with INV_OUT=1)  
**NOT B:** OUT = ~B (PASS B with INV_OUT=1)

**Example:**
```
A = 0xAA (10101010)
~A = 0x55 (01010101)
```

---

## Control Signal Decode Table

| Opcode | Operation | M | MUX_SEL | INV_OUT | LOGIC_SEL |
|--------|-----------|---|---------|---------|-----------|
| 00000 | ADD | 0 | 0 | 0 | xxx |
| 00001 | SUB | 1 | 0 | 0 | xxx |
| 00010 | INC | 0 | 0 | 0 | xxx |
| 00011 | DEC | 1 | 0 | 0 | xxx |
| 00100 | LSL | x | 0 | 0 | xxx |
| 00101 | LSR | x | 0 | 0 | xxx |
| 00110 | ASR | x | 0 | 0 | xxx |
| 00111 | REV | x | 0 | 0 | xxx |
| 01000 | NAND | x | 1 | 0 | 000 |
| 01001 | NOR | x | 1 | 0 | 001 |
| 01010 | XOR | x | 1 | 0 | 010 |
| 01011 | PASS A | x | 1 | 0 | 011 |
| 01100 | PASS B | x | 1 | 0 | 100 |
| 01101 | AND | x | 1 | 1 | 000 |
| 01110 | OR | x | 1 | 1 | 001 |
| 01111 | XNOR | x | 1 | 1 | 010 |
| 10000 | CMP | 1 | 0 | 0 | xxx |
| 10001 | NOT A | x | 1 | 1 | 011 |
| 10010 | NOT B | x | 1 | 1 | 100 |

**Control signals:**
- **M:** ADD/SUB mode (0=add, 1=subtract)
- **MUX_SEL:** Arithmetic (0) or Logic (1)
- **INV_OUT:** Global output inversion (0=direct, 1=inverted)
- **LOGIC_SEL[2:0]:** Selects logic operation

---

## Flag Generation

### Flag Definitions

| Flag | Full Name | Condition | Logic |
|------|-----------|-----------|-------|
| **LESS** | Less Than | A < B | Magnitude comparator |
| **EQUAL** | Equal | A == B | ~(A[7] XOR B[7] \| ... \| A[0] XOR B[0]) |
| **POSITIVE** | Positive | OUT > 0 | ~OUT[7] & (OUT ≠ 0) |
| **COUT** | Carry Out | Unsigned overflow | Direct from adder |

### Flag Behavior by Operation

| Operation | LESS | EQUAL | POSITIVE | COUT |
|-----------|------|-------|----------|------|
| ADD | Comparison | Comparison | Result > 0 | Carry out |
| SUB | A < B | A == B | Result > 0 | Borrow (inverted) |
| Logic ops | Comparison | Comparison | Result > 0 | 0 |
| Shifts | Comparison | Comparison | Result > 0 | Bit shifted out |
| CMP | **A < B** | **A == B** | (A-B) > 0 | Borrow |

**Note:** LESS and EQUAL always reflect comparison of A vs B, regardless of operation.

---

## Design Optimizations

### Global Inverter Technique

**Concept:** Use one 8-bit inverter to derive complementary operations

**Enabled operations:**

| Base (INV_OUT=0) | Derived (INV_OUT=1) | Savings |
|------------------|---------------------|---------|
| NAND | AND | Avoid building AND gates |
| NOR | OR | Avoid building OR gates |
| XOR | XNOR | Avoid building XNOR gates |
| PASS A | NOT A | Avoid building NOT array |
| PASS B | NOT B | Avoid building NOT array |

**Transistor cost:**
- Global inverter: 16T (8 × 2T)
- Savings: ~128T (would need separate AND/OR/XNOR gates)

**Benefit:** 89% reduction in logic unit transistor count

---

### XOR Array for ADD/SUB

**Concept:** Use XOR gates to conditionally invert B for subtraction

**Implementation:**
```
B' = B XOR M

Where M = 0: B' = B (ADD mode)
Where M = 1: B' = ~B (SUB mode)
```

**Advantage:** Same control bit M can:
1. Invert B (via XOR)
2. Set Cin = 1 (for +1 in 2's complement)

**Transistor cost:**
- XOR array: 96T (8 × 12T)
- Alternative MUX array: 160T (8 × 20T)

**Benefit:** 40% reduction vs. MUX-based approach

---

## Test Vector Examples

### Boundary Cases

| Test | A | B | Opcode | Expected | LESS | EQUAL | POSITIVE | COUT |
|------|---|---|--------|----------|------|-------|----------|------|
| Zero add | 0x00 | 0x00 | ADD | 0x00 | 0 | 1 | 0 | 0 |
| Max add | 0xFF | 0xFF | ADD | 0xFE | 0 | 0 | 1 | 1 |
| Overflow | 0xFF | 0x01 | ADD | 0x00 | 0 | 0 | 0 | 1 |
| Underflow | 0x00 | 0x01 | SUB | 0xFF | 1 | 0 | 0 | 0 |
| Equal | 0x42 | 0x42 | CMP | (N/A) | 0 | 1 | 0 | 1 |
| Less than | 0x10 | 0x20 | CMP | (N/A) | 1 | 0 | 0 | 0 |

### Corner Cases

| Test | A | B | Opcode | Expected | Notes |
|------|---|---|--------|----------|-------|
| AND zero | 0xFF | 0x00 | AND | 0x00 | Any & 0 = 0 |
| OR identity | 0xAA | 0x00 | OR | 0xAA | X \| 0 = X |
| XOR self | 0x42 | 0x42 | XOR | 0x00 | X ^ X = 0 |
| Shift max | 0xFF | - | LSL | 0xFE | Bit lost |

---

## Waveform Evidence

![Full Adder Waveform](../media/sim_ngspice_fulladder_waveform.png)
*Figure 1 - Full adder SPICE simulation: all 8 input combinations verified*

> **Evidence:** Transistor-level simulation confirms arithmetic correctness.

---

## Future Opcodes (Reserved)

### Suggested Expansion (Opcodes 19-31)

| Opcode | Proposed | Function | Difficulty |
|--------|----------|----------|------------|
| 19 | MUL | A × B (8-bit) | High |
| 20 | MULH | (A × B) >> 8 | High |
| 21 | DIV | A / B | Very High |
| 22 | MOD | A % B | Very High |
| 23 | ROL | Rotate left | Medium |
| 24 | ROR | Rotate right | Medium |
| 25 | SXT | Sign extend | Low |
| 26 | ZXT | Zero extend | Low |
| 27 | BSWAP | Byte swap | Low |
| 28-31 | - | Custom operations | - |

---

## References

- [System Architecture](ARCHITECTURE.md) - Detailed datapath and control logic
- [Verification](VERIFICATION.md) - Test methodology and results
- [Power Analysis](POWER.md) - Transistor count and power consumption
- [Specification](../spec/alu-spec.md) - Formal ALU specification

---

## Document Information

**Author:** Tyrone Marhguy  
**Affiliation:** University of Pennsylvania, Computer Engineering '28  
**Last Updated:** January 2026  
**Contact:** [tmarhguy.com](https://tmarhguy.com) | [LinkedIn](https://linkedin.com/in/tmarhguy) | [Twitter](https://twitter.com/marhguy_tyrone) | [Instagram](https://instagram.com/tmarhguy) | [Substack](https://tmarhguy.substack.com)

---

**Version:** 1.0  
**Status:** All 19 operations verified and documented
