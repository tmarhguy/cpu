# Troubleshooting Guide

**Common issues and solutions for the 8-bit discrete transistor ALU**

This guide covers simulation, hardware, and testing issues you might encounter when building or replicating this project.

---

## Table of Contents

- [Simulation Issues](#simulation-issues)
- [Hardware Issues](#hardware-issues)
- [Testing Issues](#testing-issues)
- [Common Mistakes](#common-mistakes)
- [Debugging Techniques](#debugging-techniques)
- [Getting Help](#getting-help)

---

## Simulation Issues

### Logisim Evolution

**Problem:** Outputs show "X" (undefined) or "E" (error)

**Solutions:**
1. **Check input connections:**
   - All inputs must be connected (A[7:0], B[7:0], FUNC[4:0])
   - Floating inputs cause undefined behavior
   - Use constant inputs (0 or 1) for testing

2. **Verify clock signals (if using external system):**
   - Clock must toggle for sequential elements
   - Check clock frequency (not too fast)
   - Ensure clock reaches all components

3. **Check for short circuits:**
   - Wires crossing without junctions
   - Multiple outputs driving same wire
   - Use "Analyze Circuit" tool to detect conflicts

**Problem:** Simulation is very slow

**Solutions:**
- Reduce simulation speed (Simulate → Tick Frequency)
- Disable unused components
- Use subcircuits to organize complex logic
- Close other applications to free RAM

**Problem:** Can't load circuit file

**Solutions:**
- Ensure Logisim Evolution version 3.8.0+
- Check file path (no special characters)
- Try opening in text editor to check for corruption
- Re-download from repository

---

### SPICE Simulation

**Problem:** Convergence errors

**Solutions:**
1. **Adjust simulation parameters:**
   ```spice
   .options reltol=1e-3
   .options abstol=1e-9
   .options vntol=1e-4
   ```

2. **Check MOSFET models:**
   - Ensure 2N7000 (NMOS) and BS250 (PMOS) models loaded
   - Verify model parameters (Vth, Kp, Lambda)
   - Use `.include` directive for model files

3. **Reduce timestep:**
   ```spice
   .tran 1n 1u 0 10p
   ```

**Problem:** Incorrect output voltages

**Solutions:**
- **Check power supply:** VDD = 5V, VSS = 0V
- **Verify MOSFET connections:** Source, drain, gate, bulk
- **Check pull-up/pull-down resistors:** Typical 10kΩ
- **Measure node voltages:** Use `.print V(node)` directive

**Problem:** Slow simulation

**Solutions:**
- Use larger timesteps for DC analysis
- Reduce simulation duration
- Simplify circuit (test subcircuits separately)
- Use faster SPICE engine (ngspice vs. LTspice)

---

### Python Test Framework

**Problem:** `ModuleNotFoundError` or import errors

**Solutions:**
```bash
# Install dependencies
pip install -r test/requirements.txt

# Verify Python version (must be 3.7+)
python --version

# Check pytest installation
pytest --version
```

**Problem:** Tests fail with "golden model mismatch"

**Solutions:**
1. **Verify test vectors:**
   - Check `test/vectors/` files are not corrupted
   - Re-generate vectors: `python test/scripts/generate_exhaustive_tests.py`

2. **Check ALU implementation:**
   - Compare with Logisim simulation
   - Verify opcode decoding
   - Test individual operations

3. **Update golden model:**
   - If intentional design change, update `test/test_alu.py`

**Problem:** Slow test execution

**Solutions:**
- Run quick test: `./run_tests.sh` (1,900 tests instead of 1.24M)
- For exhaustive testing: `./run_tests.sh exhaustive` (runs all test vectors)
- Use parallel execution: `pytest -n auto` (if pytest installed)

---

## Hardware Issues

### Power-On Issues

**Problem:** No output on power-up

**Checklist:**
1. ✅ **Verify power supply:**
   - Measure VCC at IC pins: 5.0V ± 0.25V
   - Check GND continuity across board
   - Ensure adequate current (1A+ supply)

2. ✅ **Check polarity:**
   - Power connector: red = +5V, black = GND
   - Electrolytic capacitors: stripe = negative
   - MOSFETs: verify pinout (2N7000 vs BS250)

3. ✅ **Inspect solder joints:**
   - No cold solder joints (dull, grainy appearance)
   - No bridges between pins
   - All pins soldered (check under ICs)

4. ✅ **Test decoupling capacitors:**
   - 100nF ceramic per IC cluster
   - Measure with multimeter (should be ~100nF)
   - Check for shorts (should not be 0Ω)

**Problem:** Board gets hot

**Causes:**
- ❌ Short circuit (VCC to GND)
- ❌ Reversed MOSFET (drain/source swapped)
- ❌ Missing current-limiting resistors on LEDs
- ❌ Excessive fanout (one gate driving too many inputs)

**Solutions:**
- Power off immediately
- Use thermal camera or finger to locate hot spot
- Check for solder bridges near hot area
- Measure resistance VCC to GND (should be >1kΩ)

---

### Arithmetic Operations

**Problem:** Incorrect addition results

**Checklist:**
1. **Test carry chain:**
   - Inject known values at each full adder
   - Scope carry-out at each stage
   - Should propagate LSB → MSB in ~400ns

2. **Verify XOR array:**
   - Test ADD mode (M=0): B should pass unchanged
   - Test SUB mode (M=1): B should be inverted
   - Scope B and B' signals

3. **Check full adder connections:**
   - A, B, Cin → FA → Sum, Cout
   - Carry chain: FA0.Cout → FA1.Cin → ... → FA7.Cout
   - No missing or swapped wires

**Problem:** Subtraction doesn't work

**Causes:**
- M bit not connected to XOR array
- M bit not connected to Cin of first adder
- Incorrect 2's complement implementation

**Test procedure:**
```
1. Set A = 10 (0x0A), B = 5 (0x05), M = 1 (SUB)
2. Expected: B' = 250 (0xFA), Cin = 1
3. Expected: OUT = 10 + 250 + 1 = 5 (0x05)
4. Scope: B[0] should be inverted when M=1
```

**Problem:** Carry flag incorrect

**Solutions:**
- Check connection from FA7.Cout to COUT flag
- Verify flag polarity (active high or low?)
- Test with known overflow: 200 + 100 = 44 (overflow, COUT=1)

---

### Logic Operations

**Problem:** Logic operations work, arithmetic fails

**Likely cause:** Adder carry chain broken

**Isolation test:**
1. Force MUX_SEL = 1 (select logic path)
2. Test NAND, NOR, XOR, PASS operations
3. If logic works, problem is in arithmetic unit

**Problem:** All logic operations give same result

**Causes:**
- LOGIC_SEL not connected to logic MUX
- MUX control pins shorted
- Incorrect MUX wiring

**Test procedure:**
```
Set A = 0xFF, B = 0x0F
Expected results:
- NAND: 0xF0
- NOR:  0x00
- XOR:  0xF0
- AND:  0x0F (NAND + global invert)
- OR:   0xFF (NOR + global invert)
```

**Problem:** AND/OR/XNOR don't work, but NAND/NOR/XOR do

**Cause:** Global inverter not working

**Solutions:**
- Check INV_OUT control signal
- Verify inverter gates (8× NOT gates)
- Test with scope: should invert when INV_OUT=1

---

### Flag Generation

**Problem:** EQUAL flag always 0 or always 1

**Causes:**
- XOR array not comparing all bits
- 8-input NOR gate broken
- Incorrect logic (should be NOR of all XORs)

**Test:**
```
Set A = 42, B = 42
Expected: EQUAL = 1 (all XOR outputs = 0, NOR = 1)

Set A = 42, B = 43
Expected: EQUAL = 0 (at least one XOR = 1, NOR = 0)
```

**Problem:** LESS flag incorrect

**Causes:**
- Cascaded comparator logic error
- MSB comparison not prioritized
- Incorrect bit order (big-endian vs little-endian)

**Test:**
```
Set A = 10, B = 20
Expected: LESS = 1 (A < B)

Set A = 20, B = 10
Expected: LESS = 0 (A >= B)
```

**Problem:** POSITIVE flag incorrect

**Causes:**
- OR gate not detecting non-zero
- MSB (sign bit) not inverted
- Logic: POSITIVE = ~OUT[7] & (OUT != 0)

---

## Testing Issues

### Test Vector Failures

**Problem:** Random test failures (not reproducible)

**Causes:**
- Timing issues (propagation delay not settled)
- Floating inputs (missing pull-up/pull-down)
- Noise on power supply
- Intermittent connections

**Solutions:**
- Add delay between input change and output read (500ns+)
- Add pull-down resistors to all inputs (10kΩ)
- Add more decoupling capacitors
- Re-solder suspect connections

**Problem:** Consistent failures on specific operations

**Causes:**
- Incorrect opcode decoding
- Missing control signal
- Wrong operation implementation

**Debug:**
1. Test operation in Logisim (should work)
2. Compare control signals (hardware vs. simulation)
3. Scope critical signals during operation
4. Verify opcode decoder truth table

---

## Common Mistakes

### ❌ Reversed PMOS/NMOS

**Symptom:** Gate doesn't work, may get hot

**Check:**
- 2N7000 (NMOS): Source to GND, Drain to output
- BS250 (PMOS): Source to VCC, Drain to output
- Gate: Control signal for both

**Fix:** Desolder and swap transistors

---

### ❌ Missing Pull-Down Resistors

**Symptom:** Floating inputs, erratic behavior

**Check:**
- All unused inputs should have 10kΩ to GND
- FUNC[4:0] inputs especially critical
- Control signals (M, MUX_SEL, INV_OUT)

**Fix:** Add 10kΩ resistor from input to GND

---

### ❌ Cold Solder Joints

**Symptom:** Intermittent connections, noise

**Identify:**
- Dull, grainy appearance (not shiny)
- Cracks visible under magnification
- Continuity test fails intermittently

**Fix:**
- Reflow with fresh solder
- Add flux for better wetting
- Ensure proper temperature (350°C)

---

### ❌ Insufficient Power Supply

**Symptom:** Voltage drops under load, erratic behavior

**Check:**
- Measure VCC during operation (should stay >4.75V)
- Use 1A+ power supply (not USB)
- Check voltage at far end of board (IR drop)

**Fix:**
- Use higher current supply
- Add bulk capacitors (100µF electrolytic)
- Improve power distribution (wider traces)

---

### ❌ Incorrect Propagation Delay Assumptions

**Symptom:** Tests fail, but circuit is correct

**Issue:** Not waiting long enough for outputs to settle

**Fix:**
- Add 500ns delay after input change
- Scope critical path to measure actual delay
- Update test framework with correct timing

---

## Debugging Techniques

### Systematic Approach

1. **Divide and conquer:**
   - Test subsystems independently
   - Arithmetic unit alone
   - Logic unit alone
   - Flag generation alone

2. **Binary search:**
   - Test half the circuit
   - If works, problem is in other half
   - Repeat until isolated

3. **Known good inputs:**
   - Start with simple cases (A=0, B=0)
   - Progress to complex cases
   - Compare with simulation

### Tools

**Multimeter:**
- Measure DC voltages (VCC, GND, logic levels)
- Check continuity (solder joints, traces)
- Test resistors, capacitors

**Oscilloscope:**
- Measure propagation delay
- Observe signal integrity (ringing, overshoot)
- Capture transient behavior
- Trigger on specific events

**Logic Analyzer:**
- Capture multiple signals simultaneously
- Decode bus transactions
- Measure timing relationships
- Export to VCD for analysis

**Thermal Camera:**
- Locate hot spots (shorts, incorrect components)
- Verify even power distribution
- Identify high-power dissipation areas

---

## Getting Help

### Before Asking

**Provide:**
1. **Clear description of problem:**
   - What you expected
   - What actually happened
   - Steps to reproduce

2. **Evidence:**
   - Photos of board (high resolution)
   - Oscilloscope traces
   - Test output logs
   - Schematic annotations

3. **What you've tried:**
   - List troubleshooting steps
   - Measurements taken
   - Theories tested

### Where to Ask

**GitHub Issues:** [github.com/tmarhguy/cpu/issues](https://github.com/tmarhguy/cpu/issues)
- Bug reports
- Feature requests
- General questions

**Email:** tmarhguy@gmail.com | tmarhguy@seas.upenn.edu
- Detailed technical questions
- Collaboration inquiries
- Educational use

**Social Media:**
- **Twitter:** [@marhguy_tyrone](https://twitter.com/marhguy_tyrone)
- **Instagram:** [@tmarhguy](https://instagram.com/tmarhguy)
- **Substack:** [@tmarhguy](https://tmarhguy.substack.com)

**Community:**
- [Hackaday.io](https://hackaday.io/) - Hardware community
- [EEVblog Forum](https://www.eevblog.com/forum/) - Electronics experts
- [r/ECE](https://reddit.com/r/ECE) - Electrical engineering subreddit

---

## Quick Reference

### Typical Voltages

| Signal | Logic 0 | Logic 1 | Notes |
|--------|---------|---------|-------|
| CMOS output | <0.5V | >4.5V | Clean rail-to-rail |
| CMOS input threshold | <1.5V | >3.5V | Hysteresis |
| TTL output | <0.4V | >2.4V | 74HC series |

### Typical Delays

| Component | Delay | Notes |
|-----------|-------|-------|
| Inverter | 5-10ns | Single CMOS pair |
| 2-input gate | 10-20ns | NAND, NOR, AND, OR |
| XOR gate | 15-25ns | More complex |
| Full adder | 40-60ns | Critical path |
| 8-bit adder | 350-450ns | Ripple-carry |
| Logic operation | 60-100ns | Gate + MUX |

### Test Points

**Critical signals to scope:**
1. VCC, GND (power integrity)
2. A[0], B[0] (input signals)
3. FA0.Cout, FA7.Cout (carry propagation)
4. MUX_OUT[0] (datapath)
5. OUT[0] (final output)
6. EQUAL, LESS, COUT (flags)

---

## Document Information

**Author:** Tyrone Marhguy  
**Last Updated:** January 2026  
**Version:** 1.0  
**Contact:** tmarhguy@gmail.com | tmarhguy@seas.upenn.edu  
Twitter: [@marhguy_tyrone](https://twitter.com/marhguy_tyrone) | Instagram: [@tmarhguy](https://instagram.com/tmarhguy) | Substack: [@tmarhguy](https://tmarhguy.substack.com)  
Twitter: [@marhguy_tyrone](https://twitter.com/marhguy_tyrone) | Instagram: [@tmarhguy](https://instagram.com/tmarhguy) | Substack: [@tmarhguy](https://tmarhguy.substack.com)

**Related Documents:**
- [GETTING_STARTED.md](GETTING_STARTED.md) - Setup and build guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [VERIFICATION.md](VERIFICATION.md) - Test methodology

---

**Still stuck?** Don't hesitate to open an issue or email. We're here to help!
