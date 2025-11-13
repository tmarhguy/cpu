<div align="center">

# 8-Bit Transistor CPU

**Computer Engineering Project - Discrete Transistor ALU Design from First Principles**

[![Computer Engineering](https://img.shields.io/badge/Computer-Engineering-blue.svg)](https://www.seas.upenn.edu/) [![University](https://img.shields.io/badge/University-Penn%20Engineering-red.svg)](https://www.seas.upenn.edu/) [![Hardware](https://img.shields.io/badge/Hardware-Discrete%20Transistors-green.svg)](https://github.com/tmarhguy/cpu) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![KiCad](https://img.shields.io/badge/KiCad-314CB0?logo=kicad&logoColor=white)](https://www.kicad.org/)[![Arduino](https://img.shields.io/badge/Arduino-00979D?logo=arduino&logoColor=white)](https://www.arduino.cc/)[![LTSpice](https://img.shields.io/badge/LTSpice-FF6B35?logo=analog&logoColor=white)](https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html)

**Computer Engineering Project**

**University of Pennsylvania, School of Engineering and Applied Science**

**Computer Engineering - From Transistors to Systems**

_A complete 8-bit Arithmetic Logic Unit (ALU) designed and built from discrete transistors. This project demonstrates the fundamental principles of digital logic design, starting with 1-bit adders and scaling to a fully functional 8-bit arithmetic unit with efficient 2's complement subtraction. All design decisions are justified through comprehensive transistor cost analysis._

</div>

---

<div align="center">

## The Story Behind the Project

</div>

I woke up to a long post from a debate with a friend the night before. He was telling me to my face many times how CS is the mother of all programs and applications—basically, computer engineering is just a child who knows how to play every instrument, but not a prodigy at either one.

Well, in an attempt to present my argument in our courtroom (the WhatsApp group), I spent the next months designing a CPU!

Yes, I built an 8-bit computer CPU from 800+ transistors all the way up, and it can add two numbers!

I love our CS students, I love them, but if you can write binary code, it's because there was a non-prodigy who wired the computer for you. It's beyond theory. Before, what do you think between CS and Comp Engineering? I think they are brothers, maybe not always agreeable, but united by function, distinct in capacity.

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
  - [2&#39;s Complement Subtraction](#2s-complement-subtraction)
  - [XOR Array vs. MUX Array](#xor-array-vs-mux-array)
- [Transistor Cost Analysis](#transistor-cost-analysis)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Hardware Implementation](#hardware-implementation)
- [Simulation &amp; Testing](#simulation--testing)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

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

### Hardware Features

- **Discrete Transistor Implementation**: Built from individual MOSFETs
- **5V HC Logic Family**: Standard TTL-compatible levels
- **Arduino Integration**: Front-end input and back-end display controllers
- **Comprehensive Testing**: Simulation and hardware validation

---

## Architecture

<div align="center">

### High-Level Block Diagram (Complete System)

</div>

```
                           ┌─────────────────────────────────────────┐
                           │        CONTROL UNIT (Arduino #1)        │
                           │  - Loads A, B registers                 │
                           │  - Sends FUNC[3:0], M, INV_OUT          │
                           │  - Coordinates ADD/SUB/LOGIC ops        │
                           │  - Handles MULTIPLY/DIVIDE sequencing   │
                           │  - Generates LOAD pulses                │
                           │  - Optional: 1 Hz for clock mode        │
                           └─────────────────────────────────────────┘
                                           │
                            Control Lines  │
      ┌────────────────────────────────────┴──────────────────────────────────┐
      │                                                                        │
┌────────────┐     Data Bus A      ┌────────────────────────┐     Data Bus B   ┌────────────┐
│  A Input   │───(A_D[7:0])──────▶ │      A REGISTER        │                     B Input   │
│ (Switches  │                     │     (74HC373/574)      │───────────────▶   (Switches   │
│ or Arduino)│                     │   Holds Operand A       │                     or Arduino)│
└────────────┘                     └────────────────────────┘                     └────────────┘
                                           │ A_Q[7:0]                B_Q[7:0] │
                                           ▼                                 ▼
                                       ┌──────────────────────────────────────────┐
                                       │                ALU CORE                  │
                                       │──────────────────────────────────────────│
                                       │  Arithmetic Unit (8-bit Ripple Adder)   │
                                       │     - ADD, SUB                          │
                                       │     - Uses M bit & XOR network          │
                                       │                                          │
                                       │  Logic Unit                              │
                                       │     - NAND, NOR, XNOR                    │
                                       │     - PASS A, PASS B                     │
                                       │     - ZERO, ONE                          │
                                       │                                          │
                                       │  OPERATION SELECT                        │
                                       │     - 74HC157 MUX (Arithmetic vs Logic) │
                                       │                                          │
                                       │  GLOBAL INVERTER                         │
                                       │     - For AND/OR/XOR/NOT/etc.           │
                                       │                                          │
                                       │  Output Bus = ALU_OUT[7:0]              │
                                       └──────────────────────────────────────────┘
                                                      │
                                                      ▼
                                      ┌────────────────────────────────────┐
                                      │         RESULT REGISTER (R)        │
                                      │           (74HC373/574)            │
                                      │    Stores the ALU Output (8-bit)    │
                                      └────────────────────────────────────┘
                                                      │
                              ┌────────────────────────┴────────────────────────────┐
                              │                                                     │
                      ALU Output Bus                                       Debug/Display
                              │                                                     │
                              ▼                                                     ▼
                    ┌──────────────────────┐                    ┌─────────────────────────────────┐
                    │  Arduino #2 (Output)│                    │   LEDs / OLED / Serial Terminal │
                    │ - Reads R register   │──────────────────▶│   - Shows A, B, Result          │
                    │ - Formats/Displays   │                    │   - Shows FLAGS (Zero, Neg)    │
                    └──────────────────────┘                    └─────────────────────────────────┘
```

### The 5 Stages of Architecture

<table>
<tr>
<td width="50%">

**Stage 1: Input (Human-Computer Interface)**
- **Keypad Module**: High-level decimal input (e.g., "134")
- **Toggle Module**: Low-level binary input (e.g., `10000110`)
- Modular, swappable input methods

**Stage 2: Control (Input Controller & Data Bus)**
- **Arduino #1 (The Translator)**: Reads keypad, converts decimal to 8-bit binary
- Places values on 8-bit Data Bus
- **Load Buttons**: Manual `Load A` and `Load B` push-buttons send clock pulses

</td>
<td width="50%">

**Stage 3: Storage (Registers)**
- **Register A (74HC574)**: Latches 8-bit value from Data Bus when "Load A" pressed
- **Register B (74HC574)**: Latches 8-bit value from Data Bus when "Load B" pressed
- Outputs permanently feed the ALU

**Stage 4: Execution (The "Crown Jewel")**
- **640+ Transistor ALU**: Custom-built processor core
- Takes 8-bit inputs from Register A and Register B
- Opcode Select switches choose function (ADD, SUB, AND, PASS A, etc.)
- **Output Register (74HC574)**: Latches and holds 8-bit result

</td>
</tr>
<tr>
<td colspan="2">

**Stage 5: Display (Output Controller)**
- **Arduino #2 (The Formatter)**: Reads stable 8-bit binary from Output Register
- **LCD/OLED Screen**: Formats binary (e.g., `11000011`) into decimal ("195") and displays

</td>
</tr>
</table>

### ALU Core Architecture

<table>
<tr>
<td width="50%">

**Arithmetic Unit**
- 8-bit ripple-carry adder
- M (mode) bit selects ADD vs SUB
- SUB uses `B XOR M`, carry-in = M
- Standard CPU subtraction implementation

**Logic Unit**
- Built from CMOS primitives:
  - NAND, NOR, XNOR
  - PASS A, PASS B
  - ZERO, ONE
- Global invert enables:
  - NAND → AND
  - NOR → OR
  - XNOR → XOR
  - PASS A → NOT A
  - ZERO → ONE

</td>
<td width="50%">

**Operation Select (MUX)**
- 2-to-1 mux (74HC157) chooses:
  - Arithmetic output
  - Logic output
- Controlled by FUNC decoding (Arduino #1)

**Global Inverter**
- Post-mux inversion layer
- Controlled by INV_OUT bit
- Enables full 16-operation function table

**Total Operations**: 16 ALU operations supported

</td>
</tr>
</table>

### Control Signals

- **FUNC[3:0]**: 4-bit opcode enabling 16 possible operations
- **M**: ADD/SUB mode (0=ADD, 1=SUB)
- **INV_OUT**: Global post-mux inversion bit
- **LOAD_A, LOAD_B, LOAD_R**: Register load enables

### Datapath

**Primary Datapath**: $A_{reg} (8b) \rightarrow ALU (arith + logic + mux + global invert) \rightarrow R_{reg} (8b)$

---

## Component Breakdown

### 1-Bit Half Adder

<table>
<tr>
<td width="50%">

### 1-Bit Full Adder

<table>
<tr>
<td width="50%">

**Logic Derivation**: Boolean expressions derived using truth tables and Karnaugh maps, verified through simulation.

### 8-Bit Ripple-Carry Adder

<table>
<tr>
<td width="50%">

### ADD/SUB Implementation

<table>
<tr>
<td width="50%">

### Control Unit

<table>
<tr>
<td width="50%">

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

**The Insight**: The same control signal used to select inversion (1 for SUB) can be wired directly to the $C_{in}$ of the first adder, elegantly handling both parts of the 2's complement operation simultaneously.

**Result**: 30% reduction in transistor count while maintaining full functionality.

---

## Transistor Cost Analysis

<div align="center">

### Gate Costs

| Gate | Transistor Count |
| ---- | ---------------- |
| NOT  | 2T               |
| NOR  | 4T               |
| NAND | 4T               |
| OR   | 6T               |
| AND  | 6T               |
| XOR  | 12T              |
| XNOR | 12T              |

</div>

### Component Costs

<table>
<tr>
<td width="50%">

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
