# Component Inventory to KiCad Directory Mapping

This document maps the component inventory from the Logisim ALU circuit to the KiCad module directory structure.

## Mapping Table

| Component Inventory | Count | KiCad Module Path | Status |
|---------------------|-------|-------------------|--------|
| **AND Gates** |
| 2-input, 1-bit AND | 10 | `gate_and/gate_and_2in/` | ✅ Directory created |
| 3-input, 1-bit AND | 1 | `gate_and/gate_and_3in/` | ✅ Directory created |
| 4-input, 1-bit AND | 19 | `gate_and/gate_and_4in/` | ✅ Directory created |
| **OR Gates** |
| 2-input, 1-bit OR | 7 | `gate_or/gate_or_2in/` | ✅ Directory created |
| 3-input, 1-bit OR | 1 | `gate_or/gate_or_3in/` | ✅ Directory created |
| **NOT Gates** |
| 1-bit NOT | 40 | `gate_inv/gate_inv_1bit/` | ✅ Directory created |
| 8-bit NOT | 1 | `gate_inv/gate_inv_8bit/` | ✅ Directory created |
| **NAND Gates** |
| 2-input, 8-bit NAND | 1 | `gate_nand/gate_nand_2in_8bit/` | ✅ Directory created |
| **NOR Gates** |
| 2-input, 1-bit NOR | 1 | `gate_nor/gate_nor_2in_1bit/` | ✅ Directory created |
| 2-input, 8-bit NOR | 1 | `gate_nor/gate_nor_2in_8bit/` | ✅ Directory created |
| 8-input, 1-bit NOR | 1 | `gate_nor/gate_nor_8in_1bit/` | ✅ Directory created |
| **XOR Gates** |
| 2-input, 8-bit XOR | 3 | `gate_xor/gate_xor_2in_8bit/` | ✅ Directory created |
| **Multiplexers** |
| 2:1 MUX (1-bit select, 8-bit data) | 2 | `mux/mux_2to1_8bit/` | ✅ Directory created |
| 4:1 MUX (2-bit select, 8-bit data) | 3 | `mux/mux_4to1_8bit/` | ✅ Directory created |
| 8:1 MUX (3-bit select, 8-bit data) | 1 | `mux/mux_8to1_8bit/` | ✅ Directory created |
| **Arithmetic** |
| 1-bit Adder | 1 | `adder1/` | ✅ Existing |
| 8-bit Adder | N/A | `adder8/` | ✅ Existing |

## Legacy Directories (Preserved)

These directories contain existing designs and are preserved for compatibility:

- `gate_and/` - Original AND gate designs
- `gate_and_8bit/` - 8-bit AND alternatives
- `gate_or/` - Original OR gate designs
- `gate_or_8bit/` - 8-bit OR alternatives
- `gate_inv/not/` - Original NOT/inverter designs
- `gate_nand/nand/` - Original NAND designs
- `gate_nand_8bit/` - 8-bit NAND alternatives
- `gate_nor/nor/` - Original NOR designs
- `gate_nor_8bit/` - 8-bit NOR alternatives
- `gate_xor/` - Original XOR designs
- `gate_xor_8bit/` - 8-bit XOR alternatives
- `gate_xor_ic/` - IC-based XOR (74HC86)
- `gate_xnor/` - XNOR gate designs
- `mux_8bit/` - Original multiplexer designs

## Next Steps

1. **Review Existing Designs**
   - Open each existing KiCad project
   - Identify the exact specifications (input count, bit width)
   - Move or copy to appropriate new directory

2. **Create New Designs**
   - For components matching inventory specs, create in new organized directories
   - Follow naming convention: `gate_[type]/gate_[type]_[inputs]in_[width]bit/`

3. **Document Each Module**
   - Add README.md in each module directory
   - Document specifications, usage count, design notes

4. **Update References**
   - Update any schematics that reference these modules
   - Update ALU core design to use organized module paths

## Usage Priority

When selecting modules for new designs:

1. **Primary:** Use organized subdirectories matching component inventory exactly
   - Example: `gate_and/gate_and_4in/` for 4-input AND gates

2. **Secondary:** Use legacy directories if organized version doesn't exist yet
   - Example: `gate_and/` temporarily until migration complete

3. **Alternative:** Use alternative implementations when needed
   - Example: `gate_xor_ic/` for IC-based XOR implementation

---

*Last updated: 2026-01-08*
