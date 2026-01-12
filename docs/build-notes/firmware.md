# Firmware Build Notes

This project uses two Arduino-compatible controllers:

- **Controller Input** (`firmware/controller-input/`) drives the data bus, opcode lines, and load strobes.
- **Controller Display** (`firmware/controller-display/`) samples the output register and logs results over Serial.

## Pin Mappings

### Controller Input (Arduino #1)

| Signal | Arduino Pin | Description |
| --- | --- | --- |
| DATA0 | D2 | Data bus bit 0 (LSB) |
| DATA1 | D3 | Data bus bit 1 |
| DATA2 | D4 | Data bus bit 2 |
| DATA3 | D5 | Data bus bit 3 |
| DATA4 | D6 | Data bus bit 4 |
| DATA5 | D7 | Data bus bit 5 |
| DATA6 | D8 | Data bus bit 6 |
| DATA7 | D9 | Data bus bit 7 (MSB) |
| OP0 | D10 | Opcode bit 0 (LSB) |
| OP1 | D11 | Opcode bit 1 |
| OP2 | D12 | Opcode bit 2 |
| OP3 | D13 | Opcode bit 3 (MSB) |
| LOAD_A | A0 | Latch A register |
| LOAD_B | A1 | Latch B register |
| LOAD_R | A2 | Latch R register |

### Controller Display (Arduino #2)

| Signal | Arduino Pin | Description |
| --- | --- | --- |
| R0 | D2 | Output register bit 0 (LSB) |
| R1 | D3 | Output register bit 1 |
| R2 | D4 | Output register bit 2 |
| R3 | D5 | Output register bit 3 |
| R4 | D6 | Output register bit 4 |
| R5 | D7 | Output register bit 5 |
| R6 | D8 | Output register bit 6 |
| R7 | D9 | Output register bit 7 (MSB) |
| LOAD_R | A0 | Strobe from output register load |

## Build + Upload (Arduino IDE)

1. Open the Arduino IDE.
2. Use **File → Open** and select:
   - `firmware/controller-input/controller-input.ino`
   - `firmware/controller-display/controller-display.ino`
3. Select the correct board and port.
4. Click **Upload** for each controller.

## Build + Upload (Arduino CLI)

```bash
arduino-cli core install arduino:avr
arduino-cli compile --fqbn arduino:avr:uno firmware/controller-input
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno firmware/controller-input

arduino-cli compile --fqbn arduino:avr:uno firmware/controller-display
arduino-cli upload -p /dev/ttyACM1 --fqbn arduino:avr:uno firmware/controller-display
```

## Sample Serial Sessions

### Controller Input

```
Controller Input Ready.
Commands:
  A <value>   - Load A register with 0-255
  B <value>   - Load B register with 0-255
  OP <value>  - Set opcode (0-15)
  BUS <value> - Drive data bus without pulsing load
  EXEC        - Pulse LOAD_R
  HELP        - Show this help

> A 12
Loaded A = 12
> B 7
Loaded B = 7
> OP 3
Opcode set to 3
> EXEC
LOAD_R pulse issued.
```

### Controller Display

```
Controller Display Ready.
Waiting for LOAD_R pulses...
R = 0x13 (dec 19, bin 00010011)
```
