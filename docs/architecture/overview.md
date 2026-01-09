# System Architecture Overview

## High-Level Block Diagram

```
             A[7:0]   B[7:0]
                |        |
    FUNC[3:0]   |        |
       |        |        |
   +---v---+    |        |
   | Control   +----v---v----+     +-------------+
   |   Unit |   | Arithmetic  |---->|             |
   +-------+   |    Unit     |  0  | 8-bit 2-to-1|
       |       +-------------+     |     MUX     |---> ALU_Result[7:0]
       |             |   |         |             |
       +------------>|   +-------->|      1      |
      (LogicSelect)  |  (ArithMode)  |             |
                     |             +-------------+
                     |                 ^
                     v                 |
               +-------------+         |
               |  Logical    |         |
               |    Unit     |---------+
               +-------------+        (FinalMuxSelect)
                     ^                    |
                     |                    |
                     +--------------------+
```

## Datapath

**Datapath:** `A_reg (8b) → ALU (arith + logic + mux + global invert) → R_reg (8b)`

## Control Signals

* **FUNC[3:0]**: 4-bit opcode (16 operations)
* **INV_OUT**: Global post-mux inversion bit
* **M**: ADD/SUB mode (0=ADD, 1=SUB)
* **LOAD_A, LOAD_B, LOAD_R**: Register load enables

## I/O Architecture

* **Front-end Arduino**: Keypad input → number entry + opcode selection
* **Back-end Arduino**: Display/logging → reads R_reg and displays results

## Clocking

* Manual (latch enables or debounced buttons)
* MCU-generated pulses

## Power

* 5 V single rail
* Common ground
* Per-IC decoupling (100 nF)
* Star ground to ALU

