# Changelog

All notable changes to the 8-Bit Transistor CPU project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned

- Carry-lookahead adder implementation
- Complete hardware testing of REV A operation
- Performance characterization (timing, power)
- Video tutorials and build guides
- FPGA implementation

---

## [1.0.0] - 2026-01-16

### Added - Initial Release

#### Core Features

- Complete 8-bit ALU with 19 operations (5-bit opcode, 32 possible)
- **Pure combinational circuit** - no clock required
- 3,856+ discrete transistor implementation
- **270mm × 270mm** main ALU board
- Arithmetic operations: ADD, SUB, INC, DEC
- Logic operations: AND, OR, XOR, NAND, NOR, XNOR
- Shift operations: LSL, LSR, ASR
- Special operations: PASS A, PASS B, NOT A, NOT B, CMP, REV A
- Flag generation: Less Than, Equal, Positive, Carry Out
- 5-bit opcode allows future expansion (13 opcodes reserved)

#### Hardware Design

- Complete KiCad schematics for all boards
- PCB layouts for main logic, control, flags, and display panels
- Bill of materials with component specifications
- Assembly instructions and build guide

#### Simulation & Verification

- Logisim Evolution complete system simulation
- ngspice SPICE simulations for all gates
- 1,900 comprehensive test vectors (100 per operation)
- Python test framework with golden model
- 100% test pass rate

#### Documentation

- Comprehensive README with project overview
- Getting Started guide with setup instructions
- Architecture documentation with block diagrams
- Verification documentation with test results
- Media index cataloging all 274 assets
- Contributing guidelines
- Complete documentation map

#### Media Assets

- 109 PNG images (schematics, PCBs, simulations)
- 95 JPG photos (fabrication, assembly, testing)
- 53 SVG vector graphics (schematics)
- 17 MP4 demonstration videos
- Process timeline showing 8 build phases
- VLSI transistor-level layouts

#### Firmware

- Arduino input controller firmware
- Arduino display controller firmware
- Serial communication protocols

#### Tools & Scripts

- Automated test runner (`run_tests.sh`)
- Component analysis scripts
- KiCad cleanup utilities
- Test vector generation scripts

### Design Decisions

- XOR array for ADD/SUB (40% transistor savings vs. MUX array)
- Global inverter for logic operation derivation (89% savings)
- Ripple-carry adder (simplicity over speed)
- Hybrid discrete/IC approach (educational value + practicality)

### Verification Results

- SPICE: 8/8 gates verified (100%)
- Logisim: 19/19 operations verified (100%)
- Software: 1,900/1,900 tests passed (100%)
- Hardware: 18/19 operations verified (95%)
- Overall coverage: 99%

---

## [0.9.0] - 2026-01-09

### Added

- Complete PCB fabrication
- All boards assembled and tested
- Initial hardware verification
- Main logic board operational
- Control unit functional
- Display panels working

### Fixed

- Power distribution issues
- Component orientation errors
- Solder bridge on flags board
- Clock signal noise

---

## [0.8.0] - 2026-01-05

### Added

- KiCad PCB layouts completed
- Gerber files generated
- PCB orders placed (JLCPCB)
- Component orders placed (DigiKey)

### Changed

- Optimized PCB routing
- Improved ground plane design
- Added test points

---

## [0.7.0] - 2026-01-03

### Added

- Complete Logisim simulation
- All 19 operations implemented
- Test vector generation
- Automated testing framework

### Verified

- Arithmetic operations in simulation
- Logic operations in simulation
- Flag generation
- Control signal decoding

---

## [0.6.0] - 2025-12-28

### Added

- SPICE simulations for all gates
- Full adder SPICE verification
- Timing analysis
- Power consumption estimates

### Verified

- NOT gate: 100% correct
- NAND gate: 100% correct
- NOR gate: 100% correct
- XOR gate: 100% correct
- Full adder: 100% correct

---

## [0.5.0] - 2025-12-20

### Added

- Complete KiCad schematics
- Hierarchical design structure
- Component selection
- Design rule checks

### Changed

- Switched to 74HC logic family
- Optimized gate designs
- Improved schematic organization

---

## [0.4.0] - 2025-12-15

### Added

- Logisim circuit design
- Gate library
- 1-bit full adder
- 8-bit ripple-carry adder

### Designed

- Arithmetic unit architecture
- Logic unit architecture
- Control unit decoder

---

## [0.3.0] - 2025-12-10

### Added

- Transistor-level gate designs
- VLSI layouts in Electric
- CMOS implementation plans
- Transistor cost analysis

### Analyzed

- Gate transistor counts
- Design trade-offs
- XOR vs. MUX for subtraction
- Global inverter approach

---

## [0.2.0] - 2025-12-05

### Added

- Project architecture design
- Operation specifications
- Opcode table (19 operations)
- Truth tables for all operations

### Defined

- 8-bit word size
- 4-bit opcode
- Control signals
- Flag definitions

---

## [0.1.0] - 2025-12-01

### Added

- Initial project setup
- Repository structure
- Basic documentation
- Design goals

### Planned

- Complete ALU implementation
- Discrete transistor design
- Educational focus
- Open-source release

---

## Version History Summary

| Version | Date       | Milestone                                   |
| ------- | ---------- | ------------------------------------------- |
| 1.0.0   | 2026-01-16 | **Initial Release** - Complete system |
| 0.9.0   | 2026-01-09 | Hardware assembly complete                  |
| 0.8.0   | 2026-01-05 | PCB fabrication                             |
| 0.7.0   | 2026-01-03 | Simulation complete                         |
| 0.6.0   | 2025-12-28 | SPICE verification                          |
| 0.5.0   | 2025-12-20 | Schematic complete                          |
| 0.4.0   | 2025-12-15 | Logisim design                              |
| 0.3.0   | 2025-12-10 | Transistor-level design                     |
| 0.2.0   | 2025-12-05 | Architecture defined                        |
| 0.1.0   | 2025-8-01  | Project inception                           |

---

## Categories

### Added

New features, files, or capabilities

### Changed

Changes to existing functionality

### Deprecated

Features that will be removed in future versions

### Removed

Features that have been removed

### Fixed

Bug fixes

### Security

Security-related changes

### Verified

Testing and verification milestones

### Designed

Design decisions and architecture

### Analyzed

Analysis and optimization work

### Planned

Future work and roadmap items

---

## Links

- [Repository](https://github.com/tmarhguy/cpu)
- [Issues](https://github.com/tmarhguy/cpu/issues)
- [Releases](https://github.com/tmarhguy/cpu/releases)
- [Documentation](docs/)

---

## Maintainer

**Tyrone Marhguy**
Sophomore, Computer Engineering, BSE
University of Pennsylvania, School of Engineering and Applied Science
Expected Graduation: May 2028

### Contact & Links

- Website: [tmarhguy.com](https://tmarhguy.com)
- Email: tmarhguy@gmail.com | tmarhguy@seas.upenn.edu
- LinkedIn: [linkedin.com/in/tmarhguy](https://linkedin.com/in/tmarhguy)
- Twitter: [@marhguy_tyrone](https://twitter.com/marhguy_tyrone)
- Instagram: [@tmarhguy](https://instagram.com/tmarhguy)
- GitHub: [github.com/tmarhguy](https://github.com/tmarhguy)
