# KiCad Modules

This directory contains individual circuit modules organized by component type and specifications.

## Directory Structure

The modules are organized to match the component inventory requirements:

### Gate Modules

#### AND Gates
- `gate_and/gate_and_2in/` - 2-input, 1-bit AND gates (10× used in ALU)
- `gate_and/gate_and_3in/` - 3-input, 1-bit AND gates (1× used in ALU)
- `gate_and/gate_and_4in/` - 4-input, 1-bit AND gates (19× used in ALU - most common)
- `gate_and_8bit/` - 8-bit wide AND gates (legacy/alternative)

#### OR Gates
- `gate_or/gate_or_2in/` - 2-input, 1-bit OR gates (7× used in ALU)
- `gate_or/gate_or_3in/` - 3-input, 1-bit OR gates (1× used in ALU)
- `gate_or_8bit/` - 8-bit wide OR gates (legacy/alternative)

#### NOT Gates (Inverters)
- `gate_inv/gate_inv_1bit/` - 1-bit inverters (40× used in ALU)
- `gate_inv/gate_inv_8bit/` - 8-bit wide inverters (1× used in ALU)

#### NAND Gates
- `gate_nand/gate_nand_2in_8bit/` - 2-input, 8-bit NAND (1× used in ALU)
- `gate_nand/` - Legacy NAND gates

#### NOR Gates
- `gate_nor/gate_nor_2in_1bit/` - 2-input, 1-bit NOR (1× used in ALU)
- `gate_nor/gate_nor_2in_8bit/` - 2-input, 8-bit NOR (1× used in ALU)
- `gate_nor/gate_nor_8in_1bit/` - 8-input, 1-bit NOR for zero detection (1× used in ALU)
- `gate_nor_8bit/` - Legacy NOR gates

#### XOR Gates
- `gate_xor/gate_xor_2in_8bit/` - 2-input, 8-bit XOR (3× used in ALU)
- `gate_xor/` - Legacy XOR gates
- `gate_xor_8bit/` - Alternative 8-bit XOR
- `gate_xor_ic/` - XOR implemented as IC (74HC86)

#### XNOR Gates
- `gate_xnor/` - XNOR gate modules

### Multiplexers

#### MUX Modules
- `mux/mux_2to1_8bit/` - 2:1 MUX, 1-bit select, 8-bit data (2× used in ALU)
- `mux/mux_4to1_8bit/` - 4:1 MUX, 2-bit select, 8-bit data (3× used in ALU)
- `mux/mux_8to1_8bit/` - 8:1 MUX, 3-bit select, 8-bit data (1× used in ALU)
- `mux_8bit/` - Legacy multiplexer modules

### Arithmetic Modules

- `adder1/` - Single-bit full adder
- `adder2/` - 2-bit full adder
- `adder8/` - 8-bit full adder

### ALU Core

- `alu_core/` - ALU core module integration

## Usage Notes

1. **Primary Modules:** Use the organized subdirectories (e.g., `gate_and/gate_and_4in/`) for new designs matching the component inventory.

2. **Legacy Modules:** The root-level directories (e.g., `gate_and/`, `gate_or_8bit/`) contain existing designs and are preserved for compatibility.

3. **Component Sizes:** The organization matches the exact component sizes used in the ALU top circuit as documented in `docs/build-notes/component_inventory.md`.

4. **File Naming:** Each module directory should contain:
   - `.kicad_sch` - Schematic file
   - `.kicad_pcb` - PCB layout file
   - `.kicad_pro` - Project file
   - Backup subdirectories
   - Related documentation

## Migration Notes

When organizing existing designs:
- Move 2-input AND gates → `gate_and/gate_and_2in/`
- Move 3-input AND gates → `gate_and/gate_and_3in/`
- Move 4-input AND gates → `gate_and/gate_and_4in/`
- Move 2-input OR gates → `gate_or/gate_or_2in/`
- Move 3-input OR gates → `gate_or/gate_or_3in/`
- Move 1-bit inverters → `gate_inv/gate_inv_1bit/`
- Move 8-bit inverters → `gate_inv/gate_inv_8bit/`
- Move multiplexers by size → `mux/mux_*to1_8bit/`

---

*Last updated: 2026-01-08*
