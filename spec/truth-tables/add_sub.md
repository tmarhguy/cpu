# Addition and Subtraction Truth Tables

> Truth tables for 8-bit addition and subtraction operations

This document provides complete truth tables for ADD and SUB operations, including flag generation and edge cases.

---

## 8-bit Addition (ADD)

**Opcode:** 00000 (binary: 00000, decimal: 0)  
**Operation:** OUT = A + B

### Basic Addition Examples

| A (hex) | A (dec) | B (hex) | B (dec) | Result (hex) | Result (dec) | COUT | Notes |
|---------|---------|---------|---------|--------------|--------------|------|-------|
| 0x00 | 0 | 0x00 | 0 | 0x00 | 0 | 0 | Zero plus zero |
| 0x01 | 1 | 0x01 | 1 | 0x02 | 2 | 0 | Simple addition |
| 0x2A | 42 | 0x17 | 23 | 0x41 | 65 | 0 | Standard addition |
| 0xFF | 255 | 0x01 | 1 | 0x00 | 0 | 1 | Overflow wraps to 0 |
| 0x7F | 127 | 0x01 | 1 | 0x80 | 128 | 0 | No unsigned overflow |
| 0x80 | 128 | 0x80 | 128 | 0x00 | 0 | 1 | Wrap-around |

### Flag Generation for ADD

| A (dec) | B (dec) | Result | COUT | EQUAL | POSITIVE | Notes |
|---------|---------|--------|------|-------|----------|-------|
| 0 | 0 | 0 | 0 | 1 | 0 | Zero result |
| 42 | 23 | 65 | 0 | 0 | 1 | Positive result |
| 255 | 1 | 0 | 1 | 1 | 0 | Wrap-around, zero result |
| 127 | 1 | 128 | 0 | 0 | 0 | MSB set (negative in 2's comp) |
| 100 | 100 | 200 | 0 | 0 | 0 | MSB set |
| 200 | 56 | 0 | 1 | 1 | 0 | Wrap to zero |

### Full Adder Truth Table (1-bit)

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

**Boolean Expressions:**
- Sum = A ⊕ B ⊕ Cin
- Cout = AB + Cin(A ⊕ B)

### 8-bit Ripple-Carry Addition

For 8-bit addition, the carry propagates from bit 0 (LSB) to bit 7 (MSB):

```
C[0] = 0 (initial carry-in)
S[0] = A[0] ⊕ B[0] ⊕ C[0]
C[1] = A[0]B[0] + C[0](A[0] ⊕ B[0])
...
S[7] = A[7] ⊕ B[7] ⊕ C[7]
COUT = C[8] = A[7]B[7] + C[7](A[7] ⊕ B[7])
```

---

## 8-bit Subtraction (SUB)

**Opcode:** 00001 (binary: 00001, decimal: 1)  
**Operation:** OUT = A - B (using 2's complement)

**Implementation:** A - B = A + (~B) + 1

### Basic Subtraction Examples

| A (hex) | A (dec) | B (hex) | B (dec) | Result (hex) | Result (dec) | COUT | Notes |
|---------|---------|---------|---------|--------------|--------------|------|-------|
| 0x05 | 5 | 0x02 | 2 | 0x03 | 3 | 1 | Simple subtraction |
| 0x64 | 100 | 0x23 | 35 | 0x41 | 65 | 1 | Standard subtraction |
| 0x00 | 0 | 0x01 | 1 | 0xFF | 255 | 0 | Underflow, borrow occurred |
| 0x05 | 5 | 0x05 | 5 | 0x00 | 0 | 1 | Equal values, zero result |
| 0x01 | 1 | 0x00 | 0 | 0x01 | 1 | 1 | No borrow |
| 0x80 | 128 | 0x01 | 1 | 0x7F | 127 | 1 | Underflow (interpreted) |

### Flag Generation for SUB

| A (dec) | B (dec) | Result | COUT | EQUAL | LESS | POSITIVE | Notes |
|---------|---------|--------|------|-------|------|----------|-------|
| 5 | 2 | 3 | 1 | 0 | 0 | 1 | A > B, positive result |
| 5 | 5 | 0 | 1 | 1 | 0 | 0 | A == B, zero result |
| 5 | 10 | 251 | 0 | 0 | 1 | 0 | A < B, borrow occurred |
| 100 | 35 | 65 | 1 | 0 | 0 | 1 | A > B |
| 0 | 1 | 255 | 0 | 0 | 1 | 0 | Underflow |

### 2's Complement Subtraction

For A - B:

1. Invert B: ~B
2. Add 1 to inverted B: ~B + 1
3. Add to A: A + (~B + 1)

**Example:** 5 - 3 = ?

```
A = 5 = 00000101
B = 3 = 00000011
~B = 11111100
~B + 1 = 11111101 (2's complement of 3 = -3)
A + (~B + 1) = 00000101 + 11111101 = 00000010 = 2
```

**Verification:** 5 - 3 = 2 ✓

### Subtraction with Borrow

When A < B, a borrow occurs:

**Example:** 3 - 5 = ?

```
A = 3 = 00000011
B = 5 = 00000101
~B = 11111010
~B + 1 = 11111011 (2's complement of 5 = -5)
A + (~B + 1) = 00000011 + 11111011 = 11111110 = 254 (unsigned) = -2 (signed)

COUT = 0 (borrow occurred)
LESS = 1 (A < B)
```

---

## Edge Cases

### Maximum Values

| Operation | A | B | Result | COUT | Description |
|-----------|---|---|--------|------|-------------|
| ADD | 255 | 1 | 0 | 1 | Maximum overflow |
| ADD | 255 | 255 | 254 | 1 | Both maximum values |
| SUB | 255 | 255 | 0 | 1 | Equal maximum values |
| SUB | 255 | 1 | 254 | 1 | Maximum - 1 |
| SUB | 1 | 255 | 2 | 0 | Minimum underflow |

### Zero Operations

| Operation | A | B | Result | COUT | Description |
|-----------|---|---|--------|------|-------------|
| ADD | 0 | 0 | 0 | 0 | Zero + Zero |
| ADD | 0 | 255 | 255 | 0 | Zero + Maximum |
| SUB | 0 | 0 | 0 | 1 | Zero - Zero |
| SUB | 0 | 1 | 255 | 0 | Zero - One (borrow) |
| SUB | 255 | 0 | 255 | 1 | Maximum - Zero |

### Signed Boundary (127/128)

| Operation | A | B | Result | COUT | Description |
|-----------|---|---|--------|------|-------------|
| ADD | 127 | 1 | 128 | 0 | Signed overflow possible |
| ADD | 128 | 128 | 0 | 1 | Wrap-around |
| SUB | 128 | 127 | 1 | 1 | Cross signed boundary |
| SUB | 127 | 128 | 255 | 0 | Negative result |

---

## Overflow Detection

### Unsigned Overflow (Carry Out)

For ADD:
- COUT = 1 when result < A or result < B (unsigned overflow)
- Example: 255 + 1 = 0 with COUT = 1

For SUB:
- COUT = 0 when A < B (borrow occurred, unsigned underflow)
- COUT = 1 when A >= B (no borrow)

### Signed Overflow (Arithmetic)

Signed overflow occurs when:
- Adding two positive numbers gives a negative result
- Adding two negative numbers gives a positive result
- Subtracting when signs differ and result has wrong sign

**Not directly detected by flags**, requires additional logic.

---

## Implementation

### ADD Operation

```
OUT[7:0] = A[7:0] + B[7:0]
COUT = Carry from bit 7
```

**Circuit:** 8-bit ripple-carry adder  
**Propagation Delay:** ~400ns (8 full adder stages)

### SUB Operation

```
OUT[7:0] = A[7:0] + (~B[7:0]) + 1
COUT = ~Borrow (1 when no borrow, 0 when borrow)
```

**Circuit:** Same adder with B inverted and Cin = 1  
**Uses:** XOR array for B inversion, M control signal

---

**Last Updated:** 2026-01-16  
**See Also:** [Logic Operations](logic_ops.md) | [Shift Operations](shifts.md) | [Compare Operation](compare.md)
