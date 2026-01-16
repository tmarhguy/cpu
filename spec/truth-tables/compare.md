# Compare Operation Truth Tables

> Truth tables for comparison operations and flag generation

The CMP operation compares two 8-bit operands (A and B) and sets flags based on the relationship between them. The operation performs A - B internally but does not produce an output result.

---

## Overview

**Opcode:** 10000 (binary: 10000, decimal: 16)  
**Operation:** Compare A and B (flags only, no output)  
**Implementation:** Performs A - B internally to determine relationship

---

## Flag Generation Truth Table

The CMP operation sets four flags based on the comparison result:

| A (dec) | B (dec) | A - B | LESS | EQUAL | POSITIVE | COUT | Description |
|---------|---------|-------|------|-------|----------|------|-------------|
| 0 | 0 | 0 | 0 | 1 | 0 | 1 | A == B (equal) |
| 0 | 1 | 255 | 1 | 0 | 0 | 0 | A < B (borrow occurred) |
| 1 | 0 | 1 | 0 | 0 | 1 | 1 | A > B (no borrow) |
| 1 | 1 | 0 | 0 | 1 | 0 | 1 | A == B (equal) |
| 5 | 5 | 0 | 0 | 1 | 0 | 1 | A == B (equal) |
| 10 | 5 | 5 | 0 | 0 | 1 | 1 | A > B |
| 5 | 10 | 251 | 1 | 0 | 0 | 0 | A < B (borrow occurred) |
| 100 | 35 | 65 | 0 | 0 | 1 | 1 | A > B |
| 35 | 100 | 191 | 1 | 0 | 0 | 0 | A < B |
| 255 | 1 | 254 | 0 | 0 | 0 | 1 | A > B (wrap-around) |
| 1 | 255 | 2 | 1 | 0 | 1 | 0 | A < B (wrap-around) |
| 128 | 128 | 0 | 0 | 1 | 0 | 1 | A == B (equal) |
| 127 | 128 | 255 | 1 | 0 | 0 | 0 | A < B |
| 128 | 127 | 1 | 0 | 0 | 1 | 1 | A > B |

---

## Flag Logic

### EQUAL Flag

**Condition:** EQUAL = 1 when A == B (result of A - B is zero)

| A[7:0] | B[7:0] | Result | EQUAL |
|--------|--------|--------|-------|
| 0x00 | 0x00 | 0x00 | 1 |
| 0xFF | 0xFF | 0x00 | 1 |
| 0x42 | 0x42 | 0x00 | 1 |
| 0x01 | 0x00 | 0x01 | 0 |
| 0x00 | 0x01 | 0xFF | 0 |

**Implementation:** 8-bit XOR array + 8-input NOR gate

```
EQUAL = ~((A[7] XOR B[7]) | (A[6] XOR B[6]) | ... | (A[0] XOR B[0]))
```

### LESS Flag

**Condition:** LESS = 1 when A < B (unsigned comparison, borrow occurred)

| A (dec) | B (dec) | LESS | COUT | Logic |
|---------|---------|------|------|-------|
| 0 | 1 | 1 | 0 | A < B, borrow occurred |
| 1 | 0 | 0 | 1 | A > B, no borrow |
| 10 | 20 | 1 | 0 | A < B |
| 50 | 10 | 0 | 1 | A > B |
| 5 | 5 | 0 | 1 | A == B (no borrow) |

**Implementation:** LESS = ~COUT when A != B

**Logic:**
```
LESS = (A < B) unsigned
      = (A - B) borrow occurred
      = ~COUT when A != B
```

### POSITIVE Flag

**Condition:** POSITIVE = 1 when result > 0 (not zero and MSB = 0)

| A - B | Result | POSITIVE | EQUAL |
|-------|--------|----------|-------|
| 0 | 0x00 | 0 | 1 |
| 5 | 0x05 | 1 | 0 |
| 255 | 0xFF | 0 | 0 (negative in 2's complement interpretation) |

**Implementation:** POSITIVE = ~OUT[7] AND ~EQUAL

**Logic:**
```
POSITIVE = (A - B > 0)
          = (OUT != 0) AND (OUT[7] == 0)
          = ~EQUAL AND ~OUT[7]
```

### COUT Flag

**Condition:** COUT = 1 when no borrow occurred (A >= B)

| A (dec) | B (dec) | COUT | LESS |
|---------|---------|------|------|
| 10 | 5 | 1 | 0 |
| 5 | 10 | 0 | 1 |
| 5 | 5 | 1 | 0 |
| 0 | 0 | 1 | 0 |

**Implementation:** Direct connection from subtractor carry-out

**Logic:**
```
COUT = Carry-out from MSB of A - B
     = 1 when A >= B (no borrow)
     = 0 when A < B (borrow occurred)
```

---

## Comparison Examples

### Example 1: Equal Values

```
CMP A=50, B=50
  Operation: 50 - 50 = 0
  Result: 0x00
  Flags:
    EQUAL = 1    (result is zero)
    LESS = 0     (no borrow)
    POSITIVE = 0 (result is zero, not positive)
    COUT = 1     (no borrow occurred)
```

### Example 2: A Greater Than B

```
CMP A=100, B=35
  Operation: 100 - 35 = 65
  Result: 0x41
  Flags:
    EQUAL = 0     (result not zero)
    LESS = 0      (no borrow)
    POSITIVE = 1  (result > 0, MSB = 0)
    COUT = 1      (no borrow occurred)
```

### Example 3: A Less Than B

```
CMP A=10, B=50
  Operation: 10 - 50 = 236 (unsigned)
  Result: 0xEC
  Flags:
    EQUAL = 0     (result not zero)
    LESS = 1      (borrow occurred, A < B)
    POSITIVE = 0  (result MSB = 1)
    COUT = 0      (borrow occurred)
```

### Example 4: Edge Case - Maximum Values

```
CMP A=255, B=255
  Operation: 255 - 255 = 0
  Result: 0x00
  Flags:
    EQUAL = 1     (A == B)
    LESS = 0
    POSITIVE = 0
    COUT = 1
```

```
CMP A=255, B=1
  Operation: 255 - 1 = 254
  Result: 0xFE
  Flags:
    EQUAL = 0
    LESS = 0      (255 > 1, no borrow)
    POSITIVE = 0  (MSB = 1)
    COUT = 1
```

---

## Flag Combinations

| Condition | EQUAL | LESS | POSITIVE | COUT | Interpretation |
|-----------|-------|------|----------|------|----------------|
| A == B | 1 | 0 | 0 | 1 | Equal |
| A > B | 0 | 0 | 1 | 1 | Greater (no borrow) |
| A < B | 0 | 1 | 0 | 0 | Less (borrow occurred) |

**Note:** EQUAL and LESS cannot both be 1. POSITIVE is 1 only when A > B (result is positive).

---

## Implementation Notes

The CMP operation uses the same subtractor circuit as SUB, but:
- The output bus (OUT[7:0]) is not used/valid
- Only the flags are meaningful
- The internal computation is identical to SUB operation
- Flags are generated based on the subtraction result

**Circuit:** Same as SUB operation (A + ~B + 1)  
**Output:** Flags only, OUT[7:0] is undefined

---

**Last Updated:** 2026-01-16  
**See Also:** [ALU Specification](../alu-spec.md) | [Opcode Table](../opcode/opcode_table.md)
