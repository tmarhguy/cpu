# KiCad PCB Design Files

**Complete hardware design for the 8-bit discrete transistor ALU**

This directory contains all KiCad schematic and PCB layout files for fabrication-ready hardware.

---

## Directory Structure

```
kicad/
├── boards/              # Complete board designs
│   ├── alu/             # Main 270×270mm ALU board (if monolithic)
│   ├── add_sub/         # Add/subtract module
│   ├── flags/           # Flag generation circuit
│   ├── main_control/    # Control decoder
│   ├── main_logic/      # Logic unit
│   └── led_panel/       # Display panels
├── modules/             # Reusable subcircuits
│   ├── gates/           # Logic gate implementations
│   ├── adder/           # Adder circuits (1-bit, 2-bit, 8-bit)
│   └── mux/             # Multiplexer modules
└── README.md            # This file
```

---

## Main ALU Board

**Design:** 270mm × 270mm combinational logic processor

### Specifications

| Parameter | Value |
|-----------|-------|
| **Board Size** | 270mm × 270mm (10.6" × 10.6") |
| **Layers** | 2 (signal + ground) |
| **Transistors** | 3,856+ discrete CMOS |
| **Technology** | 5V logic, NMOS/PMOS pairs |
| **Power** | 5V @ 0.5-1A |
| **I/O** | 22 pins (8× A, 8× B, 5× FUNC, 1× GND) |
| **Outputs** | 12 pins (8× OUT, 4× FLAGS) |

### Board Sections

1. **Arithmetic Unit** (top-left)
   - 8-bit ripple-carry adder
   - XOR array for B input
   - 432 transistors

2. **Logic Unit** (top-right)
   - NAND/NOR/XOR arrays
   - PASS A/B buffers
   - 5:1 MUX
   - 352 transistors

3. **Selection Logic** (center)
   - 2:1 MUX (arithmetic vs logic)
   - Global inverter
   - 176 transistors

4. **Flag Generation** (bottom-left)
   - EQUAL comparator
   - LESS comparator
   - POSITIVE detector
   - COUT routing
   - ~240 transistors

5. **Control Decoder** (bottom-right)
   - FUNC[4:0] opcode decoder
   - Control signal generation
   - ~68 transistors

![Main Logic Board](../../media/pcb/layouts/main_logic.png)
*Figure 1 - Main ALU logic board: 270×270mm with 3,856+ transistors*

**Evidence:** Physical PCB fabricated and assembled.

---

## File Formats

### KiCad Project Files

| Extension | Purpose | Version Control |
|-----------|---------|-----------------|
| `.kicad_pro` | Project settings | Track |
| `.kicad_sch` | Schematic | **Track (critical)** |
| `.kicad_pcb` | PCB layout | **Track (critical)** |
| `.kicad_sym` | Custom symbols | Track |
| `.kicad_mod` | Custom footprints | Track |
| `-backups/` | Auto-backups | Ignore |
| `fp-info-cache` | Footprint cache | Ignore |

### Export Formats

| Format | Purpose | Location |
|--------|---------|----------|
| **PDF** | Documentation | Export as needed |
| **SVG** | Vector schematics | `media/schematics photos svg/` |
| **Gerber** | Manufacturing | Generated on demand |
| **BOM** | Component list | `docs/build-notes/bom.md` |
| **STEP** | 3D mechanical | `web/glb exports/` |

---

## Board Designs

### Main Logic Board

**File:** `boards/main_logic/main_logic.kicad_sch`

![Main Logic Schematic](../media/schematics photos svg/main_logic.svg)
*Figure 2 - Complete main logic schematic*

**Key Components:**
- 640+ discrete transistors
- 74HC157 2:1 MUX (2×)
- Power distribution network
- I/O headers

**Interfaces:**
```
Inputs:  A[7:0], B[7:0], FUNC[4:0], VCC, GND
Outputs: OUT[7:0], LESS, EQUAL, POSITIVE, COUT
```

**Evidence:** Complete schematic shows all signal paths.

### Add/Sub Module

**File:** `boards/add_sub/add_sub.kicad_sch`

![Add/Sub Schematic](../../media/schematics/boards/add_sub_page-0001.jpg)
*Figure 3 - Add/subtract module with XOR array*

**Function:** Conditional B inversion for subtraction

**Components:**
- 8× XOR gates (96T)
- M control signal routing

**Logic:** B' = B XOR M

**Evidence:** XOR array enables efficient ADD/SUB implementation.

### Flags Board

**File:** `boards/flags/flags.kicad_sch`

![Flags Schematic](../../media/schematics/boards/flags.svg)
*Figure 4 - Flag generation circuit*

**Flags generated:**
- EQUAL: A == B comparator (~100T)
- LESS: A < B magnitude comparator (~120T)
- POSITIVE: (OUT > 0) detector (~20T)
- COUT: Carry out routing (0T)

**Evidence:** Dedicated flag logic provides comparison results.

### Control Unit

**File:** `boards/main_control/main_control.kicad_sch`

![Control Schematic](../../media/schematics/boards/main_control.svg)
*Figure 5 - Control unit opcode decoder*

**Function:** FUNC[4:0] → {M, MUX_SEL, INV_OUT, LOGIC_SEL}

**Implementation:** Combinational decode logic (~68T)

**Evidence:** Control decoder translates opcodes to internal control signals.

---

## PCB Design Process

### Step 1: Schematic Capture

![Schematic Design](../../media/design/kicad/design_kicad_alu_schematic.jpg)
*Figure 6 - Schematic capture in KiCad*

**Process:**
1. Create hierarchical design
2. Place components
3. Wire connections
4. Add power symbols
5. Annotate references
6. Run ERC (Electrical Rules Check)

### Step 2: PCB Layout

![PCB Layout](../../media/design/kicad/design_kicad_alu_pcb_layout.png)
*Figure 7 - PCB layout for ALU*

**Process:**
1. Import netlist
2. Define board outline (270×270mm)
3. Place components strategically
4. Route power rails (wide traces)
5. Route signals
6. Add ground plane
7. Run DRC (Design Rules Check)

### Step 3: Routing

[![Routing Demo](../../media/design/kicad/design_kicad_alu_pcb_layout.png)](../../media/videos/process/begining-routing-kicad-screenrecord.mp4)
*Figure 8 - Click to watch: PCB routing demonstration*

**Routing strategy:**
- Power rails first (1mm+ traces)
- Critical signals (clock-free, so no priority)
- Minimize via count
- Maintain trace spacing (0.2mm min)

**Evidence:** Routing video shows systematic layout approach.

---

## Manufacturing

### Gerber Generation

**Process:**
```
KiCad → File → Fabrication Outputs → Gerbers
```

**Generated files:**
- Copper layers (Top, Bottom)
- Solder mask layers
- Silkscreen layers
- Drill files (.drl)
- Board outline

### PCB Ordering

**Recommended manufacturers:**
- **JLCPCB** - Economical, good quality
- **PCBWay** - Higher quality options
- **OSH Park** - USA-based, excellent quality

**Specifications to provide:**
- Board size: 270×270mm
- Layers: 2
- Thickness: 1.6mm
- Copper: 1oz
- Surface finish: HASL lead-free
- Silkscreen: White on green

**Cost estimate:** ~$100 for 270×270mm board

---

## Assembly Notes

### Component Placement Order

1. **Smallest first:** Resistors, capacitors (if SMD)
2. **Transistors:** 3,856+ NMOS/PMOS pairs
3. **ICs:** 74HC157 multiplexers (use sockets)
4. **Headers:** I/O connectors
5. **LEDs:** Output indicators (last)

### Soldering Tips

- **Temperature:** 320-350°C for lead-free solder
- **Tip size:** Fine chisel (1-2mm) for transistor leads
- **Flux:** Use liberally for better flow
- **Inspection:** Magnification recommended
- **Testing:** Test subsystems before full integration

![Component Placement](../../media/photos/assembly/not_closeup_soldered_mosfets.jpg)
*Figure 9 - Component placement before soldering*

![Soldering Progress](../../media/photos/assembly/not_closeup_soldered_mosfets.jpg)
*Figure 10 - Hand soldering 3,856+ transistors*

**Evidence:** Assembly process documented step-by-step.

---

## Design Files

### Opening in KiCad

```bash
cd schematics/kicad/boards/main_logic
kicad main_logic.kicad_pro
```

**KiCad version:** 7.0 or later required

### Exporting

**Schematic PDF:**
```
File → Plot → Plot format: PDF
```

**Schematic SVG:**
```
File → Plot → Plot format: SVG
```

**PCB 3D View:**
```
View → 3D Viewer → File → Export → STEP
```

---

## References

- [Board Documentation](boards/README.md) - Individual board details
- [Modules](modules/README.md) - Reusable subcircuits
- [Architecture](../../docs/ARCHITECTURE.md) - System architecture
- [BOM](../../docs/build-notes/bom.md) - Bill of materials

---

**Last Updated:** 2026-01-16  
**KiCad Version:** 7.0+  
**Board Count:** 8 designs  
**Status:** Fabrication-ready
