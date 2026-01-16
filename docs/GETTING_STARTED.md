# Getting Started

**Complete setup and build guide for the 8-Bit Transistor CPU**

This guide walks you through setting up your development environment, understanding the build process, and running your first simulations and tests.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Environment Setup](#development-environment-setup)
- [Understanding the Build Process](#understanding-the-build-process)
- [Running Simulations](#running-simulations)
- [Running Tests](#running-tests)
- [Hardware Setup](#hardware-setup)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## Prerequisites

### Software Requirements

| Tool | Version | Purpose | Download |
|------|---------|---------|----------|
| **Logisim Evolution** | Latest | Digital logic simulation | [GitHub](https://github.com/logisim-evolution/logisim-evolution) |
| **KiCad** | 7.0+ | PCB design & schematic capture | [kicad.org](https://www.kicad.org/) |
| **ngspice** | 40+ | SPICE circuit simulation | [ngspice.org](http://ngspice.sourceforge.net/) |
| **Python** | 3.7+ | Test automation | [python.org](https://www.python.org/) |
| **Arduino IDE** | 2.0+ | Firmware development | [arduino.cc](https://www.arduino.cc/) |
| **Git** | Latest | Version control | [git-scm.com](https://git-scm.com/) |

### Hardware Requirements (for physical build)

- **Soldering equipment**: Temperature-controlled soldering iron (300-350°C)
- **Multimeter**: For continuity and voltage testing
- **Oscilloscope**: Optional but recommended for debugging
- **Power supply**: 5V DC, 2A minimum
- **Components**: See [Bill of Materials](build-notes/bom.md)

### Knowledge Prerequisites

- Basic digital logic (AND, OR, NOT gates)
- Understanding of binary arithmetic
- Familiarity with command line tools
- Basic soldering skills (for hardware build)

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tmarhguy/cpu.git
cd cpu
```

### 2. Run Tests (No Installation Required)

**Quick Test (1,900 tests):**
```bash
# Quick test - no dependencies needed
./run_tests.sh

# Or directly with Python
python3 test/test_alu.py
```

**Exhaustive Test (1,247,084 tests):**
```bash
# Run all test vectors (including exhaustive)
./run_tests.sh exhaustive
```

**Expected output (Quick):**
```
Results: 1900 passed, 0 failed out of 1900 total
Success Rate: 100.0%
```

**Expected output (Exhaustive):**
```
Summary: 1247084 passed, 0 failed
Success Rate: 100.0%
Per-operation: 65,636 tests × 19 operations = 1,247,084 total
```

![Test Results](../media/test_passed.png)
*All 1,900 test vectors passing - complete verification coverage*

> **Evidence:** Test suite validates all 19 ALU operations with 100% pass rate.

### 3. Open Logisim Simulation

```bash
# Navigate to Logisim directory
cd logisim/top

# Open the main ALU file in Logisim Evolution
# File: alu_complete.circ (or similar)
```

![Logisim Complete Circuit](../media/logism-evolution-full-circuit.png)
*Complete 8-bit ALU system in Logisim Evolution*

> **Evidence:** Full system simulation with all 19 operations implemented and verified.

---

## Development Environment Setup

### macOS Setup

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install python3 ngspice git

# Install KiCad
brew install --cask kicad

# Install Arduino IDE
brew install --cask arduino

# Clone the repository
git clone https://github.com/tmarhguy/cpu.git
cd cpu

# Run tests to verify setup
./run_tests.sh
```

### Linux Setup (Ubuntu/Debian)

```bash
# Update package manager
sudo apt update

# Install required tools
sudo apt install -y python3 python3-pip ngspice git

# Install KiCad
sudo add-apt-repository ppa:kicad/kicad-7.0-releases
sudo apt update
sudo apt install kicad

# Install Arduino IDE
wget https://downloads.arduino.cc/arduino-ide/arduino-ide_latest_Linux_64bit.AppImage
chmod +x arduino-ide_latest_Linux_64bit.AppImage

# Clone the repository
git clone https://github.com/tmarhguy/cpu.git
cd cpu

# Run tests
./run_tests.sh
```

### Windows Setup

```powershell
# Install Chocolatey (if not already installed)
# Run PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install required tools
choco install python3 git kicad arduino -y

# Clone the repository
git clone https://github.com/tmarhguy/cpu.git
cd cpu

# Run tests
python test/test_alu.py
```

---

## Understanding the Build Process

The project follows an 8-phase development process, from transistor-level design to final testing.

### Phase 1: MOSFET-Level Design

**Goal:** Design individual logic gates at the transistor level.

![MOSFET Design Phase](../media/process_timeline_01_mosfet_design.png)
*Phase 1: Transistor-level gate design*

**Key activities:**
- NMOS/PMOS transistor selection
- CMOS logic gate design
- Transistor cost analysis
- Layout planning

**Tools:** Electric VLSI, paper sketches

**Output:** Transistor-level schematics for all gates

> **Evidence:** VLSI layouts demonstrate transistor-level implementation.

### Phase 2: Schematic Capture

**Goal:** Create hierarchical schematics in KiCad.

![Schematic Capture Phase](../media/process_timeline_02_schematic.png)
*Phase 2: Schematic design in KiCad*

**Key activities:**
- Gate-level schematic entry
- Hierarchical design (gates → adders → ALU)
- Symbol creation
- Design rule checks

**Tools:** KiCad Schematic Editor

**Output:** Complete system schematics

> **Evidence:** KiCad schematics show complete system hierarchy.

### Phase 3: Simulation

**Goal:** Verify logic correctness through simulation.

![Simulation Phase](../media/process_timeline_03_simulation.png)
*Phase 3: SPICE and Logisim simulation*

**Key activities:**
- ngspice transistor-level simulation
- Logisim functional simulation
- Test vector generation
- Timing analysis

**Tools:** ngspice, Logisim Evolution

**Output:** Verified designs, waveforms, test results

![SPICE Waveforms](../media/sim_ngspice_fulladder_waveform.png)
*Full adder SPICE simulation showing sum and carry outputs*

> **Evidence:** Simulation waveforms validate correct operation before fabrication.

### Phase 4: PCB Design

**Goal:** Convert schematics to manufacturable PCBs.

![PCB Design Phase](../media/process_timeline_04_pcb_design.png)
*Phase 4: PCB layout and routing*

**Key activities:**
- Component footprint assignment
- PCB layout planning
- Trace routing
- Design rule checks
- 3D visualization

**Tools:** KiCad PCB Editor

**Output:** Gerber files for fabrication

![Unrouted PCB](../media/unrouted_full_alu_monolithic.png)
*Unrouted PCB showing component placement and ratsnest*

> **Evidence:** PCB layouts demonstrate careful component placement and routing strategy.

### Phase 5: Prototyping & Learning

**Goal:** Build and test simple circuits to validate approach.

![Prototyping Phase](../media/process_timeline_05_inverter_learning.png)
*Phase 5: Learning through prototyping*

**Key activities:**
- Breadboard prototyping
- First PCB attempts
- Component testing
- Learning from failures

**Tools:** Breadboard, multimeter, oscilloscope

**Output:** Working prototypes, lessons learned

![Failed Inverter](../media/fab_inverter_first_attempt_failed.jpg)
*First inverter attempt - learning from failure*

![Working Inverter](../media/fab_inverter_second_attempt_working.jpg)
*Second attempt - successful working inverter*

> **Evidence:** Prototyping phase shows iterative learning process.

### Phase 6: Fabrication

**Goal:** Order PCBs and components.

![Fabrication Phase](../media/process_timeline_06_fabrication.png)
*Phase 6: PCB fabrication*

**Key activities:**
- Gerber file generation
- PCB ordering (JLCPCB)
- Component ordering (DigiKey, Mouser)
- Quality inspection upon arrival

**Vendors:**
- **PCBs:** JLCPCB, PCBWay
- **Components:** DigiKey, Mouser, LCSC

**Timeline:** 1-2 weeks for PCBs, 3-7 days for components

> **Evidence:** Fabricated PCBs match design specifications.

### Phase 7: Assembly

**Goal:** Solder components and assemble boards.

![Assembly Phase](../media/process_timeline_07_assembly.png)
*Phase 7: Component assembly and soldering*

**Key activities:**
- Component placement
- Soldering (hand or reflow)
- Visual inspection
- Continuity testing

![Component Placement](../media/fab_assembly_step_01_components.jpg)
*Initial component placement before soldering*

![Soldering Progress](../media/fab_assembly_step_03_soldering.jpg)
*Soldering in progress*

![Completed Assembly](../media/fab_assembly_step_05_complete.jpg)
*Completed board assembly*

![MOSFET Close-up](../media/not_closeup_soldered_mosfets.jpg)
*Close-up of soldered MOSFET transistors*

> **Evidence:** Assembly photos document the complete build process.

### Phase 8: Testing & Verification

**Goal:** Verify hardware matches simulation.

![Testing Phase](../media/process_timeline_08_testing.png)
*Phase 8: Hardware testing and verification*

**Key activities:**
- Power-on testing
- Gate-level verification
- System-level testing
- Performance characterization

![Multimeter Testing](../media/fab_testing_multimeter.jpg)
*Testing with multimeter*

![Oscilloscope Testing](../media/fab_testing_oscilloscope.jpg)
*Oscilloscope verification*

> **Evidence:** Testing confirms hardware operates correctly.

---

## Running Simulations

### Logisim Evolution Simulation

**1. Open the main circuit:**

```bash
cd logisim/top
# Open alu_complete.circ in Logisim Evolution
```

**2. Run simulation:**
- Click **Simulate → Ticks Enabled** (or Ctrl+K)
- Adjust clock speed: **Simulate → Tick Frequency**
- Use input pins to set A, B, and FUNC values
- Observe output on result pins and LED displays

![Logisim Simulation](../media/sim_logisim_screenshot.png)
*Logisim simulation interface*

**3. Test all operations:**
- Set FUNC[3:0] to select operation (0-18)
- Provide test inputs on A[7:0] and B[7:0]
- Verify output matches expected result
- Check flags (Zero, Negative, Carry, Overflow)

[![All Operations Demo](../media/alu_top.jpg)](../media/main-demo-logism-evolution-all-opcodes.mp4)
*Click to watch: Complete demonstration of all 19 operations*

> **Evidence:** Logisim simulation validates all operations before hardware build.

### ngspice SPICE Simulation

**1. Navigate to SPICE directory:**

```bash
cd schematics/ltspice
```

**2. Run a simulation:**

```bash
# Example: Simulate inverter
ngspice inverter.cir

# Run transient analysis
ngspice> run
ngspice> plot v(in) v(out)
```

**3. View waveforms:**

![Inverter Waveform](../media/sim_ngspice_inverter_waveform.png)
*NOT gate transient analysis showing input/output inversion*

> **Evidence:** SPICE simulations validate transistor-level correctness.

---

## Running Tests

### Quick Test (No Dependencies)

```bash
# From project root
./run_tests.sh

# Or directly
python3 test/test_alu.py
```

### Full Test Suite with pytest

```bash
# Install pytest (one-time)
pip3 install pytest

# Run all tests
cd test
pytest test_alu.py -v

# Run specific operation tests
pytest test_alu.py -k "ADD_TEST" -v

# Run with coverage
pytest test_alu.py --cov --cov-report=html
```

### Test Output

```
test_alu.py::test_load_vectors PASSED                              [  0%]
test_alu.py::test_alu_operation[ADD_TEST_001_A00_B00] PASSED      [  0%]
test_alu.py::test_alu_operation[ADD_TEST_002_A01_B5F] PASSED      [  0%]
...
test_alu.py::TestArithmetic::test_add_simple PASSED               [ 99%]
test_alu.py::TestFlags::test_overflow_flag PASSED                 [100%]

======================== 1900 passed in 2.45s ==========================
```

![Test Vector Screenshot](../media/test_script_vector_screenshot.png)
*Test vector execution showing comprehensive coverage*

> **Evidence:** 1,900 test vectors provide 100% operation coverage.

### Understanding Test Results

- **1,900 parametrized tests**: 100 tests per operation × 19 operations
- **Manual unit tests**: ~25 additional focused tests
- **Coverage**: All operations, edge cases, flags
- **Golden model**: Python reference implementation

See [test/README.md](../test/README.md) for detailed testing guide.

---

## Hardware Setup

### Component Checklist

Before starting hardware assembly, verify you have:

- [ ] All PCBs fabricated and inspected
- [ ] All components ordered and received
- [ ] Soldering equipment ready
- [ ] Testing equipment available (multimeter, oscilloscope)
- [ ] 5V power supply
- [ ] Arduino boards (2x) programmed with firmware

### Assembly Steps

**1. Inspect PCBs:**
- Check for manufacturing defects
- Verify silkscreen and component labels
- Test for shorts between power and ground

**2. Solder components (smallest to largest):**
- SMD resistors and capacitors (if any)
- Transistors (MOSFETs)
- IC sockets (recommended) or ICs directly
- Headers and connectors
- LEDs and displays

**3. Visual inspection:**
- Check all solder joints
- Look for bridges or cold joints
- Verify component orientation (especially ICs and transistors)

**4. Continuity testing:**
- Test power rails (no shorts)
- Verify critical connections
- Check ground continuity

**5. Power-on test:**
- Apply 5V power
- Measure voltages at key points
- Check for excessive current draw
- Look for hot components

**6. Functional testing:**
- Test individual gates
- Test adder circuits
- Test complete ALU operations
- Verify flags generation

### Arduino Firmware

**Controller Input (Arduino #1):**

```bash
cd miscellaneous/firmware/controller-input
# Open controller_input.ino in Arduino IDE
# Select board: Arduino Uno (or your board)
# Upload to Arduino #1
```

**Controller Display (Arduino #2):**

```bash
cd miscellaneous/firmware/controller-display
# Open controller_display.ino in Arduino IDE
# Select board: Arduino Uno (or your board)
# Upload to Arduino #2
```

---

## Troubleshooting

### Simulation Issues

**Problem:** Logisim circuit doesn't simulate correctly

**Solutions:**
- Check for disconnected wires (red dots)
- Verify all inputs are driven
- Check clock signal is toggling
- Reset simulation: **Simulate → Reset Simulation**

**Problem:** ngspice simulation fails

**Solutions:**
- Check .cir file syntax
- Verify MOSFET models are loaded
- Check for missing ground node
- Review error messages carefully

### Test Failures

**Problem:** Tests fail with incorrect results

**Solutions:**
- Verify Python version (3.7+)
- Check test vectors are loading correctly
- Review ALU implementation logic
- Compare with golden model

**Problem:** "Module not found" errors

**Solutions:**
- Tests run standalone without dependencies
- Use `python3 test/test_alu.py` instead of pytest
- Check you're in project root directory

### Hardware Issues

**Problem:** No power / board doesn't turn on

**Solutions:**
- Check power supply voltage (should be 5V)
- Verify power connections
- Test for shorts between VCC and GND
- Check fuse (if present)

**Problem:** Incorrect logic levels

**Solutions:**
- Verify component values (resistors)
- Check transistor orientation
- Test individual gates with multimeter
- Verify power rail voltages

**Problem:** Intermittent operation

**Solutions:**
- Check solder joints (reflow if needed)
- Verify all connections
- Check for loose wires
- Test with oscilloscope for noise

**Problem:** Gates not switching

**Solutions:**
- Verify transistor part numbers
- Check gate drive voltages
- Test transistors individually
- Verify pull-up/pull-down resistors

---

## Next Steps

### After Setup

1. **Explore the architecture:** Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Review schematics:** Navigate to `schematics/` directory
3. **Run simulations:** Try different operations in Logisim
4. **Modify and experiment:** Change operations, add features
5. **Build hardware:** Follow assembly guide above

### Learning Path

**Beginner:**
1. Understand basic gates (AND, OR, NOT)
2. Study half adder and full adder
3. Learn about ripple-carry addition
4. Explore 2's complement arithmetic

**Intermediate:**
1. Analyze complete ALU architecture
2. Study control signal generation
3. Understand flag logic
4. Learn about multiplexer selection

**Advanced:**
1. Optimize transistor count
2. Implement carry-lookahead adder
3. Add new operations
4. Design custom instructions

### Resources

- **Documentation:** [docs/](../docs/)
- **Specifications:** [spec/](../spec/)
- **Test Suite:** [test/](../test/)
- **Schematics:** [schematics/](../schematics/)
- **Logisim Files:** [logisim/](../logisim/)

### Community

- **Issues:** [GitHub Issues](https://github.com/tmarhguy/cpu/issues)
- **Discussions:** [GitHub Discussions](https://github.com/tmarhguy/cpu/discussions)
- **Contributing:** See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## Summary Checklist

### Software Setup
- [ ] Git installed and repository cloned
- [ ] Python 3.7+ installed
- [ ] Tests run successfully
- [ ] Logisim Evolution installed
- [ ] KiCad installed (for PCB viewing)
- [ ] ngspice installed (for SPICE simulation)

### Understanding
- [ ] Read project README
- [ ] Understand 8-phase build process
- [ ] Reviewed architecture overview
- [ ] Explored Logisim simulation
- [ ] Ran test suite successfully

### Hardware (if building)
- [ ] Components ordered
- [ ] PCBs fabricated
- [ ] Soldering equipment ready
- [ ] Testing equipment available
- [ ] Arduino firmware prepared

---

**You're now ready to explore the 8-Bit Transistor CPU!**

For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md).

For testing and verification, see [VERIFICATION.md](VERIFICATION.md).

For contributing, see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

**Last Updated:** 2026-01-16  
**Version:** 1.0
