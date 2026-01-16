/******************************************************************************
 ** Test Vectors: Pre-defined test cases for ALU verification
 **
 ** This file contains structured test vectors for all 19 ALU operations.
 ** These can be used in testbenches or for automated verification.
 **
 *****************************************************************************/

`ifndef TEST_VECTORS_V
`define TEST_VECTORS_V

// Test Vector Structure
typedef struct {
    logic [7:0] A;
    logic [7:0] B;
    logic [4:0] opcode;
    logic [7:0] expected_result;
    logic       expected_carry;
    logic       expected_zero;
    logic       expected_negative;
    logic       expected_equal;
    logic       expected_great;
    logic       expected_less;
    string      test_name;
} test_vector_t;

// Test Vector Array
test_vector_t test_vectors [];

// ========================================================================
// Arithmetic Operation Test Vectors
// ========================================================================

// ADD Operations
initial begin
    test_vectors[0] = '{A: 8'd42, B: 8'd23, opcode: 5'd0, expected_result: 8'd65, 
                       expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b0,
                       expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                       test_name: "ADD: 42 + 23"};
    
    test_vectors[1] = '{A: 8'd200, B: 8'd100, opcode: 5'd0, expected_result: 8'd44,
                       expected_carry: 1'b1, expected_zero: 1'b0, expected_negative: 1'b0,
                       expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                       test_name: "ADD: 200 + 100 (overflow)"};
    
    test_vectors[2] = '{A: 8'd0, B: 8'd0, opcode: 5'd0, expected_result: 8'd0,
                       expected_carry: 1'b0, expected_zero: 1'b1, expected_negative: 1'b0,
                       expected_equal: 1'b1, expected_great: 1'b0, expected_less: 1'b0,
                       test_name: "ADD: 0 + 0"};
    
    test_vectors[3] = '{A: 8'd255, B: 8'd1, opcode: 5'd0, expected_result: 8'd0,
                       expected_carry: 1'b1, expected_zero: 1'b1, expected_negative: 1'b0,
                       expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                       test_name: "ADD: 255 + 1 (wrap to zero)"};
end

// SUB Operations
initial begin
    test_vectors[10] = '{A: 8'd65, B: 8'd23, opcode: 5'd1, expected_result: 8'd42,
                        expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b0,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "SUB: 65 - 23"};
    
    test_vectors[11] = '{A: 8'd23, B: 8'd65, opcode: 5'd1, expected_result: 8'd214,
                        expected_carry: 1'b1, expected_zero: 1'b0, expected_negative: 1'b1,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "SUB: 23 - 65 (underflow)"};
    
    test_vectors[12] = '{A: 8'd5, B: 8'd5, opcode: 5'd1, expected_result: 8'd0,
                        expected_carry: 1'b0, expected_zero: 1'b1, expected_negative: 1'b0,
                        expected_equal: 1'b1, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "SUB: 5 - 5 (zero result)"};
end

// INC Operations
initial begin
    test_vectors[20] = '{A: 8'd42, B: 8'd0, opcode: 5'd2, expected_result: 8'd43,
                        expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b0,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "INC: 42 + 1"};
    
    test_vectors[21] = '{A: 8'd255, B: 8'd0, opcode: 5'd2, expected_result: 8'd0,
                        expected_carry: 1'b1, expected_zero: 1'b1, expected_negative: 1'b0,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "INC: 255 + 1 (overflow)"};
end

// DEC Operations
initial begin
    test_vectors[30] = '{A: 8'd43, B: 8'd0, opcode: 5'd3, expected_result: 8'd42,
                        expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b0,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "DEC: 43 - 1"};
    
    test_vectors[31] = '{A: 8'd0, B: 8'd0, opcode: 5'd3, expected_result: 8'd255,
                        expected_carry: 1'b1, expected_zero: 1'b0, expected_negative: 1'b1,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "DEC: 0 - 1 (underflow)"};
end

// ========================================================================
// Logic Operation Test Vectors
// ========================================================================

// AND Operations
initial begin
    test_vectors[40] = '{A: 8'hAA, B: 8'h55, opcode: 5'd13, expected_result: 8'h00,
                        expected_carry: 1'b0, expected_zero: 1'b1, expected_negative: 1'b0,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "AND: 0xAA & 0x55"};
    
    test_vectors[41] = '{A: 8'hFF, B: 8'h0F, opcode: 5'd13, expected_result: 8'h0F,
                        expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b0,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "AND: 0xFF & 0x0F"};
end

// OR Operations
initial begin
    test_vectors[50] = '{A: 8'hAA, B: 8'h55, opcode: 5'd14, expected_result: 8'hFF,
                        expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b1,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "OR: 0xAA | 0x55"};
end

// XOR Operations
initial begin
    test_vectors[60] = '{A: 8'hAA, B: 8'h55, opcode: 5'd10, expected_result: 8'hFF,
                        expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b1,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "XOR: 0xAA ^ 0x55"};
    
    test_vectors[61] = '{A: 8'hFF, B: 8'hFF, opcode: 5'd10, expected_result: 8'h00,
                        expected_carry: 1'b0, expected_zero: 1'b1, expected_negative: 1'b0,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "XOR: 0xFF ^ 0xFF (zero)"};
end

// NAND Operations
initial begin
    test_vectors[70] = '{A: 8'hFF, B: 8'hFF, opcode: 5'd8, expected_result: 8'h00,
                        expected_carry: 1'b0, expected_zero: 1'b1, expected_negative: 1'b0,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "NAND: ~(0xFF & 0xFF)"};
end

// NOR Operations
initial begin
    test_vectors[80] = '{A: 8'h00, B: 8'h00, opcode: 5'd9, expected_result: 8'hFF,
                        expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b1,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "NOR: ~(0x00 | 0x00)"};
end

// ========================================================================
// Shift Operation Test Vectors
// ========================================================================

// LSL Operations
initial begin
    test_vectors[90] = '{A: 8'h42, B: 8'h00, opcode: 5'd4, expected_result: 8'h84,
                        expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b1,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "LSL: 0x42 << 1"};
    
    test_vectors[91] = '{A: 8'h80, B: 8'h00, opcode: 5'd4, expected_result: 8'h00,
                        expected_carry: 1'b1, expected_zero: 1'b1, expected_negative: 1'b0,
                        expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                        test_name: "LSL: 0x80 << 1 (overflow)"};
end

// LSR Operations
initial begin
    test_vectors[100] = '{A: 8'h84, B: 8'h00, opcode: 5'd5, expected_result: 8'h42,
                         expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b0,
                         expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                         test_name: "LSR: 0x84 >> 1"};
end

// ASR Operations
initial begin
    test_vectors[110] = '{A: 8'h84, B: 8'h00, opcode: 5'd6, expected_result: 8'hC2,
                         expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b1,
                         expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                         test_name: "ASR: 0x84 >> 1 (sign extend)"};
    
    test_vectors[111] = '{A: 8'h42, B: 8'h00, opcode: 5'd6, expected_result: 8'h21,
                         expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b0,
                         expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                         test_name: "ASR: 0x42 >> 1 (positive)"};
end

// ========================================================================
// Special Operation Test Vectors
// ========================================================================

// NOT A Operations
initial begin
    test_vectors[120] = '{A: 8'h42, B: 8'h00, opcode: 5'd17, expected_result: 8'hBD,
                         expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b1,
                         expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                         test_name: "NOT A: ~0x42"};
end

// NOT B Operations
initial begin
    test_vectors[130] = '{A: 8'h00, B: 8'h55, opcode: 5'd18, expected_result: 8'hAA,
                         expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b1,
                         expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b0,
                         test_name: "NOT B: ~0x55"};
end

// CMP Operations
initial begin
    test_vectors[140] = '{A: 8'd5, B: 8'd5, opcode: 5'd16, expected_result: 8'd0,
                         expected_carry: 1'b0, expected_zero: 1'b1, expected_negative: 1'b0,
                         expected_equal: 1'b1, expected_great: 1'b0, expected_less: 1'b0,
                         test_name: "CMP: 5 == 5"};
    
    test_vectors[141] = '{A: 8'd10, B: 8'd5, opcode: 5'd16, expected_result: 8'd5,
                         expected_carry: 1'b0, expected_zero: 1'b0, expected_negative: 1'b0,
                         expected_equal: 1'b0, expected_great: 1'b1, expected_less: 1'b0,
                         test_name: "CMP: 10 > 5"};
    
    test_vectors[142] = '{A: 8'd5, B: 8'd10, opcode: 5'd16, expected_result: 8'd251,
                         expected_carry: 1'b1, expected_zero: 1'b0, expected_negative: 1'b1,
                         expected_equal: 1'b0, expected_great: 1'b0, expected_less: 1'b1,
                         test_name: "CMP: 5 < 10"};
end

`endif // TEST_VECTORS_V
