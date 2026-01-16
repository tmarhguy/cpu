# Integration Guide

**How to Integrate the 8-Bit ALU into Your FPGA Design**

---

## Overview

This guide explains how to instantiate and use the ALU module in your own FPGA designs, including example integrations and best practices.

---

## Basic Instantiation

### Minimal Example

```verilog
module my_cpu(
    input  wire        clk,
    input  wire        rst,
    input  wire [7:0]  operand_a,
    input  wire [7:0]  operand_b,
    input  wire [4:0]  opcode,
    output wire [7:0]  alu_result,
    output wire        carry_flag,
    output wire        zero_flag
);

    // Instantiate ALU
    main alu_inst (
        .A_IN(operand_a),
        .B_IN(operand_b),
        .GND(1'b0),
        .logisimClockTree0(5'b00000),  // Note: Replace with opcode input
        .OVERALL(alu_result),
        .C_OUT(carry_flag),
        .EQUAL_FL(zero_flag),
        // ... other outputs ...
    );

endmodule
```

---

## Integration Patterns

### Pattern 1: Standalone ALU with External Opcode

```verilog
module alu_wrapper(
    input  wire        clk,
    input  wire [7:0]  A,
    input  wire [7:0]  B,
    input  wire [4:0]  opcode,
    output reg  [7:0]  result,
    output reg         carry,
    output reg         zero
);

    // Internal signals
    wire [7:0] alu_out;
    wire       alu_carry;
    wire       alu_zero;

    // Instantiate ALU
    main alu (
        .A_IN(A),
        .B_IN(B),
        .GND(1'b0),
        .logisimClockTree0({1'b0, opcode}),  // Map opcode
        .OVERALL(alu_out),
        .C_OUT(alu_carry),
        .EQUAL_FL(alu_zero),
        // ... connect other outputs as needed ...
    );

    // Register outputs (optional, for timing)
    always @(posedge clk) begin
        result <= alu_out;
        carry  <= alu_carry;
        zero   <= alu_zero;
    end

endmodule
```

### Pattern 2: CPU Integration

```verilog
module simple_cpu(
    input  wire        clk,
    input  wire        rst,
    input  wire [7:0]  instruction,
    output wire [7:0]  result
);

    // Registers
    reg [7:0] reg_a, reg_b;
    reg [4:0] opcode;
    
    // ALU signals
    wire [7:0] alu_result;
    wire       alu_carry;
    wire       alu_zero;
    
    // Instruction decode (simplified)
    always @(posedge clk) begin
        if (rst) begin
            reg_a <= 8'h00;
            reg_b <= 8'h00;
            opcode <= 5'h00;
        end else begin
            opcode <= instruction[4:0];
            // ... load registers based on instruction ...
        end
    end
    
    // ALU instantiation
    main alu_unit (
        .A_IN(reg_a),
        .B_IN(reg_b),
        .GND(1'b0),
        .logisimClockTree0({1'b0, opcode}),
        .OVERALL(alu_result),
        .C_OUT(alu_carry),
        .EQUAL_FL(alu_zero),
        // ... other flags ...
    );
    
    assign result = alu_result;

endmodule
```

### Pattern 3: Pipelined Integration

```verilog
module pipelined_alu(
    input  wire        clk,
    input  wire [7:0]  A,
    input  wire [7:0]  B,
    input  wire [4:0]  opcode,
    output reg  [7:0]  result,
    output reg         flags
);

    // Pipeline stages
    reg [7:0] stage1_a, stage1_b;
    reg [4:0] stage1_opcode;
    wire [7:0] stage1_result;
    wire       stage1_carry;
    
    // Stage 1: Register inputs
    always @(posedge clk) begin
        stage1_a <= A;
        stage1_b <= B;
        stage1_opcode <= opcode;
    end
    
    // Stage 2: ALU computation
    main alu (
        .A_IN(stage1_a),
        .B_IN(stage1_b),
        .GND(1'b0),
        .logisimClockTree0({1'b0, stage1_opcode}),
        .OVERALL(stage1_result),
        .C_OUT(stage1_carry),
        // ...
    );
    
    // Stage 3: Register outputs
    always @(posedge clk) begin
        result <= stage1_result;
        flags <= {stage1_carry, /* other flags */};
    end

endmodule
```

---

## Clock Domain Considerations

### Current Implementation

The ALU is **combinational** (no internal clock). However, the `logisimClockTree0` input is used for opcode selection in the current auto-generated code.

### Recommended Modification

For production use, modify `main.v` to accept opcode directly:

```verilog
// In main.v, replace:
input [4:0] logisimClockTree0;

// With:
input [4:0] opcode;
```

Then use opcode directly in control logic.

---

## Timing Considerations

### Combinational Path

The ALU is fully combinational, so:
- **Latency**: 0 cycles (combinational)
- **Throughput**: 1 operation per cycle (if registered)
- **Critical Path**: Through 8-bit ripple-carry adder

### Adding Registers

For better timing, register inputs and outputs:

```verilog
always @(posedge clk) begin
    if (enable) begin
        reg_a <= A;
        reg_b <= B;
        reg_opcode <= opcode;
    end
end

// ALU (combinational)
main alu (/* ... */);

always @(posedge clk) begin
    if (enable) begin
        result <= alu_result;
        flags <= alu_flags;
    end
end
```

---

## Constraint File Integration

### Adding to Your Constraints

```tcl
# Add ALU clock constraint
create_clock -period 10.0 -name clk [get_ports clk]

# Set input/output delays
set_input_delay -clock clk 2.0 [get_ports A_IN*]
set_input_delay -clock clk 2.0 [get_ports B_IN*]
set_output_delay -clock clk 2.0 [get_ports OVERALL*]
```

---

## Resource Sharing

### Multiple ALU Instances

If you need multiple ALUs, consider:

1. **Time-multiplexing**: Single ALU, multiple cycles
2. **Resource sharing**: Share common logic
3. **Separate instances**: If throughput is critical

---

## Debugging Integration

### Adding Debug Signals

```verilog
// Add debug outputs
wire [7:0] debug_sum;
wire [7:0] debug_logic;
wire       debug_carry;

main alu (
    // ... normal connections ...
    .SUM(debug_sum),
    .LOGIC_OUT(debug_logic),
    .C_OUT(debug_carry),
    // ...
);

// Connect to ILA (Integrated Logic Analyzer) or ChipScope
```

---

## Best Practices

### 1. Register Inputs/Outputs
- Register ALU inputs for timing
- Register ALU outputs for stability

### 2. Clock Gating
- Gate clock when ALU is idle
- Reduces power consumption

### 3. Operand Isolation
- Gate unused operands
- Prevents unnecessary switching

### 4. Error Handling
- Check for invalid opcodes
- Handle overflow conditions

### 5. Testing
- Use provided testbench as template
- Add integration-specific tests

---

## Example: Complete CPU Integration

```verilog
module cpu_with_alu(
    input  wire        clk,
    input  wire        rst,
    input  wire [15:0] instruction,
    output wire [7:0]  result
);

    // Instruction fields
    wire [4:0] opcode = instruction[4:0];
    wire [7:0] imm    = instruction[15:8];
    
    // Registers
    reg [7:0] reg_file [0:7];
    reg [7:0] pc;
    
    // ALU signals
    wire [7:0] alu_a = reg_file[instruction[7:5]];  // Source 1
    wire [7:0] alu_b = reg_file[instruction[10:8]]; // Source 2
    wire [7:0] alu_result;
    wire       alu_carry, alu_zero;
    
    // ALU instantiation
    main alu (
        .A_IN(alu_a),
        .B_IN(alu_b),
        .GND(1'b0),
        .logisimClockTree0({1'b0, opcode}),
        .OVERALL(alu_result),
        .C_OUT(alu_carry),
        .EQUAL_FL(alu_zero)
    );
    
    // Write back
    always @(posedge clk) begin
        if (rst) begin
            pc <= 8'h00;
        end else begin
            if (instruction[15]) begin  // ALU operation
                reg_file[instruction[13:11]] <= alu_result;
            end
            pc <= pc + 1;
        end
    end
    
    assign result = alu_result;

endmodule
```

---

## Migration from Discrete Implementation

### Key Differences

| Aspect | Discrete | FPGA |
|--------|----------|------|
| **Interface** | Direct I/O | Verilog ports |
| **Control** | External switches | Opcode input |
| **Timing** | Propagation delay | Combinational |
| **Power** | ~500mA @ 5V | ~TBD mW |

### Migration Steps

1. **Replace Physical I/O** with Verilog ports
2. **Replace Switches** with opcode register
3. **Add Clocking** if needed for registers
4. **Update Constraints** for FPGA pins

---

## References

- [Module Documentation](MODULES.md) - Detailed module reference
- [Testing Guide](TESTING.md) - Testbench usage
- [Performance Analysis](PERFORMANCE.md) - Resource and timing

---

## Support

For questions or issues, refer to:
- Main project README: `../../README.md`
- ALU Specification: `../../spec/alu-spec.md`
