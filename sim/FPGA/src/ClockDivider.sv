/******************************************************************************
 ** Clock Divider / Tick Generator
 ** 
 ** Description:
 **   Generates a single-cycle enable pulse ('Tick') at a lower frequency
 **   derived from the main system clock.
 **   Used to slow down operations for human-visible demonstration.
 **
 *****************************************************************************/

`timescale 1ns / 1ps

module ClockDivider #(
    parameter CLOCK_FREQ = 100_000_000, // 100 MHz
    parameter TARGET_FREQ = 1           // 1 Hz
)(
    input  logic Clock,
    input  logic Reset,
    output logic Tick
);

    // Calculate max count: (ClockFreq / TargetFreq) - 1
    localparam MAX_COUNT = (CLOCK_FREQ / TARGET_FREQ) - 1;
    localparam WIDTH = $clog2(MAX_COUNT);
    
    logic [WIDTH-1:0] counter;

    always_ff @(posedge Clock or posedge Reset) begin
        if (Reset) begin
            counter <= '0;
            Tick <= 1'b0;
        end else begin
            if (counter >= MAX_COUNT) begin
                counter <= '0;
                Tick <= 1'b1;
            end else begin
                counter <= counter + 1'b1;
                Tick <= 1'b0;
            end
        end
    end

endmodule
