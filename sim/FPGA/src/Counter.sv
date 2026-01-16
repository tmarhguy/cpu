/******************************************************************************
 ** Generic Binary Counter
 ** 
 ** Description:
 **   N-bit parameterized up-counter with Enable and Reset.
 **
 *****************************************************************************/

`timescale 1ns / 1ps

module Counter #(
    parameter WIDTH = 8,
    parameter MAX_VAL = {WIDTH{1'b1}} // Default to max possible 2^N - 1
)(
    input  logic             Clock,
    input  logic             Reset,
    input  logic             Enable,
    output logic [WIDTH-1:0] Count
);

    always_ff @(posedge Clock or posedge Reset) begin
        if (Reset) begin
            Count <= '0;
        end else if (Enable) begin
            if (Count >= MAX_VAL)
                Count <= '0;
            else
                Count <= Count + 1'b1;
        end
    end

endmodule
