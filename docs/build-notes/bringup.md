# Bring-Up Checklist

Use this checklist during initial hardware bring-up to validate power and logic stages in a controlled order.

## Hardware Bring-Up Steps

1. **Power rail verification and current draw**
   - Verify each rail is at its nominal voltage with no unexpected sag.
   - Measure idle current draw and compare against expected budget.
   - Confirm regulator temperature remains within safe limits.

2. **Continuity checks and decoupling placement**
   - Perform continuity checks for shorts between rails and ground.
   - Verify continuity for critical nets (clock, reset, and data buses).
   - Inspect decoupling capacitors for correct placement and polarity.

3. **Stage-by-stage validation: registers, ALU, output register**
   - Validate register file load/enable behavior.
   - Exercise ALU operations and observe result flags.
   - Confirm output register latching and external visibility.

## Minimal Test Patterns

Use a small, repeatable set of patterns to validate each stage:

- **Registers**
  - Write 0x00, 0xFF, 0xAA, 0x55 and read back from each register.
  - Verify reset clears all registers to 0x00.

- **ALU**
  - ADD: 0x01 + 0x01 → 0x02 (no carry)
  - ADD: 0xFF + 0x01 → 0x00 (carry set)
  - AND: 0xAA & 0x55 → 0x00
  - XOR: 0xAA ^ 0x55 → 0xFF

- **Output Register**
  - Latch 0x00, 0xFF, 0xAA, 0x55 and verify external pins/LEDs.
  - Confirm output retains value when input bus changes.
