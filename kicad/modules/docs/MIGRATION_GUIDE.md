# KiCad Modules Migration Guide

This guide helps migrate existing KiCad projects to the new organized structure that matches the component inventory.

## Current vs. Target Structure

### AND Gates

**Current:**
```
gate_and/          (contains generic AND gate)
gate_and_8bit/     (contains 8-bit AND)
```

**Target:**
```
gate_and/
  gate_and_2in/    (2-input, 1-bit) - 10× used
  gate_and_3in/    (3-input, 1-bit) - 1× used
  gate_and_4in/    (4-input, 1-bit) - 19× used (MOST COMMON)
gate_and_8bit/     (keep for alternative designs)
```

**Action:** Review existing `gate_and/` files and move/copy to appropriate subdirectory based on input count.

### OR Gates

**Current:**
```
gate_or/           (contains generic OR gate)
gate_or_8bit/      (contains 8-bit OR)
```

**Target:**
```
gate_or/
  gate_or_2in/     (2-input, 1-bit) - 7× used
  gate_or_3in/     (3-input, 1-bit) - 1× used
gate_or_8bit/      (keep for alternative designs)
```

**Action:** Review existing `gate_or/` files and organize by input count.

### NOT Gates (Inverters)

**Current:**
```
gate_inv/
  not/             (contains generic NOT/inverter)
```

**Target:**
```
gate_inv/
  gate_inv_1bit/   (1-bit inverter) - 40× used (MOST COMMON)
  gate_inv_8bit/   (8-bit inverter) - 1× used
```

**Action:** Move existing `not/` files and organize by bit width.

### NAND Gates

**Current:**
```
gate_nand/
  nand/            (generic NAND)
gate_nand_8bit/    (8-bit NAND)
```

**Target:**
```
gate_nand/
  gate_nand_2in_8bit/  (2-input, 8-bit) - 1× used
gate_nand/             (keep legacy)
gate_nand_8bit/        (keep legacy)
```

**Action:** The existing 8-bit NAND likely matches the required 2-input, 8-bit specification.

### NOR Gates

**Current:**
```
gate_nor/
  nor/             (generic NOR)
gate_nor_8bit/     (8-bit NOR)
```

**Target:**
```
gate_nor/
  gate_nor_2in_1bit/   (2-input, 1-bit) - 1× used
  gate_nor_2in_8bit/   (2-input, 8-bit) - 1× used
  gate_nor_8in_1bit/   (8-input, 1-bit) - 1× used (zero detection)
gate_nor/              (keep legacy)
gate_nor_8bit/         (keep legacy)
```

**Action:** Review and organize by both input count and bit width.

### XOR Gates

**Current:**
```
gate_xor/          (generic XOR)
gate_xor_8bit/     (8-bit XOR)
gate_xor_ic/       (IC-based XOR)
```

**Target:**
```
gate_xor/
  gate_xor_2in_8bit/   (2-input, 8-bit) - 3× used
gate_xor/              (keep legacy)
gate_xor_8bit/         (keep legacy)
gate_xor_ic/           (keep - IC implementation)
```

**Action:** Organize 8-bit XOR designs into the new subdirectory.

### Multiplexers

**Current:**
```
mux_8bit/          (generic 8-bit MUX)
```

**Target:**
```
mux/
  mux_2to1_8bit/   (2:1 MUX, 1-bit select, 8-bit data) - 2× used
  mux_4to1_8bit/   (4:1 MUX, 2-bit select, 8-bit data) - 3× used
  mux_8to1_8bit/   (8:1 MUX, 3-bit select, 8-bit data) - 1× used
mux_8bit/          (keep legacy)
```

**Action:** Review existing MUX designs and organize by input count (2:1, 4:1, 8:1).

## Migration Steps

1. **Review Existing Designs**
   - Open each existing `.kicad_sch` file
   - Identify the gate/component specifications:
     - Input count (for AND, OR, NAND, NOR)
     - Bit width
     - MUX size (2:1, 4:1, 8:1)

2. **Create Target Directories**
   - Use the `mkdir -p` command to create target directories
   - Example: `mkdir -p gate_and/gate_and_4in/`

3. **Move/Copy Files**
   - **Option A (Recommended):** Copy files to preserve originals
     ```bash
     cp gate_and/*.kicad_* gate_and/gate_and_4in/
     ```
   - **Option B:** Move files if you're certain of their specification
     ```bash
     mv gate_and/*.kicad_* gate_and/gate_and_4in/
     ```

4. **Update Project Files**
   - Update `.kicad_pro` files to reflect new paths
   - Verify all linked files are in correct locations
   - Update any library paths if needed

5. **Document Specifications**
   - Add a README.md in each module directory
   - Document:
     - Input count
     - Bit width
     - Usage count in ALU
     - Design notes

6. **Verify**
   - Open each migrated project in KiCad
   - Verify schematics load correctly
   - Check that PCB layouts are intact
   - Validate component libraries

## Component Inventory Reference

For detailed component counts and specifications, see:
- `docs/build-notes/component_inventory.md`

Key specifications to match:
- **AND:** 2-input (10×), 3-input (1×), 4-input (19×) - all 1-bit
- **OR:** 2-input (7×), 3-input (1×) - all 1-bit
- **NOT:** 1-bit (40×), 8-bit (1×)
- **NOR:** 2-input 1-bit (1×), 2-input 8-bit (1×), 8-input 1-bit (1×)
- **MUX:** 2:1 (2×), 4:1 (3×), 8:1 (1×) - all 8-bit data

---

*Created: 2026-01-08*
