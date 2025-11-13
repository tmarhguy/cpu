<div align="center">

# 8-Bit Transistor CPU

**Computer Engineering Project - Discrete Transistor ALU Design from First Principles**

[![Computer Engineering](https://img.shields.io/badge/Computer-Engineering-blue.svg)](https://www.seas.upenn.edu/) [![University](https://img.shields.io/badge/University-Penn%20Engineering-red.svg)](https://www.seas.upenn.edu/) [![Hardware](https://img.shields.io/badge/Hardware-Discrete%20Transistors-green.svg)](https://github.com/tmarhguy/cpu) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![KiCad](https://img.shields.io/badge/KiCad-314CB0?logo=kicad&logoColor=white)](https://www.kicad.org/) [![Arduino](https://img.shields.io/badge/Arduino-00979D?logo=arduino&logoColor=white)](https://www.arduino.cc/) [![LTSpice](https://img.shields.io/badge/LTSpice-FF6B35?logo=analog&logoColor=white)](https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html)

**Computer Engineering Project**  

**University of Pennsylvania, School of Engineering and Applied Science**  

**Computer Engineering - From Transistors to Systems**

_A complete 8-bit Arithmetic Logic Unit (ALU) designed and built from discrete transistors. This project demonstrates the fundamental principles of digital logic design, starting with 1-bit adders and scaling to a fully functional 8-bit arithmetic unit with efficient 2's complement subtraction. All design decisions are justified through comprehensive transistor cost analysis._

</div>

---

## Table of Contents

- [The Story Behind the Project](#the-story-behind-the-project)
- [Project Overview](#project-overview)
  - [Design Philosophy](#design-philosophy)
  - [Project Scope](#project-scope)
- [Features](#features)
- [Architecture](#architecture)
- [Component Breakdown](#component-breakdown)
  - [1-Bit Half Adder](#1-bit-half-adder)
  - [1-Bit Full Adder](#1-bit-full-adder)
  - [8-Bit Ripple-Carry Adder](#8-bit-ripple-carry-adder)
  - [ADD/SUB Implementation](#addsub-implementation)
  - [Control Unit](#control-unit)
- [Key Design Decisions](#key-design-decisions)
  - [2's Complement Subtraction](#2s-complement-subtraction)
  - [XOR Array vs. MUX Array](#xor-array-vs-mux-array)
- [Transistor Cost Analysis](#transistor-cost-analysis)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Hardware Implementation](#hardware-implementation)
- [Simulation & Testing](#simulation--testing)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---
<div align="center">

## The Story Behind the Project

</div>

I woke up to a long post from a debate with a friend the night before. He was telling me to my face many times how CS is the mother of all programs and applications—basically, computer engineering is just a child who knows how to play every instrument, but not a prodigy at either one.

Well, in an attempt to present my argument in our courtroom (the WhatsApp group), I spent the next months designing a CPU!

Yes, I built an 8-bit computer CPU from 800+ transistors all the way up, and it can add two numbers!

I love our CS students, I love them, but if you can write binary code, it's because there was a non-prodigy who wired the computer for you. It's beyond theory. Before, what do you think between CS and Comp Engineering? I think they are brothers, maybe not always agreeable, but united by function, distinct in capacity.

---

## Project Overview

This repository documents the complete design, implementation, and analysis of an 8-bit Arithmetic Logic Unit (ALU) built from discrete transistors. The design follows a bottom-up approach, starting with fundamental 1-bit adders and systematically scaling to a multi-function 8-bit unit capable of 2's complement arithmetic.

### Design Philosophy

The project emphasizes:

- **Transistor-Level Understanding**: Every design decision is justified through transistor cost analysis
- **Scalable Architecture**: Built from reusable 1-bit components scaled to 8-bit operations
- **Efficient Implementation**: Optimized designs that minimize transistor count while maintaining functionality
- **Educational Value**: Clear documentation of design rationale and trade-offs

### Project Scope

The current implementation supports:

- **8-bit word size**: Operates on two 8-bit inputs, $A[7:0]$ and $B[7:0]$
- **Arithmetic Operations**: ADD and SUBTRACT using 2's complement
- **Scalable Control**: 4-bit control signal allowing 16 possible operations
- **Centralized Control Unit**: Dedicated decoder translating opcodes to internal control signals

---

## Features

### Core Capabilities

<table>
<tr>
<td width="50%">

**Arithmetic Operations**
- **ADD**: $A + B$ (direct addition)
- **SUB**: $A - B$ (2's complement subtraction)
- Efficient XOR-based implementation

**Architecture**
- 8-bit ripple-carry adder
- Modular 1-bit full adder design
- Scalable to 16 operations via 4-bit control

</td>
<td width="50%">

**Control System**
- 4-bit opcode (FUNC[3:0])
- Centralized control unit decoder
- Future support for logical operations

**Design Optimization**
- Transistor cost analysis for all components
- XOR-based subtraction (96T vs 138T MUX design)
- Optimized carry generation circuits

</td>
</tr>
</table>

### Hardware Features

- **Discrete Transistor Implementation**: Built from individual MOSFETs
- **5V HC Logic Family**: Standard TTL-compatible levels
- **Arduino Integration**: Front-end input and back-end display controllers
- **Comprehensive Testing**: Simulation and hardware validation

---

## Architecture

<div align="center">

### High-Level Block Diagram

```
             A[7:0]   B[7:0]
                |        |
    FUNC[3:0]   |        |
       |        |        |
   +---v---+    |        |
   | Control   +----v---v----+     +-------------+
   |   Unit |   | Arithmetic  |---->|             |
   +-------+   |    Unit     |  0  | 8-bit 2-to-1|
       |       +-------------+     |     MUX     |---> ALU_Result[7:0]
       |             |   |         |             |
       +------------>|   +-------->|      1      |
      (LogicSelect)  |  (ArithMode)  |             |
                     |             +-------------+
                     |                 ^
                     v                 |
               +-------------+         |
               |  Logical    |         |
               |    Unit     |---------+
               +-------------+        (FinalMuxSelect)
```

</div>

### Datapath

**Primary Datapath**: $A_{reg} (8b) \rightarrow ALU (arith + logic + mux + global invert) \rightarrow R_{reg} (8b)$

### Control Signals

- **FUNC[3:0]**: 4-bit opcode enabling 16 possible operations
- **M**: ADD/SUB mode (0=ADD, 1=SUB)
- **INV_OUT**: Global post-mux inversion bit
- **LOAD_A, LOAD_B, LOAD_R**: Register load enables

---

## Component Breakdown

### 1-Bit Half Adder

<table>
<tr>
<td width="50%">

**Inputs**
- A
- B

**Outputs**
- Sum: $A \oplus B$
- Carry-out: $A \cdot B$

</td>
<td width="50%">

**Implementation**
- AND gate for carry generation
- XOR gate for sum calculation
- Foundation for full adder design

</td>
</tr>
</table>

### 1-Bit Full Adder

<table>
<tr>
<td width="50%">

**Inputs**
- A
- B
- $C_{in}$

**Outputs**
- **Sum**: $A \oplus B \oplus C$
- **Carry**: $AB + BC + AC$ (standard)
- **Carry (optimized)**: $AB + C(A \oplus B)$

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

**Logic Derivation**: Boolean expressions derived using truth tables and Karnaugh maps, verified through simulation.

### 8-Bit Ripple-Carry Adder

<table>
<tr>
<td width="50%">

**Structure**
- 8× 1-bit full adders daisy-chained
- Carry-out of bit $i$ → carry-in of bit $i+1$
- Sequential propagation through all stages

**Inputs**
- 8-bit Input $A[7:0]$
- 8-bit Input $B[7:0]$

</td>
<td width="50%">

**Outputs**
- 8-bit output $S[7:0]$
- 1-bit carry (1 if overflow)
- Final carry: $C_8$ or $C_{final}$

**Implementation**
- Modular black-box approach
- Reusable 1-bit full adder design
- Scalable architecture

</td>
</tr>
</table>

### ADD/SUB Implementation

<table>
<tr>
<td width="50%">

**Operations**
- **ADD**: $A + B$
- **SUB**: $A - B = A + (-B)$ (2's complement)

**Design Approach**
- XOR-based implementation
- Control signal feeds XOR gates:
  - $B \oplus 0 = B$ (pass-through)
  - $B \oplus 1 = \overline{B}$ (invert)

</td>
<td width="50%">

**Control Signals**
- **ADD**: `00000000` (8-bit)
- **SUB**: `11111111` (8-bit)
- Control bit (1-bit) feeds ALU as $C_{in}$ to complete 2's complement

**Cost Comparison**
- XOR design: $8 \cdot 12 = 96T$
- MUX design: $138T$
- **Savings**: $42T$ (30% reduction)

</td>
</tr>
</table>

### Control Unit

<table>
<tr>
<td width="50%">

**Input**
- 4-bit control signal (FUNC[3:0])
- Allows $2^{4} = 16$ possible operations

**Outputs**
- 1-bit to adder (as $C_{in}$)
- 8-bit signal of 1s or 0s to XOR gates
- Logic select signals (future)
- Final mux select (future)

</td>
<td width="50%">

**Purpose**
- Decode opcodes to internal control signals
- Coordinate ALU operations
- Enable future operation expansion

**Future Operations**
- Currently: ADD, SUB
- Planned: MUL, DIV
- Logical operations: AND, OR, NAND, NOR, XOR, XNOR

</td>
</tr>
</table>

---

## Key Design Decisions

### 2's Complement Subtraction

**Requirement**: Support subtraction ($A - B$) using the existing 8-bit adder.

**Solution**: Implement 2's complement arithmetic, where $-B = \overline{B} + 1$.

This approach allows reuse of the entire 8-bit adder by:
1. Inverting the $B$ input (to get $\overline{B}$)
2. Setting the initial carry-in ($C_{in}$ of the first adder) to $1$ (to perform the $+ 1$)

**Result**: The circuit computes $A + \overline{B} + 1 = A + (-B)$, which is 2's complement subtraction.

### XOR Array vs. MUX Array

<table>
<tr>
<td width="50%">

**MUX-Based Approach (Considered)**
- 8-bit 2-to-1 MUX array
- Separate control signal for $C_{in}$
- **Cost**: ~138T
- More complex control logic

</td>
<td width="50%">

**XOR-Based Approach (Implemented)**
- 8 XOR gates as conditional inverters
- Single control signal handles both inversion and $C_{in}$
- **Cost**: $8 \cdot 12 = 96T$
- Elegant and efficient solution

</td>
</tr>
</table>

**The Insight**: The same control signal used to select inversion (1 for SUB) can be wired directly to the $C_{in}$ of the first adder, elegantly handling both parts of the 2's complement operation simultaneously.

**Result**: 30% reduction in transistor count while maintaining full functionality.

---

## Transistor Cost Analysis

<div align="center">

### Gate Costs

| Gate | Transistor Count |
|------|------------------|
| NOT | 2T |
| NOR | 4T |
| NAND | 4T |
| OR | 6T |
| AND | 6T |
| XOR | 12T |
| XNOR | 12T |

</div>

### Component Costs

<table>
<tr>
<td width="50%">

**1-Bit Full Adder**
- Sum: $A \oplus B \oplus C$ = 36T
- Carry (optimized): $AB + C(A \oplus B)$ = 30T
- **Total**: **66T**

**8-Bit Adder**
- 8 × 66T = 528T (core adder)
- Additional routing and buffering

</td>
<td width="50%">

**B-Inversion Logic (8-bit)**
- MUX-based design: ~138T
- XOR-based design: $8 \times 12 = 96T$
- **Savings**: 42T (30% reduction)

**Design Principles**
- Best design: $(n-1)$ MOSFETs for $n$ input
- $n$-AND = $(n-1)$ NAND + $n$-OR = $(n-1)$ OR NOT

</td>
</tr>
</table>

This analysis clearly justifies the selection of the XOR-based design for subtraction.

---

## Tech Stack

<div align="center">

### Hardware Design

![KiCad](https://img.shields.io/badge/KiCad-314CB0?style=for-the-badge&logo=kicad&logoColor=white)
![LTSpice](https://img.shields.io/badge/LTSpice-FF6B35?style=for-the-badge&logo=analog&logoColor=white)
![Discrete Transistors](https://img.shields.io/badge/Discrete_Transistors-000000?style=for-the-badge&logo=circuit&logoColor=white)

### Control & Interface

![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)

### Logic Family

![74HC Series](https://img.shields.io/badge/74HC-5V_Logic-FF6B6B?style=for-the-badge&logo=circuit&logoColor=white)

</div>

---

## Project Structure

```
cpu/
├── hardware/              # Hardware design files
│   ├── alu/              # ALU core implementation
│   │   ├── full-adder/   # 1-bit full adder
│   │   └── logic-circuits/ # Logic gate implementations
│   ├── control-unit/     # Control unit design
│   │   ├── input-control/
│   │   └── output-control/
│   └── power_supply/     # Power distribution
├── schematics/           # Schematic design files
│   ├── kicad/           # KiCad projects
│   └── ltspice/         # LTSpice simulations
├── firmware/            # Microcontroller firmware
│   ├── controller-input/  # Front-end Arduino
│   └── controller-display/ # Back-end Arduino
├── tests/               # Test vectors and validation
├── docs/                # Documentation
│   ├── architecture_overview.md
│   ├── opcodes.md
│   └── bom.md
└── media/               # Build photos and demos
```

---

## Quick Start

### Prerequisites

- **KiCad** (for schematic/PCB design)
- **LTSpice** (for circuit simulation)
- **Arduino IDE** (for firmware development)
- **Hardware components** (see [BOM](docs/bom.md))

### Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/tmarhguy/cpu.git
   cd cpu
   ```

2. **Review the design documentation:**

   - [Architecture Overview](docs/architecture_overview.md)
   - [ALU Design Notes](alu_design.md)
   - [Opcode Map](docs/opcodes.md)

3. **Explore the hardware design:**

   - Navigate to `hardware/` for component designs
   - Check `schematics/kicad/` for KiCad projects
   - Review `schematics/ltspice/` for simulations

4. **Set up firmware:**

   - Open `firmware/controller-input/` in Arduino IDE
   - Open `firmware/controller-display/` in Arduino IDE
   - Upload to respective Arduino boards

---

## Hardware Implementation

### Bill of Materials

Key components (see [full BOM](docs/bom.md)):

- **Registers**: 3× 74HC373/574 (A, B, R registers)
- **Multiplexers**: 2× 74HC157 (8-bit 2:1 mux)
- **ALU Core**: Discrete transistors (NMOS/PMOS pairs)
- **Power**: 5V supply, decoupling capacitors (100 nF per IC, 10 µF bulk)
- **I/O**: LEDs, resistors, headers, test points
- **Controllers**: 2× Arduino (input and display)

### Power Distribution

- **Voltage**: 5V single rail
- **Ground**: Star topology with single-point ground to ALU
- **Decoupling**: 100 nF ceramic per IC, 10 µF bulk per board
- **Logic Family**: 5V HC (74HCxx) throughout

### I/O Architecture

- **Front-end Arduino**: Keypad input → number entry + opcode selection
- **Back-end Arduino**: Display/logging → reads R_reg and displays results
- **Direct I/O**: 5V logic levels, direct digital I/O connections

---

## Simulation & Testing

### Simulation Milestones

1. **1-bit half adder**: Circuit diagram with AND and XOR gates
2. **1-bit full adder**: Truth table + K-map analysis
3. **Carry circuit**: Design and simulation (test case: A=1, B=0, C=1)
4. **Sum circuit**: Design and simulation (test case: A=1, B=0, C=0)
5. **8-bit ripple adder**: Propagation delay analysis
6. **System-level**: Full datapath simulation with control unit

### Test Vectors

Test vectors are stored in JSON format in the `tests/` directory:

- **add_sub.json**: Arithmetic operation test vectors
- **logic_ops.json**: Logic operation test vectors (future)

See [tests/README.md](tests/README.md) for detailed test vector format and usage.

---

## Future Work

### Immediate Next Steps

1. **Implement Control Unit**: Build the decoder logic to translate all 16 FUNC codes into their respective internal signals
2. **Build Logical Unit**: Design and add the parallel Logical Unit to handle bitwise operations (AND, OR, NOR, etc.)
3. **Add Final MUX**: Implement the 8-bit 2-to-1 MUX to select the final output from either the Arithmetic or Logical unit

### Planned Enhancements

4. **Implement Overflow Detection**: Add logic to detect signed arithmetic overflow
5. **Implement Zero Flag**: Add an 8-input NOR gate to detect if the result is zero
6. **Expand Operations**: Begin scaffolding for more complex operations like MUL (multiplication) and DIV (division)
7. **Complete Opcode Set**: Implement all 16 operations defined in the opcode map

### Long-Term Goals

- Full instruction set implementation
- Memory interface integration
- Complete CPU system with program counter and instruction decoder
- Performance optimization and timing analysis

---

## Contributing

We welcome contributions! Here's how to get started:

<details>
<summary>Click to expand contribution guidelines</summary>

### Quick Contribution Guide

1. **Fork the repository**

2. **Create a feature branch:**

   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes and test thoroughly**

4. **Commit with conventional commits:**

   ```bash
   git commit -m "feat: add amazing new feature"
   ```

5. **Push to your fork and create a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/cpu.git

# Navigate to project
cd cpu
```

### Code Standards

- **Hardware**: Follow transistor cost analysis for all design decisions
- **Firmware**: Arduino coding standards, proper error handling
- **Documentation**: Update README and docs for new features
- **Testing**: Provide test vectors for new operations

### Areas for Contribution

- **Hardware**: ALU optimizations, control unit implementation
- **Firmware**: Arduino code improvements, test vector runners
- **Documentation**: Tutorials, design explanations
- **Testing**: Additional test vectors, simulation improvements

</details>

---

## License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) for details.

---

## Acknowledgments

### Academic Context

**University of Pennsylvania, School of Engineering and Applied Science**  
**Computer Engineering Program**

This project represents a comprehensive exploration of digital logic design, from transistor-level implementation to system-level architecture.

### Technical Acknowledgments

- **KiCad** — Schematic and PCB design
- **LTSpice** — Circuit simulation and analysis
- **Arduino** — Microcontroller platform for control and interface
- **74HC Logic Family** — Standard TTL-compatible logic components

### Educational Resources

- Digital logic design principles and best practices
- Transistor-level circuit design methodologies
- Computer architecture fundamentals
- Hardware description and documentation standards

---

<div align="center">

### Connect & Collaborate

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/tmarhguy)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/tmarhguy)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tmarhguy@seas.upenn.edu)

**Student:** Tyrone Marhguy  
**University Email:** tmarhguy@seas.upenn.edu  
**University:** University of Pennsylvania, School of Engineering and Applied Science  
**Major:** Computer Engineering

---

**Star this repository if you found this project helpful!**

_Building bridges between silicon and software, one transistor at a time_

</div>
