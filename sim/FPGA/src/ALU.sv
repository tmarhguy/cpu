/******************************************************************************
 ** SystemVerilog ALU (Arithmetic Logic Unit)
 ** 
 ** Description:
 **   A high-performance, parameterizable Arithmetic Logic Unit utilizing
 **   SystemVerilog behavioral modeling. This module replaces the auto-generated
 **   netlist with clean, synthesizable RTL.
 **
 ** Operations:
 **   0:  ADD   (A + B)
 **   1:  SUB   (A - B)
 **   2:  INC   (A + 1)
 **   3:  DEC   (A - 1)
 **   4:  LSL   (A << 1)
 **   5:  LSR   (A >> 1)
 **   6:  ASR   (A >>> 1)
 **   7:  REV   (Reverse A)
 **   8:  NAND  ~(A & B)
 **   9:  NOR   ~(A | B)
 **   10: XOR   (A ^ B)
 **   11: XNOR  ~(A ^ B)
 **   12: PASS_A (A)
 **   13: AND   (A & B)
 **   14: OR    (A | B)
 **   15: PASS_B (B)
 **   16: CMP   (Compare A, B - Updates flags only, result is 0 or diff)
 **   17: NOT_A (~A)
 **   18: NOT_B (~B)
 **
 ** Flags:
 **   - Zero (Z): Result == 0
 **   - Carry (C): Arithmetic carry/borrow or shift bit out
 **   - Negative (N): MSB of result is 1
 **   - Comparison (Equal, Less, Great): Based on unsigned comparison
 **
 *****************************************************************************/

`timescale 1ns / 1ps

module ALU #(
    parameter WIDTH = 8
)(
    input  logic [WIDTH-1:0] A,
    input  logic [WIDTH-1:0] B,
    input  logic [4:0]       Opcode,
    
    output logic [WIDTH-1:0] Result,
    output logic             CarryOut,
    output logic             Zero,
    output logic             Negative,
    output logic             Overflow,  // Not in original but good practice
    output logic             Equal,
    output logic             Great,
    output logic             Less
);

    // Internal results with extra bit for carry capture
    logic [WIDTH:0] temp_result;
    
    always @* begin
        // Default assignments
        temp_result = '0;
        CarryOut = 0;
        Overflow = 0; // Placeholder
        
        case (Opcode)
            // Arithmetic
            5'd0: begin // ADD
                temp_result = {1'b0, A} + {1'b0, B};
                CarryOut = temp_result[WIDTH]; // Carry from addition
            end
            5'd1: begin // SUB
                /* 
                   For subtraction A - B, we use 2's complement: A + (~B) + 1.
                   We need to capture the 9th bit for Carry/Borrow info.
                */
                 temp_result = {1'b0, A} + {1'b0, ~B} + 9'd1;
                 CarryOut = temp_result[WIDTH]; 
            end
            5'd2: begin // INC
                temp_result = {1'b0, A} + 1'b1;
                CarryOut = temp_result[WIDTH]; 
            end
            5'd3: begin // DEC
                 temp_result = {1'b0, A} + {1'b0, 8'hFF}; // A + (-1)
                 CarryOut = temp_result[WIDTH];
            end
            
            // Shift
            5'd4: begin // LSL
                temp_result[WIDTH-1:0] = A << 1;
                CarryOut = A[WIDTH-1]; // MSB shifts out to carry
                temp_result[WIDTH] = CarryOut; // Consistency
            end
            5'd5: begin // LSR
                temp_result[WIDTH-1:0] = A >> 1;
                CarryOut = A[0]; // LSB shifts out to carry
            end
            5'd6: begin // ASR
                temp_result[WIDTH-1:0] = $signed(A) >>> 1;
                CarryOut = A[0]; // LSB shifts out
            end
            
            // Logic
            5'd13: temp_result[WIDTH-1:0] = A & B;      // AND
            5'd14: temp_result[WIDTH-1:0] = A | B;      // OR
            5'd10: temp_result[WIDTH-1:0] = A ^ B;      // XOR
            5'd8:  temp_result[WIDTH-1:0] = ~(A & B);   // NAND
            5'd9:  temp_result[WIDTH-1:0] = ~(A | B);   // NOR
            5'd11: temp_result[WIDTH-1:0] = ~(A ^ B);   // XNOR
            
            // Special
            5'd17: temp_result[WIDTH-1:0] = ~A;         // NOT A
            5'd18: temp_result[WIDTH-1:0] = ~B;         // NOT B
            5'd12: temp_result[WIDTH-1:0] = A;          // PASS A
            5'd15: temp_result[WIDTH-1:0] = B;          // PASS B
            5'd7:  begin                                // REV
                integer i;
                for(i=0; i<WIDTH; i++) temp_result[i] = A[WIDTH-1-i];
            end
            
            5'd16: begin // CMP
               // Subtraction for comparison
               temp_result = {1'b0, A} + {1'b0, ~B} + 9'd1;
               CarryOut = temp_result[WIDTH];
            end
            
            default: temp_result = '0; 
        endcase
    end
    
    // Output assignment
    assign Result = temp_result[WIDTH-1:0];
    
    // Flag Generation
    assign Zero = (Result == '0);
    assign Negative = Result[WIDTH-1];
    
    // Comparison Flags (Unsigned)
    assign Equal = (A == B);
    assign Less  = (A < B);
    assign Great = (A > B);

endmodule
