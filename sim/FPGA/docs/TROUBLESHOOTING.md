# Troubleshooting Guide

**Common Issues and Solutions for FPGA ALU Implementation**

---

## Table of Contents

- [Simulation Issues](#simulation-issues)
- [Synthesis Issues](#synthesis-issues)
- [Timing Issues](#timing-issues)
- [Functional Issues](#functional-issues)
- [Integration Issues](#integration-issues)

---

## Simulation Issues

### Issue: Unknown (X) Values in Simulation

**Symptoms**:
- Signals show 'X' in waveform
- Testbench reports unknown values

**Causes**:
1. Uninitialized inputs
2. Multiple drivers on same signal
3. Timing violations

**Solutions**:

```verilog
// Solution 1: Initialize all inputs
initial begin
    A_IN = 8'h00;
    B_IN = 8'h00;
    GND = 1'b0;
    logisimClockTree0 = 5'b00000;
    #100;  // Wait for initialization
end

// Solution 2: Check for multiple assignments
// Ensure each signal has only one driver

// Solution 3: Add delays if needed
#10;  // Wait for combinational propagation
```

### Issue: Testbench Hangs

**Symptoms**:
- Simulation runs indefinitely
- No output generated

**Causes**:
1. Missing `$finish` statement
2. Infinite loops
3. Clock not toggling

**Solutions**:

```verilog
// Add explicit finish
initial begin
    // ... tests ...
    #1000;
    $finish;
end

// Check for infinite loops
// Ensure all loops have exit conditions
```

### Issue: Wrong Results in Simulation

**Symptoms**:
- Operations produce incorrect results
- Flags are wrong

**Causes**:
1. Opcode not set correctly
2. Operands not stable
3. Timing issues

**Solutions**:

```verilog
// Verify opcode setting
// Check that logisimClockTree0[4:0] matches desired opcode

// Ensure operands are stable
A_IN = 8'd42;
B_IN = 8'd23;
#10;  // Wait before checking result

// Check timing
// Add sufficient delay for combinational path
```

---

## Synthesis Issues

### Issue: Synthesis Fails with "Unsupported Construct"

**Symptoms**:
- Synthesis error about unsupported Verilog
- Tool doesn't recognize certain constructs

**Causes**:
1. SystemVerilog features in Verilog file
2. Incompatible syntax
3. Missing module definitions

**Solutions**:

```verilog
// Check file extensions
// Use .v for Verilog, .sv for SystemVerilog

// Ensure all modules are defined
// Check that all instantiated modules exist

// Use synthesis-compatible constructs
// Avoid unsupported SystemVerilog features
```

### Issue: High Resource Usage

**Symptoms**:
- LUT usage > 80%
- FFs usage > 80%
- Synthesis warnings

**Causes**:
1. Inefficient logic
2. Unnecessary registers
3. Large multiplexers

**Solutions**:

1. **Optimize Multiplexers**:
   ```verilog
   // Use case statements instead of large mux trees
   case (sel)
       2'b00: out = in0;
       2'b01: out = in1;
       // ...
   endcase
   ```

2. **Share Common Logic**:
   ```verilog
   // Share adder for multiple operations
   wire [7:0] sum = A + B;
   wire [7:0] diff = A - B;
   ```

3. **Use DSP Slices** (if applicable):
   ```verilog
   // Let synthesis infer DSP for multipliers
   wire [15:0] product = A * B;
   ```

### Issue: Constraint Violations

**Symptoms**:
- Timing violations
- Setup/hold violations
- Clock domain issues

**Solutions**:

```tcl
# Add timing constraints
create_clock -period 10.0 -name clk [get_ports clk]

# Set input/output delays
set_input_delay -clock clk 2.0 [get_ports A_IN*]
set_output_delay -clock clk 2.0 [get_ports OVERALL*]

# Add false paths if needed
set_false_path -from [get_ports async_signal]
```

---

## Timing Issues

### Issue: Critical Path Too Long

**Symptoms**:
- Negative slack in timing report
- Cannot meet clock frequency

**Causes**:
1. Long combinational paths
2. Ripple-carry adder delay
3. Large multiplexers

**Solutions**:

1. **Add Pipeline Stages**:
   ```verilog
   // Break into stages
   always @(posedge clk) begin
       stage1_a <= A;
       stage1_b <= B;
   end
   
   // ALU computation
   // ...
   
   always @(posedge clk) begin
       result <= alu_out;
   end
   ```

2. **Use Carry-Lookahead Adder**:
   - Reduces critical path
   - Increases LUT usage

3. **Register Intermediate Results**:
   ```verilog
   reg [7:0] temp_result;
   always @(posedge clk) begin
       temp_result <= intermediate_calc;
   end
   ```

### Issue: Setup/Hold Violations

**Symptoms**:
- Timing report shows violations
- Signals not stable at clock edge

**Solutions**:

```tcl
# Increase clock period
create_clock -period 15.0 -name clk [get_ports clk]

# Adjust input delays
set_input_delay -clock clk 1.0 [get_ports A_IN*]

# Add clock uncertainty
set_clock_uncertainty 0.5 [get_clocks clk]
```

---

## Functional Issues

### Issue: Wrong Operation Selected

**Symptoms**:
- ALU performs wrong operation
- Opcode doesn't match operation

**Causes**:
1. Opcode mapping incorrect
2. Control signals wrong
3. Multiplexer selection error

**Solutions**:

```verilog
// Verify opcode mapping
// Check that logisimClockTree0[4:0] matches opcode table

// Debug control signals
$display("Opcode: %d, Operation: %s", opcode, op_name);

// Check multiplexer selection
// Verify sel signals are correct
```

### Issue: Flags Not Set Correctly

**Symptoms**:
- Carry flag wrong
- Zero flag incorrect
- Comparison flags wrong

**Solutions**:

```verilog
// Verify flag logic
// Check zero detection: NOR of all result bits
// Check carry: From adder carry-out
// Check comparison: From subtraction result

// Debug flags
$display("Result: %h, Zero: %b, Carry: %b", result, zero, carry);
```

### Issue: Overflow Not Detected

**Symptoms**:
- Arithmetic overflow not caught
- Results wrap incorrectly

**Solutions**:

```verilog
// Add overflow detection
wire overflow = (A[7] == B[7]) && (result[7] != A[7]);

// Check for signed overflow
wire signed_overflow = 
    (A[7] && B[7] && !result[7]) ||  // Negative + Negative = Positive
    (!A[7] && !B[7] && result[7]);    // Positive + Positive = Negative
```

---

## Integration Issues

### Issue: ALU Not Responding

**Symptoms**:
- No output from ALU
- Signals stuck

**Causes**:
1. Clock not connected
2. Reset not released
3. Enable signal not set

**Solutions**:

```verilog
// Check clock
always @(posedge clk) begin
    // ALU should respond
end

// Check reset
if (rst) begin
    // Initialize
end else begin
    // Normal operation
end

// Check enable
if (enable) begin
    // ALU active
end
```

### Issue: Port Mismatch

**Symptoms**:
- Synthesis error about port mismatch
- Simulation error about connections

**Solutions**:

```verilog
// Verify port names match
main alu (
    .A_IN(operand_a),      // Check: A_IN vs A
    .B_IN(operand_b),      // Check: B_IN vs B
    .OVERALL(result)       // Check: OVERALL vs OUT
);

// Check port widths
// Ensure [7:0] matches [7:0]
```

### Issue: Multiple Clock Domains

**Symptoms**:
- Timing violations
- Metastability issues

**Solutions**:

```verilog
// Use synchronizers for cross-domain signals
reg [7:0] sync_a, sync_a_meta;
always @(posedge clk_b) begin
    sync_a_meta <= A_from_clk_a;
    sync_a <= sync_a_meta;
end

// Or use FIFOs for data
// Or use handshaking protocols
```

---

## Debugging Tips

### 1. Use Waveform Viewer

- Add all relevant signals
- Use cursors to measure timing
- Check signal transitions

### 2. Add Debug Prints

```verilog
$display("Time: %t, A=%h, B=%h, Result=%h", 
         $time, A_IN, B_IN, OVERALL);
```

### 3. Use Assertions

```verilog
assert (OVERALL == expected) 
    else $error("Result mismatch: Expected %h, Got %h", 
                 expected, OVERALL);
```

### 4. Check Synthesis Reports

- Review resource usage
- Check timing reports
- Look for warnings

### 5. Use ILA (Integrated Logic Analyzer)

- Add debug cores
- Capture real-time signals
- Trigger on conditions

---

## Common Error Messages

### "Port width mismatch"

**Solution**: Check that port widths match in instantiation

### "Undefined module"

**Solution**: Ensure all modules are included in project

### "Multiple drivers"

**Solution**: Check for multiple assignments to same signal

### "Latch inferred"

**Solution**: Ensure all branches of if/case assign values

### "Timing violation"

**Solution**: Add pipeline stages or increase clock period

---

## Getting Help

1. **Check Documentation**:
   - [Module Documentation](MODULES.md)
   - [Testing Guide](TESTING.md)
   - [Performance Analysis](PERFORMANCE.md)

2. **Review Testbench**:
   - See `testbench/alu_tb.v` for examples
   - Use as template for your tests

3. **Check Synthesis Reports**:
   - Review warnings and errors
   - Check resource usage

4. **Simulate First**:
   - Always simulate before synthesis
   - Catch functional errors early

---

## Prevention

### Best Practices

1. ✅ **Always simulate before synthesis**
2. ✅ **Use consistent naming conventions**
3. ✅ **Add timing constraints early**
4. ✅ **Test edge cases**
5. ✅ **Document assumptions**
6. ✅ **Use version control**
7. ✅ **Review synthesis warnings**

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024 | Initial troubleshooting guide |
