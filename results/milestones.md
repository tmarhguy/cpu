<div align="center">

# Schematics & ALU Simulation Metrics

**Schematic design files and simulation models for the ALU system**

</div>

---

## Table of Contents

- [ALU Simulation Metrics](#alu-simulation-metrics)
- [Circuit Designs](#circuit-designs)
- [Transistor Count Analysis](#transistor-count-analysis)
- [Component Inventory](#component-inventory)
- [Supported Operations](#supported-operations)

---

## ALU Simulation Metrics

### Project Overview

Complete 8-bit Arithmetic Logic Unit designed in **Logisim Evolution 4.0.0**, built from discrete transistor-level components with 74xx IC integration for complex functions.

**File:** `alusimulation.circ`  
**Total Lines:** 2,120 lines of XML  
**Components:** 150+ discrete components  
**Total Discrete Transistors:** **3,856 transistors**

---

### Component Inventory

#### Logic Gates (Discrete Transistors)

| Gate Type | Count | Width | Total Units | Transistors | Purpose |
|-----------|-------|-------|-------------|-------------|---------|
| NOT | 41 | 1-bit (40), 8-bit (1) | 48 units | 96 | Inversions, control logic |
| AND | 26 | 2-in (8), 3-in (1), 4-in (17) | 26 gates | 226 | Control decoding, masking |
| OR | 8 | 2-in (6), 3-in (1) | 8 gates | 44 | Control logic, flags |
| NOR | 3 | 2-in (1), 8-in (2) | 3 gates | 40 | Zero detection |
| NAND | 1 | 8-bit | 1 gate | 32 | Logic operations |
| XOR | 3 | 8-bit | 3 gates | N/A | **74xx IC (74HC86)** |

#### Multiplexers (74xx ICs)

| Type | Count | Width | Select | Transistors | IC Recommendation |
|------|-------|-------|--------|-------------|-------------------|
| 8:1 MUX | 1 | 8-bit | 3-bit | 1,206 | 74HC151 (×8) |
| 4:1 MUX | 3 | 8-bit | 2-bit | 1,668 | 74HC153 (×12) |
| 2:1 MUX | 2 | 8-bit | 1-bit | 320 | 74HC157 (×8) |

#### Arithmetic Components

| Component | Width | Implementation | Transistors |
|-----------|-------|----------------|-------------|
| Full Adder | 8-bit | Discrete (ripple-carry) | 224 |
| Bit Extender | 1→8 bit | Wire replication | 0 |

---

### Transistor Count Breakdown

```
NOT Gates:         96 transistors (48 units × 2)
AND Gates:        226 transistors (mixed 2/3/4-input)
OR Gates:          44 transistors (2/3-input)
NOR Gates:         40 transistors (2/8-input)
NAND Gates:        32 transistors (8-bit width)
8-bit Adder:      224 transistors (8 × 28 per bit)
Multiplexers:   3,194 transistors (all MUX circuits)
─────────────────────────────────────────────────
TOTAL:          3,856 DISCRETE TRANSISTORS
═════════════════════════════════════════════════

PLUS: 24 XOR gates implemented as 74HC86 ICs (not counted)
```

---

### Supported Operations (18+ Operations)

#### Arithmetic (8 operations)
- **ADD** - A + B
- **SUB** - A - B (2's complement)
- **INC** - A + 1
- **DEC** - A - 1
- **LSL** - Logical Shift Left
- **LSR** - Logical Shift Right
- **ASR** - Arithmetic Shift Right
- **REV_A** - Bit reverse A

#### Logic (8 operations)
- **AND** - A AND B
- **NAND** - A NAND B
- **OR** - A OR B
- **NOR** - A NOR B
- **XOR** - A XOR B
- **XNOR** - A XNOR B
- **PASS_A** - Output A
- **PASS_B** - Output B

#### Special (3+ operations)
- **CMP** - Compare (A - B with flags)
- **NOT_A** - Invert A
- **NOT_B** - Invert B

---

### Signal Specifications

**Inputs:**
- `A_IN`, `B_IN` (8-bit each) - Primary operands
- `CTRL` (5-bit) - Operation selector (32 opcodes)
- `C_IN` (1-bit) - Carry input
- `M` (1-bit) - Add/Sub mode

**Outputs:**
- `OVERALL` (8-bit) - Final ALU result
- `SUM` (8-bit) - Arithmetic result
- `LOGIC_OUT` (8-bit) - Logic result
- `C_OUT` (1-bit) - Carry/Borrow flag
- `EQUAL_FL`, `LESS_FL`, `GREAT_FL` (1-bit each) - Comparison flags
- `LSL`, `LSR`, `ASR`, `REV_A` (8-bit each) - Shift results

---

### Performance Estimates

| Metric | Value | Notes |
|--------|-------|-------|
| **Propagation Delay** | ~20 gate levels | Through ripple-carry adder |
| **Max Frequency** | ~5-10 MHz | With 74HC series logic |
| **Power (5V, 1MHz)** | ~140 mW | Estimated dynamic power |
| **Physical Size** | 20-25 breadboards | If built discretely |
| **Assembly Time** | 200-300 hours | For physical construction |

---

### Recommended Bill of Materials (BOM)

For physical implementation using hybrid discrete/IC approach:

| Component | Type | Quantity | Purpose |
|-----------|------|----------|---------|
| 74HC86 | Quad XOR | 6 | XOR operations |
| 74HC151 | 8:1 MUX | 8 | Logic selection |
| 74HC153 | Dual 4:1 MUX | 12 | Arithmetic/shift routing |
| 74HC157 | Quad 2:1 MUX | 8 | Final output selection |
| 74HC08 | Quad AND | 10 | AND operations |
| 74HC32 | Quad OR | 5 | OR operations |
| 74HC04 | Hex Inverter | 8 | NOT operations |
| 74HC02 | Quad NOR | 2 | NOR operations |
| 2N2222 | NPN Transistor | ~3,900 | Full discrete option |
| Resistors | 10kΩ, 1kΩ | ~4,000 | Pull-up/down, current limiting |

---

<div align="center">

## Circuit Designs

</div>

### 1-Bit Half Adder

<table>
<tr>
<td width="50%">

**Circuit Components**
- Two input lines: A and B
- AND gate: inputs A and B, output labeled 'out'
- XOR gate: inputs A and B, output labeled 'carry out'

</td>
<td width="50%">

**Truth Table**
- Includes values: 0, 1, 00, 01, 11, 10
- Validates sum and carry outputs

</td>
</tr>
</table>

---

### 1-Bit Full Adder

<table>
<tr>
<td width="50%">

**Truth Table and K-Map**
- Inputs: A, B, $C_{in}$
- Output: $A + B + C_{in}$
- K-maps used to derive logic expressions

</td>
<td width="50%">

**Derived Formulas**
- **Sum:** $A \oplus B \oplus C$
- **Carry:** $ABC + ABC + ABC + ABC$
- Simplified to: $AB + BC + AC$

</td>
</tr>
</table>

---

### Carry Circuit

<table>
<tr>
<td width="50%">

**Design**
- Implements $AB + BC + AC$ carry logic
- Standard carry generation circuit

</td>
<td width="50%">

**Simulation Example**
- **Inputs:** `101` (A=1, B=0, C=1)
- **Output:** Carry = 1
- Circuit path highlighted in simulation

</td>
</tr>
</table>

---

### Sum Circuit

<table>
<tr>
<td width="50%">

**Design**
- Two XOR gates in cascade
- Implements $A \oplus B \oplus C$

</td>
<td width="50%">

**Simulation Example**
- **Inputs:** `100` (A=1, B=0, C=0)
- **Output:** Sum = 1
- Circuit path highlighted in simulation

</td>
</tr>
</table>

---

### 8-Bit Ripple-Carry Adder

<table>
<tr>
<td width="50%">

**Architecture**
- Chaining carry-out from one stage ($C_0, C_1, \ldots, C_7$) to carry-in of next
- Sequential propagation through all stages

</td>
<td width="50%">

**Outputs**
- Produces $S[0]$ through $S[7]$
- Final carry-out: $C_8$ or $C_{final}$

</td>
</tr>
</table>

---

### Logic with Control Signal (XOR Design)

<table>
<tr>
<td width="50%">

**Block Diagram Components**
- Inputs: A, B, Control signal, $C_{in}$
- Outputs: Sum, carry-out
- Control unit (black box) takes 4-bit CT. Sig

</td>
<td width="50%">

**Control Unit Outputs**
- 1-bit to adder (as $C_{in}$)
- 8-bit signal to XOR gates
- Coordinates ADD/SUB operations

</td>
</tr>
</table>

---

<div align="center">

## Directory Structure

</div>

<table>
<tr>
<td width="50%">

### `ltspice/`
LTSpice simulation files

## Supported Operations (19 Instructions)

Complete instruction set with opcodes and implementation status:

| Opcode (Dec) | Opcode (Binary) | Function | Description | Circuit Status |
|--------------|-----------------|----------|-------------|----------------|
| 00000 | `00000` | **ADD** | A + B | ✅ TRUE |
| 00001 | `00001` | **SUB** | A - B (2's complement) | ✅ TRUE |
| 00002 | `00010` | **INC A** | A + 1 | ✅ TRUE |
| 00003 | `00011` | **DEC A** | A - 1 | ✅ TRUE |
| 00004 | `00100` | **LSL / SLL** | Shift left logical | ✅ TRUE |
| 00005 | `00101` | **LSR / SRL** | Shift right logical | ✅ TRUE |
| 00006 | `00110` | **ASR** | Arithmetic shift right | ✅ TRUE |
| 00007 | `00111` | **REV A** | Bit reverse A | ✅ TRUE |
| 00008 | `01000` | **NAND** | A NAND B | ✅ TRUE |
| 00009 | `01001` | **NOR** | A NOR B | ✅ TRUE |
| 00010 | `01010` | **XOR** | A XOR B | ✅ TRUE |
| 00011 | `01011` | **PASS A** | Output A | ✅ TRUE |
| 00012 | `01100` | **PASS B** | Output B | ✅ TRUE |
| 00013 | `01101` | **AND** | NAND + invert | ✅ TRUE |
| 00014 | `01110` | **OR** | NOR + invert | ✅ TRUE |
| 00015 | `01111` | **XNOR** | XOR + invert | ✅ TRUE |
| 00016 | `10000` | **CMP** | A - B, flags only | ✅ TRUE |
| 00017 | `10001` | **NOT A** | Invert A | ✅ TRUE |
| 00018 | `10010` | **NOT B** | Invert B | ✅ TRUE |

#### Instruction Categories

**Arithmetic Operations (8):**
- ADD, SUB, INC A, DEC A, LSL, LSR, ASR, REV A

**Logic Operations (8):**
- AND, NAND, OR, NOR, XOR, XNOR, PASS A, PASS B

**Special Operations (3):**
- CMP, NOT A, NOT B

**Total: 19 fully implemented instructions** across 32 possible opcodes (5-bit control)

**Simulations**
- 1-bit adder simulations
- Gate-level simulations
- 8-bit slice simulations
- Timing analysis
- Carry circuit simulation (inputs: 101)
- Sum circuit simulation (inputs: 100)

</td>
<td width="50%">

### `kicad/`
KiCad schematic and PCB files

**Contents**
- Main ALU schematic
- PCB layouts
- Library files
- Manufacturing outputs

</td>
</tr>
</table>

---

<div align="center">

## Simulation Milestones

</div>

<table>
<tr>
<td width="33%">

**1. 1-Bit Half Adder**
- Circuit diagram with AND and XOR gates
- Truth table validation

</td>
<td width="33%">

**2. 1-Bit Full Adder**
- Truth table + K-map analysis
- Logic expression derivation

</td>
<td width="33%">

**3. Carry Circuit**
- Design implementation
- Simulation with test case (A=1, B=0, C=1)

</td>
</tr>
<tr>
<td width="33%">

**4. Sum Circuit**
- Two XOR gate cascade
- Simulation with test case (A=1, B=0, C=0)

</td>
<td width="33%">

**5. 8-Bit Ripple Adder**
- Propagation delay analysis
- Full-width simulation

</td>
<td width="33%">

**6. System-Level**
- Full datapath simulation
- Control unit integration

</td>
</tr>
</table>
