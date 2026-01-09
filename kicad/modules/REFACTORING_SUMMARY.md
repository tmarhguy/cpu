# KiCad Files Refactoring Summary

**Date:** 2026-01-08  
**Purpose:** Renamed all KiCad project files to match their directory names for consistency.

## Refactoring Process

All KiCad files (`.kicad_sch`, `.kicad_pcb`, `.kicad_pro`, `.kicad_prl`) have been renamed to match their parent directory names.

## Files Renamed

### Gates

#### AND Gates
- `gates/gate_and/gate_and_2in_8bit/`
  - `8-bit-and.*` → `gate_and_2in_8bit.*` ✓

#### NAND Gates
- `gates/gate_nand/gate_nand_2in/`
  - `nand.*` → `gate_nand_2in.*` ✓
- `gates/gate_nand/gate_nand_8bit/`
  - `8-bit-nand.*` → `gate_nand_8bit.*` ✓

#### NOR Gates
- `gates/gate_nor/gate_nor_8bit/`
  - `8-bit-nor.*` → `gate_nor_8bit.*` ✓
- `gates/gate_nor/nor/`
  - `nor.*` → Already matches directory name ✓

#### XNOR Gates
- `gates/gate_xnor/gate_xnor_2in/`
  - `xnor.*` → `gate_xnor_2in.*` ✓

#### NOT Gates (Inverters)
- `gates/gate_inv/gate_inv_1bit/`
  - `not.*` → `gate_inv_1bit.*` ✓

#### XOR Gates
- `gates/gate_xor/gate_xor_2in/`
  - `xor.*` → `gate_xor_2in.*` ✓
- `gates/gate_xor/gate_xor_8bit/`
  - `8-bit-xor.*` → `gate_xor_8bit.*` ✓

#### OR Gates
- `gates/gate_or/gate_or_8bit/`
  - `8-bit-or.*` → `gate_or_8bit.*` ✓
- `gates/gate_or/`
  - `or.*` → `gate_or.*` ✓

#### AND Gates (Root)
- `gates/gate_and/`
  - `.model PMOS...` → `gate_and.kicad_sch` ✓

### Already Consistent

The following directories already had files matching directory names:
- `gates/gate_and/gate_and_2in/gate_and_2in.*` ✓
- `adder/adder2/adder2.*` ✓

## Naming Convention

After refactoring, all files follow this pattern:
```
<directory_name>.<extension>
```

Examples:
- Directory: `gate_and_2in/` → Files: `gate_and_2in.kicad_sch`, `gate_and_2in.kicad_pcb`, etc.
- Directory: `mux_4to1_8bit/` → Files: `mux_4to1_8bit.kicad_sch`, `mux_4to1_8bit.kicad_pcb`, etc.

## Reference Updates

The refactoring script attempted to update internal references in:
- `.kicad_pro` files (JSON format)
- `.kicad_sch` files (Sheetfile references)

**Note:** Some reference updates may require manual verification in KiCad if parent schematics reference these modules.

## Verification

To verify all files match their directories:
```bash
find kicad/modules -name "*.kicad_pro" ! -path "*/backup*" | while read f; do
  dir=$(basename "$(dirname "$f")")
  file=$(basename "$f" .kicad_pro)
  [ "$dir" != "$file" ] && echo "MISMATCH: $f"
done
```

## Next Steps

1. Open each project in KiCad to verify it loads correctly
2. Check parent schematics (e.g., `boards/alu_core/`) for broken references
3. Update any hardcoded file paths in documentation or scripts
4. Test that all modules are accessible from the main ALU design

---

*Refactoring script: `tools/rename_kicad_files.py`*
