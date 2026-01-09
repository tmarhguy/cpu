# Control Unit Architecture

This document describes the control unit design and implementation.

## Control Signals

- FUNC[3:0] - 4-bit operation selector
- M - ADD/SUB mode
- INV_OUT - Global inversion enable
- LOAD_A, LOAD_B, LOAD_R - Register load enables

## Decoder Logic

The control unit decodes FUNC[3:0] into internal control signals for ALU operation.

