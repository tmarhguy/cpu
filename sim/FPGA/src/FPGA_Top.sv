/******************************************************************************
 ** FPGA Top Level
 ** 
 ** Description:
 **   Top-level module for the ALU verification project.
 **   Integrates the ALU with a test pattern generator (Counter) driven by
 **   a reduced-speed clock for hardware demonstration.
 **
 *****************************************************************************/

`timescale 1ns / 1ps

module FPGA_Top (
    input  logic clk,       // Main System Clock (e.g. 100MHz)
    input  logic btnC,      // Reset Button (Center)
    output logic [7:0] led  // Example: Display Result on LEDs
);

    // Internal Signals
    logic tick;
    logic [4:0] opcode;
    logic [7:0] result;
    logic zero, carry, neg, flow, equal, less, great;
    
    // Invert reset if button is active low (depends on board)
    // Assuming Active High for now (Basys3 style)
    logic reset;
    assign reset = btnC;

    // 1. Clock Divider: Reduce 100MHz to ~1Hz for visibility
    ClockDivider #(
        .CLOCK_FREQ(100_000_000),
        .TARGET_FREQ(1) 
    ) clk_div (
        .Clock(clk),
        .Reset(reset),
        .Tick(tick)
    );

    // 2. Operation Counter: Cycle through all ALU opcodes (0-31)
    Counter #(
        .WIDTH(5),
        .MAX_VAL(5'd31)
    ) op_counter (
        .Clock(clk),
        .Reset(reset),
        .Enable(tick), // Only count on tick
        .Count(opcode)
    );

    // 3. ALU Instance
    ALU #(
        .WIDTH(8)
    ) alu_inst (
        .A(8'd42),      // Fixed Input A for demo
        .B(8'd23),      // Fixed Input B for demo
        .Opcode(opcode),
        .Result(result),
        .CarryOut(carry),
        .Zero(zero),
        .Negative(neg),
        .Overflow(flow),
        .Equal(equal),
        .Less(less),
        .Great(great)
    );

    // 4. Output Mapping
    // Map ALU Result to LEDs
    assign led = result;
    
endmodule
