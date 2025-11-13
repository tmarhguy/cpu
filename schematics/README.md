<div align="center">

# Schematics

**Schematic design files and simulation models for the ALU system**

</div>

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
