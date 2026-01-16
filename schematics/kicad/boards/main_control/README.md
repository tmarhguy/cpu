# Control Decoder Board

**5-bit opcode decoder generating internal control signals**

---

## Function

Decode FUNC[4:0] opcode into internal control signals for ALU operation.

---

## Schematic

![Control Schematic](../../../../media/schematics photos svg/main_control.svg)
*Control unit opcode decoder*

---

## Control Signal Generation

### Decode Table

| FUNC[4:0] | M | MUX_SEL | INV_OUT | LOGIC_SEL |
|-----------|---|---------|---------|-----------|
| 00000 (ADD) | 0 | 0 | 0 | xxx |
| 00001 (SUB) | 1 | 0 | 0 | xxx |
| 01000 (NAND) | x | 1 | 0 | 000 |
| 01101 (AND) | x | 1 | 1 | 000 |

See [docs/OPCODE_TABLE.md](../../../../docs/OPCODE_TABLE.md) for complete table.

---

## Signals

**Inputs:**
- FUNC[4:0] - 5-bit opcode

**Outputs:**
- M - ADD/SUB mode
- MUX_SEL - Arithmetic(0) / Logic(1)
- INV_OUT - Global inversion enable
- LOGIC_SEL[2:0] - Logic operation select

---

## Implementation

**Transistor count:** ~68T

**Combinational decode logic** - no clock required

---

**Last Updated:** 2026-01-16
