# Add/Subtract Module

**8-bit adder with conditional B inversion for subtraction**

---

## Function

Implements both addition and subtraction using a single 8-bit ripple-carry adder.

**Operations:**
- ADD: OUT = A + B (when M=0)
- SUB: OUT = A - B (when M=1, using 2's complement)

---

## Block Diagram

```
A[7:0] ────────────────┐
                       ├──> Full Adder (8-bit) ──> SUM[7:0]
B[7:0] ──> XOR[M] ─────┤
                       │
M ──────────────> Cin ─┘
```

---

## Implementation

### XOR Array (96T)

**Purpose:** Conditional B inversion

```
B'[i] = B[i] XOR M  (for i = 0 to 7)
```

**Truth table:**
| M | B | B' |
|---|---|----|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

When M=0 (ADD): B' = B  
When M=1 (SUB): B' = ~B

### 8-Bit Ripple-Carry Adder (336T)

**Structure:** 8 cascaded full adders

**Per full adder (42T):**
- Sum = A ⊕ B' ⊕ Cin
- Cout = A·B' + Cin·(A ⊕ B')

---

## Schematic

![Add/Sub Schematic](../../../../media/schematics photos svg/add_sub.svg)
*Complete add/subtract module schematic*

> **Evidence:** Schematic shows XOR array and 8-bit adder.

---

## PCB

![Add/Sub PCB](../../../../media/pcb photos/add_sub.png)
*Fabricated add/subtract board*

> **Evidence:** Physical implementation of arithmetic unit.

---

## Signals

### Inputs

| Signal | Width | Voltage | Description |
|--------|-------|---------|-------------|
| A[7:0] | 8 bits | 0V/5V | First operand |
| B[7:0] | 8 bits | 0V/5V | Second operand |
| M | 1 bit | 0V/5V | ADD(0) or SUB(1) mode |
| VCC | Power | 5V | Power supply |
| GND | Power | 0V | Ground |

### Outputs

| Signal | Width | Voltage | Description |
|--------|-------|---------|-------------|
| SUM[7:0] | 8 bits | 0V/5V | Arithmetic result |
| COUT | 1 bit | 0V/5V | Carry out (unsigned overflow) |

---

## Timing

**Propagation delay:**
- XOR array: ~15ns
- Adder (worst case): ~400ns
- **Total:** ~415ns (input to output)

**Critical path:** A[0] → XOR → FA0 → FA1 → ... → FA7 → SUM[7]

---

## Testing

**Test vectors:**

| A | B | M | Expected SUM | Expected COUT |
|---|---|---|--------------|---------------|
| 0x01 | 0x01 | 0 | 0x02 | 0 |
| 0xFF | 0x01 | 0 | 0x00 | 1 |
| 0x64 | 0x23 | 1 | 0x41 | 1 |
| 0x00 | 0x01 | 1 | 0xFF | 0 |

---

**Last Updated:** 2026-01-16
