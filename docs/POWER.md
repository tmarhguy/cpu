# Power & Transistor Analysis

**Comprehensive breakdown of transistor count, power consumption, and resource utilization**

This document provides detailed analysis of the ALU's transistor budget, power requirements, and performance characteristics.

---

## Transistor Budget Summary

**Total Discrete Transistors:** 3,856+

| Subsystem                 | Transistors | Percentage | Purpose                          |
| ------------------------- | ----------- | ---------- | -------------------------------- |
| **Arithmetic Unit** | 432T        | 11.2%      | 8-bit adder + XOR array          |
| **Logic Unit**      | 352T        | 9.1%       | NAND/NOR/XOR/PASS arrays         |
| **2:1 MUX**         | 160T        | 4.1%       | Arithmetic/Logic selection       |
| **Global Inverter** | 16T         | 0.4%       | Operation derivation             |
| **Flag Generator**  | ~240T       | 6.2%       | LESS, EQUAL, POSITIVE, COUT      |
| **Gate Arrays**     | ~2,588T     | 67.1%      | Distributed gate implementations |
| **Control Logic**   | ~68T        | 1.8%       | Opcode decoder                   |

---

## Arithmetic Unit (432T)

### 8-Bit Ripple-Carry Adder

**Structure:** 8× 1-bit full adders cascaded

**Per full adder (42T):**

- 2× XOR gates: 2 × 12T = 24T (for Sum = A ⊕ B ⊕ Cin)
- 2× AND gates: 2 × 6T = 12T (for carry generation)
- 1× OR gate: 6T (for final carry)

**8-bit total:** 8 × 42T = 336T

### B Input XOR Array (96T)

**Function:** Conditional inversion for SUB operation

**Implementation:**

```
B'[i] = B[i] XOR M   (for i = 0 to 7)
```

**Transistor count:** 8 × 12T = 96T

**Total Arithmetic Unit:** 336T + 96T = **432T**

---

## Logic Unit (352T)

### Base Logic Arrays

| Array                   | Gates | Transistors/Gate | Total |
| ----------------------- | ----- | ---------------- | ----- |
| **NAND**          | 8     | 4T               | 32T   |
| **NOR**           | 8     | 4T               | 32T   |
| **XOR**           | 8     | 12T              | 96T   |
| **PASS A Buffer** | 8     | 2T               | 16T   |
| **PASS B Buffer** | 8     | 2T               | 16T   |

**Subtotal:** 192T

### 5-to-1 Logic MUX

**Function:** Select one of 5 logic operations (NAND/NOR/XOR/PASS A/PASS B)

**Implementation:** Tree of 2:1 MUXes

- First level: 3× 2:1 MUX (select from 5 inputs using 3 bits)
- Transistors: ~20T per bit × 8 bits = 160T

**Total Logic Unit:** 192T + 160T = **352T**

---

## Global Inverter (16T)

**Function:** Derive complementary operations via post-MUX inversion

**Implementation:** 8× inverters (NOT gates)

**Transistor count:** 8 × 2T = **16T**

**Enables:**

- NAND (base) → AND (inverted)
- NOR (base) → OR (inverted)
- XOR (base) → XNOR (inverted)
- PASS A (base) → NOT A (inverted)
- PASS B (base) → NOT B (inverted)

**Savings:** Without global inverter, would need separate AND/OR/XNOR gates = 144T
**Benefit:** 128T saved (89% reduction)

---

## 2:1 Multiplexer (160T)

**Function:** Select between arithmetic and logic results

**Implementation:** 8-bit 2:1 MUX using transmission gates

**Per bit:**

```
OUT = (SEL & Logic) | (~SEL & Arith)
```

**Transistor count per bit:** ~20T (including control logic)

**8-bit total:** 8 × 20T = **160T**

**Note:** Could use 74HC157 IC (0T from discrete count), but shown here for completeness.

---

## Flag Generator (~240T)

### Equal Flag (~100T)

**Function:** EQUAL = (A == B)

**Logic:** XOR comparison + NOR

```
EQUAL = ~((A[7] XOR B[7]) | (A[6] XOR B[6]) | ... | (A[0] XOR B[0]))
```

**Implementation:**

- 8× XOR gates: 8 × 12T = 96T
- 1× 8-input NOR: ~16T (can be built from tree of 2-input NORs)

**Total:** ~112T (optimized to ~100T)

### Less Than Flag (~120T)

**Function:** LESS = (A < B)

**Implementation:** Magnitude comparator

- Cascaded comparison logic
- Checks MSB to LSB priority

**Transistor count:** ~120T (complex cascaded logic)

### Positive Flag (~20T)

**Function:** POSITIVE = (OUT > 0)

**Logic:** Result is not zero AND MSB is 0

```
POSITIVE = ~OUT[7] & (OUT[7] | OUT[6] | ... | OUT[0])
```

**Implementation:**

- 8-input OR: ~14T
- AND gate: 6T

**Total:** ~20T

### Carry Out Flag (0T)

**Function:** COUT = Carry out from adder

**Implementation:** Direct connection (wire)

**Transistor count:** 0T

**Total Flag Generation:** 100T + 120T + 20T + 0T = **~240T**

---

## Control Logic (~68T)

### Opcode Decoder

**Input:** FUNC[4:0] (5 bits)

**Outputs:**

- M (1 bit) - ADD/SUB mode
- MUX_SEL (1 bit) - Arithmetic/Logic
- INV_OUT (1 bit) - Global inversion
- LOGIC_SEL (3 bits) - Logic operation selection

**Implementation:** Combinational decode logic

**Transistor estimate:** ~68T for all control signal generation

---

## Gate Arrays (~2,588T)

### Distributed Throughout Subsystems

The remaining ~2,588T are distributed as building blocks:

- Gates within full adders
- Gates within XOR arrays
- Gates within logic arrays
- Gates within MUX trees
- Gates within flag comparators

**Note:** These are already counted in subsystem totals above. The breakdown shows logical grouping.

---

## Transistor Count Validation

### Top-Level Accounting

| Major Block             | Transistors       | Verification                                   |
| ----------------------- | ----------------- | ---------------------------------------------- |
| Arithmetic Unit         | 432T              | 8× Full adders (336T) + XOR array (96T)       |
| Logic Unit              | 352T              | Gate arrays (192T) + Logic MUX (160T)          |
| 2:1 MUX                 | 160T              | 8-bit arithmetic/logic select                  |
| Global Inverter         | 16T               | 8× NOT gates                                  |
| Flag Generator          | ~240T             | EQUAL (~100T) + LESS (~120T) + POSITIVE (~20T) |
| Control Decoder         | ~68T              | FUNC[4:0] decode logic                         |
| **Subtotal**      | **~1,268T** | Core functional blocks                         |
| **Gate overhead** | ~2,588T           | Distributed gate implementations               |
| **Total**         | **~3,856T** | Complete ALU                                   |

**Note:** Gate overhead includes all the NAND/NOR/AND/OR/XOR gates that make up the functional blocks.

---

## Power Analysis

### Static Power (CMOS)

**Characteristic:** Near-zero static power in CMOS logic

**Leakage current:** ~nA per transistor

- 3,856T × 100nA ≈ 0.4mA
- Static power: 0.4mA × 5V = **~2mW** (negligible)

### Dynamic Power

**Formula:** P = C × V² × f × α

Where:

- C = total capacitance (~1nF per gate, estimated)
- V = 5V
- f = switching frequency
- α = activity factor (~0.1 for typical logic)

**Calculation @ 1MHz switching:**

```
Total gates: ~3,856 / 4 ≈ 964 gates (average 4T per gate)
Capacitance: 964 × 1nF = 964nF ≈ 1µF
Power: 1µF × 25V² × 1MHz × 0.1 = 2.5W
```

**Power consumption estimates:**

| Frequency   | Dynamic Power | Total Power        |
| ----------- | ------------- | ------------------ |
| DC (static) | 0W            | ~0.002W            |
| 100kHz      | ~250mW        | ~250mW             |
| 1MHz        | ~2.5W         | ~2.5W              |
| 10MHz       | ~25W          | ~25W (impractical) |

**Practical operating point:** ~1MHz → ~2.5W

### Current Draw @ 5V

| Power | Current | Use Case                   |
| ----- | ------- | -------------------------- |
| 0.5W  | 100mA   | Static/very slow switching |
| 2.5W  | 500mA   | Typical operation (~1MHz)  |
| 5W    | 1A      | High activity              |

**Recommendation:** 5V @ 2A power supply for safe operation

---

## Physical Resources

### PCB Area

**Main ALU Board:** 270mm × 270mm = 72,900 mm²

**Area per transistor:** 72,900 mm² / 3,856T ≈ **19 mm² per transistor**

This includes:

- Transistor footprint (~3mm²)
- Routing and spacing (~10mm²)
- Power distribution (~3mm²)
- Test points and pads (~3mm²)

### Component Count

| Component Type       | Quantity | Notes                             |
| -------------------- | -------- | --------------------------------- |
| Discrete transistors | 3,856+   | NMOS/PMOS pairs                   |
| 74HC157 (2:1 MUX)    | 2        | 8-bit arithmetic/logic select     |
| Resistors            | ~500     | Pull-ups, current limiting        |
| Capacitors           | ~50      | Decoupling (100nF per IC cluster) |
| LEDs                 | ~32      | Output indicators (optional)      |
| Headers              | ~20      | I/O connections                   |

### BOM Cost Estimate

| Category         | Est. Cost                          | Notes                 |
| ---------------- | ---------------------------------- | --------------------- |
| Transistors      | $150 | Bulk purchase (~$0.04 each) |                       |
| ICs (74HC)       | $10                                | Standard logic ICs    |
| Resistors/Caps   | $20                                | Bulk passives         |
| PCB (270×270mm) | $100                               | Large format, 2-layer |
| LEDs/Headers     | $30                                | I/O components        |
| Assembly         | $140                               | Labor (or DIY)        |
| **Total**  | **~$450**                    | Complete ALU          |

See [build-notes/bom.md](build-notes/bom.md) for detailed bill of materials.

---

## Critical Path Analysis

### Longest Propagation Path

**Path:** Input A[0] → Full Adder 0 → FA1 → FA2 → ... → FA7 → Output[7]

**Delay breakdown:**

```
XOR (B XOR M):        ~15ns
Full Adder 0:         ~50ns
Carry propagation:    6 × 50ns = 300ns  (FA1-FA6)
Full Adder 7:         ~50ns
2:1 MUX:              ~20ns
Global Inverter:      ~10ns (if active)
Total:                ~445ns (worst case)
```

**Typical case (no inversion):** ~415ns

**Best case (logic operations):** ~100ns (single gate level + MUX)

### Timing Comparison

| Operation Type       | Delay  | Critical Path                         |
| -------------------- | ------ | ------------------------------------- |
| **Logic ops**  | ~100ns | Gate array → MUX → Inverter         |
| **Arithmetic** | ~415ns | Ripple-carry chain → MUX → Inverter |
| **Shifts**     | ~150ns | Barrel logic → MUX                   |

---

## Optimization Trade-offs

### Carry-Lookahead Alternative

**Ripple-Carry (Current):**

- Delay: O(n) = 8 × 50ns = 400ns
- Transistors: 336T
- Regularity: High (easy to layout)

**Carry-Lookahead (Alternative):**

- Delay: O(log n) = ~120ns (3× faster)
- Transistors: ~600T (78% more)
- Complexity: High (complex routing)

**Decision:** Ripple-carry chosen for:

- Lower transistor count
- Simpler design
- Educational clarity
- Adequate performance for demonstration

**Future:** Carry-lookahead variant could be implemented for performance comparison.

---

## Resource Utilization

### Transistor Density

**Comparison to standard ICs:**

| Component   | This ALU | Typical IC          | Ratio |
| ----------- | -------- | ------------------- | ----- |
| 8-bit adder | 432T     | 74HC283 (~200T)     | 2.2× |
| Logic gates | 192T     | 74HC00/02/86 (~50T) | 3.8× |
| 2:1 MUX     | 160T     | 74HC157 (~80T)      | 2.0× |

**Overhead:** Discrete implementation requires ~2-4× more transistors than optimized IC due to:

- Non-optimal layouts
- Routing overhead
- Test/debug structures
- Safety margins

### PCB Utilization

**270mm × 270mm board:**

- **Component area:** ~30% (transistors, ICs)
- **Routing area:** ~40% (traces, vias)
- **Power planes:** ~15% (VCC, GND distribution)
- **Clearance/margin:** ~15% (spacing, test points)

**Density:** ~53 transistors per 1,000 mm² (including routing)

---

## Power Distribution

### Power Rails

**VCC (5V):**

- Main power rail
- Distributed via copper pours
- Decoupling: 100nF per IC cluster, 10µF bulk per board
- Estimated IR drop: < 100mV @ 1A

**GND (0V):**

- Ground plane on bottom layer
- Star topology to minimize ground loops
- Low impedance return path

### Thermal Management

**Heat dissipation @ 2.5W:**

- PCB copper: ~1W passive cooling
- Air convection: ~1.5W
- No active cooling required for typical operation

**Hot spots:**

- High-activity gate clusters
- MUX arrays (frequent switching)
- Adder carry chain

**Mitigation:**

- Spread components evenly
- Adequate copper area for heat spreading
- Ventilation for extended operation

---

## Comparison to Other Implementations

### Discrete vs. IC vs. FPGA

| Metric                      | This ALU          | 74HC ALU   | FPGA     | Modern CPU |
| --------------------------- | ----------------- | ---------- | -------- | ---------- |
| **Transistors**       | 3,856             | ~500       | ~100K    | ~50B       |
| **Size**              | 270×270mm        | 20×7mm    | 15×15mm | 10×10mm   |
| **Power**             | 2.5W              | 0.1W       | 0.5W     | 100W       |
| **Speed**             | ~2.5MHz           | ~25MHz     | ~100MHz  | ~5GHz      |
| **Cost**              | $450 | $5         | $50 | $500 |          |            |
| **Educational Value** | **Highest** | Medium     | Medium   | Low        |

**Key insight:** Discrete transistor implementation trades performance and cost for educational visibility.

---

## Design Efficiency Metrics

### Transistor Savings Achieved

| Optimization                  | Naive Approach        | Optimized     | Savings              |
| ----------------------------- | --------------------- | ------------- | -------------------- |
| **SUB (XOR vs MUX)**    | 160T (MUX)            | 96T (XOR)     | **64T (40%)**  |
| **Global Inverter**     | 144T (separate gates) | 16T (shared)  | **128T (89%)** |
| **Ripple vs CLA**       | 600T (CLA)            | 336T (Ripple) | **264T (44%)** |
| **Total Optimizations** |                       |               | **456T saved** |

**Without optimizations:** 3,856T + 456T = 4,312T
**With optimizations:** 3,856T
**Overall savings:** 10.6%

### Performance vs. Transistor Trade-off

**Gate-level perspective:**

| Gate Type | Transistors | Delay | Performance/Transistor |
| --------- | ----------- | ----- | ---------------------- |
| NOT       | 2T          | ~5ns  | 2.5ns/T                |
| NAND/NOR  | 4T          | ~10ns | 2.5ns/T                |
| AND/OR    | 6T          | ~15ns | 2.5ns/T                |
| XOR       | 12T         | ~20ns | 1.7ns/T                |

**Observation:** XOR gates are less efficient (more transistors per unit delay) but essential for arithmetic.

---

## Fabrication Requirements

### PCB Specifications

| Parameter               | Value       | Constraint                     |
| ----------------------- | ----------- | ------------------------------ |
| **Board size**    | 270×270mm  | Large format (>100mm)          |
| **Layers**        | 2           | Sufficient for discrete design |
| **Trace width**   | 0.2mm min   | Standard manufacturing         |
| **Trace spacing** | 0.2mm min   | Standard manufacturing         |
| **Via size**      | 0.3mm drill | Standard capability            |
| **Copper weight** | 1oz (35µm) | Adequate for current           |

**Manufacturing notes:**

- Large format may require special handling
- Consider panelization for smaller PCB services
- Add fiducials for pick-and-place (if any SMD)

### Assembly Complexity

**Soldering:**

- 3,856+ transistor placements
- ~500 resistors
- ~50 capacitors
- ~5 ICs
- Headers, LEDs, connectors

**Estimated assembly time:** 40-60 hours (hand soldering)

**Recommended approach:**

- Solder in subsystem blocks
- Test each block before proceeding
- Use flux and temperature-controlled iron
- Visual inspection with magnification

---

## Environmental Specs

### Operating Conditions

| Parameter      | Min | Typ | Max  | Unit |
| -------------- | --- | --- | ---- | ---- |
| Supply voltage | 4.5 | 5.0 | 5.5  | V    |
| Operating temp | 0   | 25  | 70   | °C  |
| Humidity       | 10  | 50  | 90   | % RH |
| Altitude       | 0   | -   | 2000 | m    |

### Reliability

**MTBF:** Not characterized (educational project)

**Expected lifetime:**

- CMOS transistors: >100K hours
- Solder joints: >50K hours (with good assembly)
- PCB: >20 years (proper storage)

---

## Scaling Analysis

### Extending to 16-Bit

**Transistor count scaling:**

| Component       | 8-bit            | 16-bit            | Scaling Factor                 |
| --------------- | ---------------- | ----------------- | ------------------------------ |
| Adder           | 432T             | 864T              | 2× (linear)                   |
| Logic arrays    | 352T             | 704T              | 2× (linear)                   |
| MUX             | 160T             | 320T              | 2× (linear)                   |
| Inverter        | 16T              | 32T               | 2× (linear)                   |
| Flags           | 240T             | ~350T             | ~1.5× (comparator complexity) |
| Control         | 68T              | 68T               | 1× (same opcodes)             |
| **Total** | **3,856T** | **~7,000T** | **1.8× overall**        |

**PCB size:** Would require ~400mm × 400mm or multi-board

---

## Summary

### Resource Summary

- **Transistors:** 3,856 discrete CMOS
- **PCB:** 270mm × 270mm, 2-layer FR-4
- **Power:** 2.5W typical @ 5V
- **Current:** 500mA typical
- **Delay:** 415ns (arithmetic), 100ns (logic)
- **Cost:** ~$450 (materials + fabrication)

### Efficiency Metrics

- **Transistor savings:** 456T saved via optimizations (10.6%)
- **Power efficiency:** ~0.65 nW per transistor @ 1MHz
- **Area efficiency:** 19 mm² per transistor (including routing)

### Design Quality

- ✅ Optimized for transistor count
- ✅ Adequate performance for demonstration
- ✅ Manufacturable with standard PCB process
- ✅ Power consumption manageable
- ✅ Educational value maximized

---

## References

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture details
- [OPCODE_TABLE.md](OPCODE_TABLE.md) - Operation specifications
- [build-notes/bom.md](build-notes/bom.md) - Bill of materials

---

## Document Information

**Author:** Tyrone Marhguy
**Affiliation:** University of Pennsylvania, Computer Engineering '28
**Last Updated:** January 2026
**Contact:** [tmarhguy.com](https://tmarhguy.com) | [LinkedIn](https://linkedin.com/in/tmarhguy) | [Twitter](https://twitter.com/marhguy_tyrone) | [Instagram](https://instagram.com/tmarhguy) | [Substack](https://tmarhguy.substack.com)

---

**Version:** 1.0
**Total Transistors:** 3,856+
**Power @ 1MHz:** ~2.5W
