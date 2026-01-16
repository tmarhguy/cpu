# Main ALU Board (270×270mm)

**Monolithic 8-bit ALU - Complete combinational processor on single PCB**

---

## Specifications

| Parameter | Value |
|-----------|-------|
| **Board Size** | 270mm × 270mm (10.6" × 10.6") |
| **Transistor Count** | 3,856+ discrete CMOS |
| **Architecture** | Pure combinational (no clock) |
| **Layers** | 2 (top signal/power, bottom ground) |
| **Power** | 5V @ 0.5-1A |
| **Propagation Delay** | ~445ns (worst case) |

---

## Functional Blocks

### Arithmetic Unit (Top-Left Quadrant)

**Components:**
- 8× 1-bit full adders (336T)
- 8× XOR gates for B input (96T)
- Carry chain routing

**Function:** A + B or A - B (via 2's complement)

**Signals:**
```
IN:  A[7:0], B[7:0], M
OUT: SUM[7:0], COUT
```

### Logic Unit (Top-Right Quadrant)

**Components:**
- NAND array (32T)
- NOR array (32T)
- XOR array (96T)
- PASS A/B buffers (32T)
- 5:1 MUX (160T)

**Function:** NAND, NOR, XOR, PASS A, PASS B operations

**Signals:**
```
IN:  A[7:0], B[7:0], LOGIC_SEL[2:0]
OUT: LOGIC_OUT[7:0]
```

### Selection & Output (Center)

**Components:**
- 2:1 MUX (160T) - arithmetic vs logic select
- Global inverter (16T)

**Function:** Select result and optionally invert

**Signals:**
```
IN:  ARITH[7:0], LOGIC[7:0], MUX_SEL, INV_OUT
OUT: RESULT[7:0]
```

### Flag Generation (Bottom-Left Quadrant)

**Components:**
- EQUAL comparator (~100T)
- LESS comparator (~120T)
- POSITIVE detector (~20T)

**Function:** Generate comparison and status flags

**Signals:**
```
IN:  A[7:0], B[7:0], OUT[7:0], COUT_IN
OUT: LESS, EQUAL, POSITIVE, COUT
```

### Control Decoder (Bottom-Right Quadrant)

**Components:**
- Combinational decode logic (~68T)

**Function:** FUNC[4:0] → control signals

**Signals:**
```
IN:  FUNC[4:0]
OUT: M, MUX_SEL, INV_OUT, LOGIC_SEL[2:0]
```

---

## Pinout

### Input Pins (22 total)

| Pin Group | Count | Description |
|-----------|-------|-------------|
| A[7:0] | 8 | First operand |
| B[7:0] | 8 | Second operand |
| FUNC[4:0] | 5 | Opcode |
| VCC | 1 | +5V power |
| GND | 1 | Ground (multiple connections) |

### Output Pins (12 total)

| Pin Group | Count | Description |
|-----------|-------|-------------|
| OUT[7:0] | 8 | Result |
| LESS | 1 | Less than flag |
| EQUAL | 1 | Equal flag |
| POSITIVE | 1 | Positive flag |
| COUT | 1 | Carry out flag |

---

## Fabrication

### Manufacturing Requirements

**PCB Specs:**
- **Size:** 270×270mm (**confirm manufacturer supports large format**)
- **Layers:** 2
- **Thickness:** 1.6mm
- **Copper:** 1oz (35µm)
- **Min trace/space:** 0.2mm/0.2mm
- **Surface finish:** HASL lead-free

**Cost:** ~$100 (large format premium)

### Assembly

**Component count:**
- 3,856+ transistors (NMOS/PMOS pairs)
- ~500 resistors (10kΩ pull-ups, 220Ω current limiting)
- ~50 capacitors (100nF decoupling)
- 2× 74HC157 ICs
- Headers, test points

**Estimated assembly time:** 50-70 hours (hand soldering)

---

## Testing

### Power-On Test

```
1. Visual inspection
2. Continuity: VCC, GND
3. Resistance: VCC-GND > 10kΩ
4. Power-on: Measure current < 200mA idle
5. Voltage: VCC = 5.0V ± 0.1V at all points
```

### Functional Test

```
Test ADD operation:
  FUNC = 00000
  A = 0x01
  B = 0x01
  Expected OUT = 0x02
  Measure with multimeter or logic analyzer
```

---

## References

- [Schematic](main_alu.kicad_sch) - Complete circuit
- [PCB Layout](main_alu.kicad_pcb) - Board layout
- [Architecture](../../../docs/ARCHITECTURE.md) - System design

---

**Status:** Design complete, fabrication-ready  
**Last Updated:** 2026-01-16
