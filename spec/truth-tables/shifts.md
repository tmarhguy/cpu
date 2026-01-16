# Shift Operations Truth Tables

> Truth tables for shift operations: Logical Shift Left (LSL), Logical Shift Right (LSR), and Arithmetic Shift Right (ASR)

The ALU implements three shift operations that move bits left or right within an 8-bit word, with different fill strategies for vacated bits.

---

## Logical Shift Left (LSL)

**Opcode:** 00100 (binary: 00100, decimal: 4)  
**Operation:** OUT = A << 1 (shift left by 1 bit)  
**Fill:** Rightmost bit filled with 0  
**Carry Out:** MSB shifted out becomes COUT

### Truth Table

| A (binary) | A (hex) | OUT (binary) | OUT (hex) | COUT | Description |
|------------|---------|--------------|-----------|------|-------------|
| 00000000 | 0x00 | 00000000 | 0x00 | 0 | Zero shifted |
| 00000001 | 0x01 | 00000010 | 0x02 | 0 | Shift 1 → 2 |
| 00000010 | 0x02 | 00000100 | 0x04 | 0 | Shift 2 → 4 |
| 10000000 | 0x80 | 00000000 | 0x00 | 1 | MSB shifted out |
| 11000000 | 0xC0 | 10000000 | 0x80 | 1 | MSB shifted out |
| 10110001 | 0xB1 | 01100010 | 0x62 | 1 | MSB = 1, shifted out |
| 01111111 | 0x7F | 11111110 | 0xFE | 0 | MSB = 0 |
| 11111111 | 0xFF | 11111110 | 0xFE | 1 | All ones, MSB out |

### Examples

**Example 1:**
```
A = 0x05 (00000101)
LSL A = 0x0A (00001010)
COUT = 0 (MSB was 0)
```

**Example 2:**
```
A = 0x81 (10000001)
LSL A = 0x02 (00000010)
COUT = 1 (MSB = 1 was shifted out)
```

**Example 3:**
```
A = 0xB1 (10110001)
LSL A = 0x62 (01100010)
COUT = 1 (MSB = 1 was shifted out)
```

### Effect on Value

LSL effectively multiplies by 2 (for unsigned values):

| Input | Output | Multiplier | Notes |
|-------|--------|------------|-------|
| 0x01 | 0x02 | ×2 | 1 → 2 |
| 0x02 | 0x04 | ×2 | 2 → 4 |
| 0x40 | 0x80 | ×2 | 64 → 128 |
| 0x80 | 0x00 | Overflow | 128 → 0 (COUT = 1) |
| 0xFF | 0xFE | Overflow | 255 → 254 (COUT = 1) |

---

## Logical Shift Right (LSR)

**Opcode:** 00101 (binary: 00101, decimal: 5)  
**Operation:** OUT = A >> 1 (shift right by 1 bit)  
**Fill:** Leftmost bit filled with 0  
**Carry Out:** LSB shifted out becomes COUT

### Truth Table

| A (binary) | A (hex) | OUT (binary) | OUT (hex) | COUT | Description |
|------------|---------|--------------|-----------|------|-------------|
| 00000000 | 0x00 | 00000000 | 0x00 | 0 | Zero shifted |
| 00000010 | 0x02 | 00000001 | 0x01 | 0 | Shift 2 → 1 |
| 00000001 | 0x01 | 00000000 | 0x00 | 1 | LSB shifted out |
| 10000000 | 0x80 | 01000000 | 0x40 | 0 | MSB becomes 0 |
| 11111111 | 0xFF | 01111111 | 0x7F | 1 | All ones, LSB out |
| 10110001 | 0xB1 | 01011000 | 0x58 | 1 | LSB = 1, shifted out |
| 01000000 | 0x40 | 00100000 | 0x20 | 0 | MSB stays 0 |

### Examples

**Example 1:**
```
A = 0x0A (00001010)
LSR A = 0x05 (00000101)
COUT = 0 (LSB was 0)
```

**Example 2:**
```
A = 0x01 (00000001)
LSR A = 0x00 (00000000)
COUT = 1 (LSB = 1 was shifted out)
```

**Example 3:**
```
A = 0xB1 (10110001)
LSR A = 0x58 (01011000)
COUT = 1 (LSB = 1 was shifted out)
MSB changed from 1 to 0 (logical shift)
```

### Effect on Value

LSR effectively divides by 2 (for unsigned values):

| Input | Output | Divisor | Notes |
|-------|--------|---------|-------|
| 0x02 | 0x01 | ÷2 | 2 → 1 |
| 0x04 | 0x02 | ÷2 | 4 → 2 |
| 0x80 | 0x40 | ÷2 | 128 → 64 |
| 0x01 | 0x00 | Underflow | 1 → 0 (COUT = 1) |

---

## Arithmetic Shift Right (ASR)

**Opcode:** 00110 (binary: 00110, decimal: 6)  
**Operation:** OUT = A >> 1 (shift right with sign extension)  
**Fill:** Leftmost bit filled with original MSB (sign bit)  
**Carry Out:** LSB shifted out becomes COUT

### Truth Table

| A (binary) | A (hex) | A (signed) | OUT (binary) | OUT (hex) | OUT (signed) | COUT | Description |
|------------|---------|------------|--------------|-----------|--------------|------|-------------|
| 00000000 | 0x00 | 0 | 00000000 | 0x00 | 0 | 0 | Zero, sign bit 0 |
| 00000001 | 0x01 | +1 | 00000000 | 0x00 | 0 | 1 | Positive, LSB out |
| 01111111 | 0x7F | +127 | 00111111 | 0x3F | +63 | 1 | Max positive |
| 10000000 | 0x80 | -128 | 11000000 | 0xC0 | -64 | 0 | Min negative |
| 11000000 | 0xC0 | -64 | 11100000 | 0xE0 | -32 | 0 | Negative, sign extended |
| 11111111 | 0xFF | -1 | 11111111 | 0xFF | -1 | 1 | All ones, stays -1 |
| 10110001 | 0xB1 | -79 | 11011000 | 0xD8 | -40 | 1 | Negative, sign extended |

### Examples

**Example 1: Positive Number**
```
A = 0x42 (01000010) = +66 (signed)
ASR A = 0x21 (00100001) = +33 (signed)
COUT = 0 (LSB was 0)
MSB stays 0 (positive sign preserved)
```

**Example 2: Negative Number**
```
A = 0xB1 (10110001) = -79 (signed, 2's complement)
ASR A = 0xD8 (11011000) = -40 (signed, 2's complement)
COUT = 1 (LSB = 1 was shifted out)
MSB stays 1 (negative sign preserved)
```

**Example 3: Minimum Negative**
```
A = 0x80 (10000000) = -128 (signed)
ASR A = 0xC0 (11000000) = -64 (signed)
COUT = 0 (LSB was 0)
MSB preserved (negative sign)
```

### Effect on Signed Value

ASR effectively divides by 2 (for signed values, with sign extension):

| Input (signed) | Output (signed) | Divisor | Notes |
|----------------|-----------------|---------|-------|
| +66 (0x42) | +33 (0x21) | ÷2 | Positive, MSB = 0 |
| -79 (0xB1) | -40 (0xD8) | ÷2 | Negative, MSB = 1 |
| +127 (0x7F) | +63 (0x3F) | ÷2 | Max positive |
| -128 (0x80) | -64 (0xC0) | ÷2 | Min negative |
| -1 (0xFF) | -1 (0xFF) | ÷2 | Stays -1 (odd division) |

---

## Comparison of Shift Operations

| Operation | Direction | Fill Bit | Use Case | Example |
|-----------|-----------|----------|----------|---------|
| LSL | Left | 0 (rightmost) | Unsigned multiply by 2 | 0x05 → 0x0A |
| LSR | Right | 0 (leftmost) | Unsigned divide by 2 | 0x0A → 0x05 |
| ASR | Right | MSB (sign bit) | Signed divide by 2 | 0xB1 → 0xD8 |

### LSR vs ASR Difference

| Input | LSR Output | ASR Output | Difference |
|-------|------------|------------|------------|
| 0x80 (128 unsigned, -128 signed) | 0x40 (64) | 0xC0 (-64 signed) | LSR treats as unsigned |
| 0xB1 (177 unsigned, -79 signed) | 0x58 (88) | 0xD8 (-40 signed) | ASR preserves sign |
| 0x7F (127, both same) | 0x3F (63) | 0x3F (63) | Same for positive |

---

## Flag Generation for Shifts

### COUT Flag

COUT indicates the bit that was shifted out:

| Operation | Shifted Out Bit | COUT |
|-----------|----------------|------|
| LSL | A[7] (MSB) | A[7] |
| LSR | A[0] (LSB) | A[0] |
| ASR | A[0] (LSB) | A[0] |

### EQUAL Flag

EQUAL = 1 when result is zero:

| Operation | A | Result | EQUAL |
|-----------|---|--------|-------|
| LSL | 0x00 | 0x00 | 1 |
| LSL | 0x80 | 0x00 | 1 (wrap-around) |
| LSR | 0x00 | 0x00 | 1 |
| LSR | 0x01 | 0x00 | 1 |

### POSITIVE Flag

POSITIVE = 1 when result > 0 and MSB = 0:

| Operation | A | Result | POSITIVE |
|-----------|---|--------|----------|
| LSL | 0x05 | 0x0A | 1 (MSB = 0) |
| LSL | 0x80 | 0x00 | 0 (result is zero) |
| LSR | 0x0A | 0x05 | 1 (MSB = 0) |
| ASR | 0x42 | 0x21 | 1 (positive result) |
| ASR | 0xB1 | 0xD8 | 0 (MSB = 1, negative) |

---

**Last Updated:** 2026-01-16  
**See Also:** [Addition/Subtraction](add_sub.md) | [Logic Operations](logic_ops.md) | [Compare Operation](compare.md)
