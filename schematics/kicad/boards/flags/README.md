# Flags Generation Board

**Comparison and status flag generation**

---

## Function

Generate 4 flags for ALU status and comparison:
- **LESS:** A < B (magnitude comparison)
- **EQUAL:** A == B (equality check)
- **POSITIVE:** OUT > 0 (positive result)
- **COUT:** Carry out (from adder)

---

## Schematic

![Flags Schematic](../../../../media/schematics photos svg/flags.svg)
*Flags generation circuit*

---

## Flag Implementations

### EQUAL Flag (~100T)

**Function:** Detect A == B

**Logic:**
```
EQUAL = ~((A[7] XOR B[7]) | (A[6] XOR B[6]) | ... | (A[0] XOR B[0]))
```

**Implementation:**
- 8× XOR gates (96T)
- 8-input NOR gate (16T)

### LESS Flag (~120T)

**Function:** Detect A < B

**Logic:** Cascaded priority comparison (MSB first)

**Implementation:** ~120T comparator logic

### POSITIVE Flag (~20T)

**Function:** Detect OUT > 0

**Logic:**
```
NOT_ZERO = OUT[7] | ... | OUT[0]
POSITIVE = ~OUT[7] & NOT_ZERO
```

### COUT Flag (0T)

**Function:** Pass carry from adder

**Implementation:** Direct wire

---

## Signals

**Inputs:**
- A[7:0], B[7:0] - For comparison
- OUT[7:0] - For POSITIVE detection
- COUT_IN - From adder

**Outputs:**
- LESS, EQUAL, POSITIVE, COUT

---

**Last Updated:** 2026-01-16
