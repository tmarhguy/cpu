<div align="center">

# 8-Bit Transistor CPU

**Computer Engineering Project - Discrete Transistor ALU Design from First Principles**

[![Computer Engineering](https://img.shields.io/badge/Computer-Engineering-blue.svg)](https://www.seas.upenn.edu/) [![University](https://img.shields.io/badge/University-Penn%20Engineering-red.svg)](https://www.seas.upenn.edu/) [![Hardware](https://img.shields.io/badge/Hardware-Discrete%20Transistors-green.svg)](https://github.com/tmarhguy/cpu)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![KiCad](https://img.shields.io/badge/KiCad-314CB0?logo=kicad&logoColor=white)](https://www.kicad.org/) [![Arduino](https://img.shields.io/badge/Arduino-00979D?logo=arduino&logoColor=white)](https://www.arduino.cc/) [![LTSpice](https://img.shields.io/badge/LTSpice-FF6B35?logo=analog&logoColor=white)](https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html)

**Computer Engineering Personal Project**

**University of Pennsylvania, School of Engineering and Applied Science**

**Computer Engineering - From Transistors to Systems**

_A complete 8-bit Arithmetic Logic Unit (ALU) designed and built from discrete transistors. This project demonstrates the fundamental principles of digital logic design, starting with 1-bit adders and scaling to a fully functional 8-bit arithmetic unit with efficient 2's complement subtraction. All design decisions are justified through comprehensive transistor cost analysis._

</div>

---

<div align="center">

## The Story Behind the Project

</div>

I woke up to a long post from a debate with a friend the night before. He was telling me to my face many times how CS is the mother of all programs and applications, basically, computer engineering is just a child who knows how to play every instrument, but not a prodigy at either one.

Well, in an attempt to present my argument in our courtroom (the WhatsApp group), I spent the next months designing a ALU!

Yes, I built an 8-bit computer ALU from 800+ transistors all the way up, and it can add two numbers and more (16 arithmetic and logical operations)!

I love our CS students, I love them, but if you can write binary code, it's because there was a non-prodigy who wired the computer for you. It's beyond theory. I think they are brothers, maybe not always agreeable, but united by function, distinct in capacity.

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
- [Skills Demonstrated](#skills-demonstrated)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Hardware Implementation](#hardware-implementation)
- [Simulation &amp; Testing](#simulation-testing)
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
