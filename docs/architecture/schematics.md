# Schematics and Simulations

This page enumerates the schematic sources and simulation artifacts used to describe the hardware blocks.

## KiCad projects

- `kicad/boards/alu_core/master-alu.kicad_pro` — top-level ALU core board project that ties arithmetic and logic subcircuits together.
- `kicad/boards/add_sub/add_sub.kicad_pro` — add/subtract arithmetic board used by the ALU core.
- `kicad/boards/main_logic/main_logic.kicad_pro` — logic-unit board that implements non-arithmetic operations.
- `kicad/boards/flags/flags.kicad_pro` — status/flags board that captures condition outputs.
- `kicad/boards/main_control/main_control.kicad_pro` — control board for the CPU’s main control signals.

**Open this file to see the ALU core:** `kicad/boards/alu_core/master-alu.kicad_sch`.

## LTSpice simulations

- _None tracked in this repo yet._ (Simulation outputs are expected to land under `spice/runs/` when added.)
