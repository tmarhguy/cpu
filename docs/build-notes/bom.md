# Bill of Materials (BOM)

## Core Components

### Registers
* 3× 74HC373/574 (A, B, R registers)
  - Alternative: 74HC573/273 (edge-triggered)

### Multiplexers
* 2× 74HC157 (8-bit 2:1 mux for ALU output selection)

### Logic
* 1× 74HC14 (Schmitt trigger for debouncing, optional)

### ALU Core
* Discrete transistors for ALU (NMOS/PMOS pairs)
  - Quantity depends on implementation (see transistor cost analysis)

### Power & Decoupling
* 100 nF ceramic capacitors (one per IC)
* 10 µF bulk capacitors (one per board)
* 5V power supply

### I/O Components
* LEDs + 1k-2.2kΩ resistors (for R display, optional A/B too)
* Headers/ribbon cables for bus connections
* Test points for debugging

### Microcontrollers
* 2× Arduino (or compatible)
  - Arduino #1: Front-end (keypad/UI)
  - Arduino #2: Back-end (display/logging)

### Input/Output
* Keypad or buttons for input
* OLED display (I²C) or Serial for output
* Optional: Rotary encoder

## PCB Components
* SMD passives: 0805 size
* SOT-23 FETs (if using discrete transistors)
* Standoffs for mounting
* Edge connectors or ribbon cables

## Notes
* All logic uses 5V HC family (74HCxx)
* Common ground throughout
* Fan-out considerations: may need 220-470Ω series resistors to MCU pins

