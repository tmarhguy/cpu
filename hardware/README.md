<div align="center">

# Hardware Design

**Complete hardware design files including schematics, PCB layouts, and manufacturing outputs**

</div>

---

<div align="center">

## ALU Architecture

</div>

### 1-Bit Half Adder

<table>
<tr>
<td width="50%">

**Inputs**
- A
- B

</td>
<td width="50%">

**Outputs**
- Sum (out): $A \oplus B$
- Carry-out: $A \cdot B$

</td>
</tr>
</table>

---

### 1-Bit Full Adder

<table>
<tr>
<td width="50%">

**Inputs**
- A
- B
- $C_{in}$

**Outputs**
- **Sum:** $A \oplus B \oplus C$
- **Carry:** $AB + BC + AC$ (standard)
- **Carry (optimized):** $AB + C(A \oplus B)$

</td>
<td width="50%">

**Design Cost**

| Component | Cost |
|-----------|------|
| Standard Carry | $3 \cdot AND + 1 \cdot OR = 30T$ |
| Optimized Carry | $2 \cdot AND + 1 \cdot OR + 1 \cdot XOR = 30T$ |
| Sum | $3 \cdot XOR = 36T$ |
| **Total** | **66T** |

</td>
</tr>
</table>

---

### 8-Bit Full Adder

<table>
<tr>
<td width="50%">

**Inputs**
- 8-bit Input $A[7:0]$
- 8-bit Input $B[7:0]$

**Outputs**
- 8-bit output $S[7:0]$
- 1-bit carry (1 if overflow)

</td>
<td width="50%">

**Implementation**
- Ripple-carry adder architecture
- Chaining carry-out ($C_0, C_1, \ldots, C_7$) to carry-in of next stage
- Final carry: $C_8$ or $C_{final}$

</td>
</tr>
</table>

---

### ADD/SUB Implementation

<table>
<tr>
<td width="50%">

**Operations**
- **ADD:** $A + B$
- **SUB:** $A - B = A + (-B)$ (2's complement)

**Design Approach**
- XOR-based implementation (instead of dedicated MUX)
- Control signal feeds XOR gates:
  - $B \oplus 0 = B$
  - $B \oplus 1 = \overline{B}$

</td>
<td width="50%">

**Control Signals**
- **ADD:** `00000000` (8-bit)
- **SUB:** `11111111` (8-bit)
- Control bit (1-bit) feeds ALU as $C_{in}$ to complete 2's complement

**Cost Comparison**
- XOR design: $8 \cdot 12 = 96T$
- MUX design: $138T$
- **Savings:** $42T$ (30% reduction)

</td>
</tr>
</table>

---

### Control Unit

<table>
<tr>
<td width="50%">

**Input**
- 4-bit control signal (CT. Sig)
- Allows $2^{4} = 16$ possible operations

**Outputs**
- 1-bit to adder (as $C_{in}$)
- 8-bit signal of 1s or 0s to XOR gates

</td>
<td width="50%">

**Purpose**
- Process different operators with decoder
- Coordinate ALU operations

**Future Operations**
- Currently: ADD, SUB
- Planned: MUL (multiplication), DIV (divide)
- Logical operations support

</td>
</tr>
</table>

---

<div align="center">

## Transistor Costs

</div>

<table>
<tr>
<td width="50%">

### Gate Costs

| Gate | Transistor Count |
|------|------------------|
| NOT | 2T |
| NOR | 4T |
| NAND | 4T |
| OR | 6T |
| AND | 6T |
| XOR | 12T |
| XNOR | (not specified) |

</td>
<td width="50%">

### Design Principles

**Optimization Rules**
- Best design: $(n-1)$ MOSFETs for $n$ input
- $n$-AND = $(n-1)$ NAND + $n$-OR = $(n-1)$ OR NOT

**Cost Analysis**
- Full adder total: **66T**
- 8-bit XOR design: **96T**
- MUX alternative: **138T**

</td>
</tr>
</table>

---

<div align="center">

## Directory Structure

</div>

<table>
<tr>
<td width="33%">

### `alu/`
ALU core design
- **`full-adder/`**: 1-bit full adder implementation
- **`logic-circuits/`**: Logic gate implementations

</td>
<td width="33%">

### `control-unit/`
Control unit design
- **`input-control/`**: Input control logic
- **`output-control/`**: Output control logic

</td>
<td width="33%">

### `power_supply/`
Power distribution board
- 5V regulation
- Decoupling network
- Star ground distribution

</td>
</tr>
</table>

---

<div align="center">

## Design Specifications

</div>

<table>
<tr>
<td width="50%">

**Logic Family**
- 5V HC logic family
- Direct digital I/O compatibility

**Power Distribution**
- Decoupling: 100 nF per IC
- Bulk capacitance: 10 µF per board
- Star topology ground

</td>
<td width="50%">

**Test Points**
- All critical signals accessible
- A, B, R buses
- Carry chain monitoring
- Control signal observation

</td>
</tr>
</table>
