# Logic Operations Truth Tables

> Truth tables for all logic operations supported by the ALU

The ALU implements 8 logic operations: AND, NAND, OR, NOR, XOR, XNOR, PASS A, and PASS B. Several operations are implemented efficiently using base operations with global inversion.

---

## Base Logic Operations

### NAND (Opcode: 01000)

**Operation:** OUT = ~(A & B)  
**Implementation:** Base operation (INV_OUT = 0)

| A | B | OUT | Description |
|---|---|-----|-------------|
| 0 | 0 | 1 | NAND(0,0) = 1 |
| 0 | 1 | 1 | NAND(0,1) = 1 |
| 1 | 0 | 1 | NAND(1,0) = 1 |
| 1 | 1 | 0 | NAND(1,1) = 0 |

**8-bit Example:**
| A (hex) | B (hex) | OUT (hex) | Description |
|---------|---------|-----------|-------------|
| 0xFF | 0x0F | 0xF0 | ~(0xFF & 0x0F) = ~0x0F = 0xF0 |
| 0xAA | 0x55 | 0xFF | ~(0xAA & 0x55) = ~0x00 = 0xFF |
| 0x00 | 0xFF | 0xFF | ~(0x00 & 0xFF) = ~0x00 = 0xFF |

---

### NOR (Opcode: 01001)

**Operation:** OUT = ~(A \| B)  
**Implementation:** Base operation (INV_OUT = 0)

| A | B | OUT | Description |
|---|---|-----|-------------|
| 0 | 0 | 1 | NOR(0,0) = 1 |
| 0 | 1 | 0 | NOR(0,1) = 0 |
| 1 | 0 | 0 | NOR(1,0) = 0 |
| 1 | 1 | 0 | NOR(1,1) = 0 |

**8-bit Example:**
| A (hex) | B (hex) | OUT (hex) | Description |
|---------|---------|-----------|-------------|
| 0xF0 | 0x0F | 0x00 | ~(0xF0 \| 0x0F) = ~0xFF = 0x00 |
| 0xAA | 0x55 | 0x00 | ~(0xAA \| 0x55) = ~0xFF = 0x00 |
| 0x00 | 0x00 | 0xFF | ~(0x00 \| 0x00) = ~0x00 = 0xFF |

---

### XOR (Opcode: 01010)

**Operation:** OUT = A ^ B  
**Implementation:** Base operation (INV_OUT = 0)

| A | B | OUT | Description |
|---|---|-----|-------------|
| 0 | 0 | 0 | XOR(0,0) = 0 |
| 0 | 1 | 1 | XOR(0,1) = 1 |
| 1 | 0 | 1 | XOR(1,0) = 1 |
| 1 | 1 | 0 | XOR(1,1) = 0 |

**8-bit Example:**
| A (hex) | B (hex) | OUT (hex) | Description |
|---------|---------|-----------|-------------|
| 0xAA | 0x55 | 0xFF | 0xAA ^ 0x55 = 0xFF (bitwise XOR) |
| 0xFF | 0xFF | 0x00 | 0xFF ^ 0xFF = 0x00 |
| 0x12 | 0x34 | 0x26 | 0x12 ^ 0x34 = 0x26 |

---

### PASS A (Opcode: 01011)

**Operation:** OUT = A  
**Implementation:** Base operation, passes A unchanged

| A (hex) | OUT (hex) | Description |
|---------|-----------|-------------|
| 0x00 | 0x00 | Pass 0 unchanged |
| 0xFF | 0xFF | Pass maximum value |
| 0x42 | 0x42 | Pass arbitrary value |

---

### PASS B (Opcode: 01100)

**Operation:** OUT = B  
**Implementation:** Base operation, passes B unchanged

| B (hex) | OUT (hex) | Description |
|---------|-----------|-------------|
| 0x00 | 0x00 | Pass 0 unchanged |
| 0xFF | 0xFF | Pass maximum value |
| 0x23 | 0x23 | Pass arbitrary value |

---

## Derived Logic Operations (via INV_OUT)

These operations use base operations with global inversion enabled (INV_OUT = 1).

### AND (Opcode: 01101)

**Operation:** OUT = A & B  
**Implementation:** NOT(NAND(A, B))

**1-bit Truth Table:**
| A | B | NAND | AND (inverted) |
|---|---|------|----------------|
| 0 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

**8-bit Examples:**
| A (hex) | B (hex) | NAND Result | AND Result | Description |
|---------|---------|-------------|------------|-------------|
| 0xFF | 0x0F | 0xF0 | 0x0F | 0xFF & 0x0F = 0x0F |
| 0xAA | 0x55 | 0xFF | 0x00 | 0xAA & 0x55 = 0x00 |
| 0x12 | 0x34 | 0xED | 0x10 | 0x12 & 0x34 = 0x10 |

---

### OR (Opcode: 01110)

**Operation:** OUT = A \| B  
**Implementation:** NOT(NOR(A, B))

**1-bit Truth Table:**
| A | B | NOR | OR (inverted) |
|---|---|-----|---------------|
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 |

**8-bit Examples:**
| A (hex) | B (hex) | NOR Result | OR Result | Description |
|---------|---------|------------|-----------|-------------|
| 0xF0 | 0x0F | 0x00 | 0xFF | 0xF0 \| 0x0F = 0xFF |
| 0xAA | 0x55 | 0x00 | 0xFF | 0xAA \| 0x55 = 0xFF |
| 0x12 | 0x34 | 0xE9 | 0x36 | 0x12 \| 0x34 = 0x36 |

---

### XNOR (Opcode: 01111)

**Operation:** OUT = ~(A ^ B)  
**Implementation:** NOT(XOR(A, B))

**1-bit Truth Table:**
| A | B | XOR | XNOR (inverted) |
|---|---|-----|-----------------|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

**8-bit Examples:**
| A (hex) | B (hex) | XOR Result | XNOR Result | Description |
|---------|---------|------------|-------------|-------------|
| 0xAA | 0x55 | 0xFF | 0x00 | ~(0xAA ^ 0x55) = 0x00 |
| 0xFF | 0xFF | 0x00 | 0xFF | ~(0xFF ^ 0xFF) = 0xFF |
| 0x12 | 0x34 | 0x26 | 0xD9 | ~(0x12 ^ 0x34) = 0xD9 |

---

### NOT A (Opcode: 10001)

**Operation:** OUT = ~A  
**Implementation:** NOT(PASS A)

| A (hex) | PASS A Result | NOT A Result | Description |
|---------|---------------|--------------|-------------|
| 0x00 | 0x00 | 0xFF | Invert all zeros to all ones |
| 0xFF | 0xFF | 0x00 | Invert all ones to all zeros |
| 0xAA | 0xAA | 0x55 | Invert bit pattern |
| 0x42 | 0x42 | 0xBD | Invert arbitrary value |

---

### NOT B (Opcode: 10010)

**Operation:** OUT = ~B  
**Implementation:** NOT(PASS B)

| B (hex) | PASS B Result | NOT B Result | Description |
|---------|---------------|--------------|-------------|
| 0x00 | 0x00 | 0xFF | Invert all zeros to all ones |
| 0xFF | 0xFF | 0x00 | Invert all ones to all zeros |
| 0x55 | 0x55 | 0xAA | Invert bit pattern |
| 0x23 | 0x23 | 0xDC | Invert arbitrary value |

---

## Operation Summary Table

| Opcode | Operation | Base Operation | INV_OUT | Truth Table Size |
|--------|-----------|----------------|---------|------------------|
| 01000 | NAND | NAND | 0 | 2^2 = 4 rows |
| 01001 | NOR | NOR | 0 | 2^2 = 4 rows |
| 01010 | XOR | XOR | 0 | 2^2 = 4 rows |
| 01011 | PASS A | PASS A | 0 | 2^8 = 256 values |
| 01100 | PASS B | PASS B | 0 | 2^8 = 256 values |
| 01101 | AND | NAND | 1 | Derived from NAND |
| 01110 | OR | NOR | 1 | Derived from NOR |
| 01111 | XNOR | XOR | 1 | Derived from XOR |
| 10001 | NOT A | PASS A | 1 | Derived from PASS A |
| 10010 | NOT B | PASS B | 1 | Derived from PASS B |

---

## Bitwise Operation Examples

### Pattern Recognition

| Operation | A | B | Result | Pattern |
|-----------|---|---|--------|---------|
| AND | 0xFF | 0x0F | 0x0F | Mask lower nibble |
| OR | 0xF0 | 0x0F | 0xFF | Combine nibbles |
| XOR | 0xAA | 0x55 | 0xFF | Invert alternating |
| NAND | 0xFF | 0x0F | 0xF0 | Mask complement |
| NOR | 0xF0 | 0x0F | 0x00 | Both set = 0 |

---

**Last Updated:** 2026-01-16  
**See Also:** [Addition/Subtraction](add_sub.md) | [Shift Operations](shifts.md) | [Compare Operation](compare.md)
