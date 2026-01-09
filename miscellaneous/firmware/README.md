<div align="center">

# Firmware

**Microcontroller firmware for the ALU system control and interface**

</div>

---

<div align="center">

## Control Unit Interface

</div>

<table>
<tr>
<td width="50%">

**Control Signal Processing**
- **4-bit control signal** (CT. Sig)
- Allows $2^{4} = 16$ possible operations
- Flexible operation encoding

**Control Unit Outputs**
- 1-bit signal to adder (as $C_{in}$)
- Used to complete 2's complement for subtraction

</td>
<td width="50%">

**8-Bit XOR Gate Control**
- **ADD:** `00000000` ($B \oplus 0 = B$)
- **SUB:** `11111111` ($B \oplus 1 = \overline{B}$)
- Direct control signal mapping

**Control Line Logic**
- 1 if Sub, else 0 (for ADD/SUB operations)
- Setting SUB to 1 supplies adder with $\overline{B}$ and adds 1 (as $C_{in}$) to complete 2's complement

</td>
</tr>
</table>

---

<div align="center">

## Directory Structure

</div>

<table>
<tr>
<td width="50%">

### `controller_input/`
Front-end Arduino (Arduino #1)

**Functionality**
- Handles keypad/button input
- Converts decimal to binary
- Generates control signals:
  - A_D, B_D
  - FUNC, M
  - INV_OUT
  - LOAD_A, LOAD_B, LOAD_R

**Libraries**
- Keypad.h

</td>
<td width="50%">

### `controller_display/`
Back-end Arduino (Arduino #2)

**Functionality**
- Reads ALU outputs (A_Q, B_Q, R_Q, flags)
- Displays results on OLED/Serial
- Logs test vectors

**Libraries**
- LiquidCrystal.h (or OLED library)

</td>
</tr>
</table>

---

<div align="center">

## Communication

</div>

<table>
<tr>
<td width="33%">

**Front-end → ALU**
- Direct digital I/O
- 5V logic levels
- Real-time control

</td>
<td width="33%">

**ALU → Back-end**
- Direct digital I/O
- 5V logic levels
- Result monitoring

</td>
<td width="33%">

**Arduino ↔ Arduino**
- Optional serial communication
- Synchronization protocol
- Status updates

</td>
</tr>
</table>

---

<div align="center">

## Development Notes

</div>

<table>
<tr>
<td width="50%">

**Development Environment**
- Arduino IDE
- PlatformIO
- Version control integration

**Hardware Compatibility**
- 5V logic compatibility (HC family)
- Direct I/O interfacing
- Signal level matching

</td>
<td width="50%">

**Implementation Requirements**
- Debouncing for manual controls
- Test vector runner for automated validation
- Error handling and logging
- Real-time monitoring

</td>
</tr>
</table>
