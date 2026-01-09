# 4:1 Multiplexer (8-bit data)

**Most Common MUX in ALU Design**

## Specifications

- **Type:** 4:1 Multiplexer
- **Select Bits:** 2-bit (selects 1 of 4 inputs)
- **Data Width:** 8-bit
- **Usage Count:** 3× (most frequently used MUX in ALU)
- **Library:** Plexers (lib="2")

## Design Notes

The 4:1 MUX is used for routing multiple 8-bit data paths in the ALU. It requires:
- 4× 8-bit input buses
- 1× 2-bit select signal
- 1× 8-bit output bus

Common uses:
- Operation selection
- Data path routing
- Result multiplexing

## Files

- `*.kicad_sch` - Schematic file
- `*.kicad_pcb` - PCB layout file
- `*.kicad_pro` - KiCad project file

## Related Modules

- `../mux_2to1_8bit/` - 2:1 MUX (2× used)
- `../mux_8to1_8bit/` - 8:1 MUX (1× used)

---

*See `docs/build-notes/component_inventory.md` for complete specifications*
