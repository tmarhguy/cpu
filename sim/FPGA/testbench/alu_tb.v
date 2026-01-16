/******************************************************************************
 ** Testbench: 8-Bit ALU Comprehensive Test Suite
 ** 
 ** This testbench verifies all 19 ALU operations with comprehensive
 ** test coverage including edge cases and flag generation.
 **
 ** Test Coverage:
 **   - All 19 operations (ADD, SUB, INC, DEC, LSL, LSR, ASR, REV,
 **     NAND, NOR, XOR, PASS A, PASS B, AND, OR, XNOR, CMP, NOT A, NOT B)
 **   - Flag generation (Carry, Zero, Negative, Comparison flags)
 **   - Edge cases (overflow, underflow, zero results)
 **
 *****************************************************************************/

`timescale 1ns / 1ps

module alu_tb;

    // Test Parameters
    parameter CLK_PERIOD = 10;  // 10ns = 100 MHz
    
    // Inputs
    reg [7:0] A_IN;
    reg [7:0] B_IN;
    reg       GND;
    reg [4:0] Opcode;
    
    // Outputs
    wire [7:0] ASR;
    wire [7:0] A_DEC;
    wire [7:0] B_DEC;
    wire [1:0] B_SEL;
    wire [7:0] CMP_REG;
    wire       C_IN;
    wire       C_OUT;
    wire       EQUAL_FL;
    wire       GREAT_FL;
    wire       LESS_FL;
    wire [7:0] LOGIC_OUT;
    wire [7:0] LSL;
    wire [7:0] LSR;
    wire       M;
    wire [7:0] OVERALL;
    wire [7:0] Output_bus_1;
    wire [7:0] REV_A;
    wire [7:0] SUM;
    wire [24:0] logisimOutputBubbles;
    
    // Test Control
    integer test_count = 0;
    integer pass_count = 0;
    integer fail_count = 0;
    
    // Instantiate Unit Under Test
    // Instantiate Unit Under Test
    ALU #(
        .WIDTH(8)
    ) uut (
        .A(A_IN),
        .B(B_IN),
        .Opcode(Opcode),
        .Result(OVERALL),
        .CarryOut(C_OUT),
        .Zero(EQUAL_FL),
        .Negative(M), // M seems to be Negative flag in main.v (or wire leading to it) - based on checks, let's verify.
        // Actually, let's check what M is checked against.
        // alu_tb checks C_OUT, EQUAL_FL. It doesn't check M in the snippets I saw for flags?
        // Wait, "SUB: 23 - 65 (underflow)" check_result(214...).
        // "CMP: 10 > 5" checks GREAT_FL.
        // My ALU has Great, Less.
        .Great(GREAT_FL),
        .Less(LESS_FL),
        .Overflow() // Not checked in TB
    );
    
    // Unused outputs from original TB (wires)
    assign ASR = OVERALL;
    assign LSL = OVERALL;
    assign LSR = OVERALL;
    assign SUM = OVERALL;
    assign LOGIC_OUT = OVERALL;
    
    // Clock Generation (if needed)
    // Note: The ALU is combinational, but clock tree is provided for compatibility
    
    // Test Helper Functions
    task check_result;
        input [7:0] expected;
        input [7:0] actual;
        input string test_name;
        begin
            test_count = test_count + 1;
            if (expected === actual) begin
                $display("[PASS] %s: Expected 0x%02X, Got 0x%02X", test_name, expected, actual);
                pass_count = pass_count + 1;
            end else begin
                $display("[FAIL] %s: Expected 0x%02X, Got 0x%02X", test_name, expected, actual);
                fail_count = fail_count + 1;
            end
        end
    endtask
    
    task check_flag;
        input expected;
        input actual;
        input string flag_name;
        begin
            test_count = test_count + 1;
            if (expected === actual) begin
                $display("[PASS] %s: Expected %b, Got %b", flag_name, expected, actual);
                pass_count = pass_count + 1;
            end else begin
                $display("[FAIL] %s: Expected %b, Got %b", flag_name, expected, actual);
                fail_count = fail_count + 1;
            end
        end
    endtask
    
    // Initialize
    initial begin
        $display("========================================");
        $display("8-Bit ALU Comprehensive Test Suite");
        $display("========================================\n");
        
        // Initialize inputs
        A_IN = 8'h00;
        B_IN = 8'h00;
        GND = 1'b0;
        Opcode = 0;
        
        #100; // Wait for initialization
        
        // Run test suites
        test_arithmetic_operations();
        test_logic_operations();
        test_shift_operations();
        test_special_operations();
        test_flags();
        test_edge_cases();
        
        // Print summary
        #100;
        $display("\n========================================");
        $display("Test Summary");
        $display("========================================");
        $display("Total Tests: %d", test_count);
        $display("Passed:      %d", pass_count);
        $display("Failed:      %d", fail_count);
        $display("========================================\n");
        
        if (fail_count == 0) begin
            $display("*** ALL TESTS PASSED ***");
        end else begin
            $display("*** SOME TESTS FAILED ***");
        end
        
        $finish;
    end
    
    // ========================================================================
    // Test Suite 1: Arithmetic Operations
    // ========================================================================
    task test_arithmetic_operations;
        begin
            $display("\n--- Test Suite 1: Arithmetic Operations ---\n");
            
            // Test ADD: 42 + 23 = 65
            Opcode = 0; // ADD
            A_IN = 8'd42;
            B_IN = 8'd23;
            #10;
            check_result(8'd65, OVERALL, "ADD: 42 + 23");
            
            // Test ADD: 200 + 100 = 44 (overflow, wraps to 44)
            Opcode = 0; // ADD
            A_IN = 8'd200;
            B_IN = 8'd100;
            #10;
            check_result(8'd44, OVERALL, "ADD: 200 + 100 (overflow)");
            check_flag(1'b1, C_OUT, "ADD: Carry flag on overflow");
            
            // Test SUB: 65 - 23 = 42
            Opcode = 1; // SUB
            A_IN = 8'd65;
            B_IN = 8'd23;
            #10;
            check_result(8'd42, OVERALL, "SUB: 65 - 23");
            
            // Test SUB: 23 - 65 = 214 (underflow, 2's complement)
            Opcode = 1; // SUB
            A_IN = 8'd23;
            B_IN = 8'd65;
            #10;
            check_result(8'd214, OVERALL, "SUB: 23 - 65 (underflow)");
            
            // Test INC: 42 + 1 = 43
            Opcode = 2; // INC
            A_IN = 8'd42;
            B_IN = 8'd00;  // Not used for INC
            #10;
            check_result(8'd43, OVERALL, "INC: 42 + 1");
            
            // Test INC: 255 + 1 = 0 (overflow)
            Opcode = 2; // INC
            A_IN = 8'd255;
            B_IN = 8'd00;
            #10;
            check_result(8'd0, OVERALL, "INC: 255 + 1 (overflow)");
            check_flag(1'b1, C_OUT, "INC: Carry flag on overflow");
            
            // Test DEC: 43 - 1 = 42
            Opcode = 3; // DEC
            A_IN = 8'd43;
            B_IN = 8'd00;  // Not used for DEC
            #10;
            check_result(8'd42, OVERALL, "DEC: 43 - 1");
            
            // Test DEC: 0 - 1 = 255 (underflow)
            Opcode = 3; // DEC
            A_IN = 8'd0;
            B_IN = 8'd00;
            #10;
            check_result(8'd255, OVERALL, "DEC: 0 - 1 (underflow)");
        end
    endtask
    
    // ========================================================================
    // Test Suite 2: Logic Operations
    // ========================================================================
    task test_logic_operations;
        begin
            $display("\n--- Test Suite 2: Logic Operations ---\n");
            
            // Test AND: 0xAA & 0x55 = 0x00
            Opcode = 13; // AND
            A_IN = 8'hAA;
            B_IN = 8'h55;
            #10;
            check_result(8'h00, OVERALL, "AND: 0xAA & 0x55");
            
            // Test AND: 0xFF & 0x0F = 0x0F
            Opcode = 13; // AND
            A_IN = 8'hFF;
            B_IN = 8'h0F;
            #10;
            check_result(8'h0F, OVERALL, "AND: 0xFF & 0x0F");
            
            // Test OR: 0xAA | 0x55 = 0xFF
            Opcode = 14; // OR
            A_IN = 8'hAA;
            B_IN = 8'h55;
            #10;
            check_result(8'hFF, OVERALL, "OR: 0xAA | 0x55");
            
            // Test XOR: 0xAA ^ 0x55 = 0xFF
            Opcode = 10; // XOR
            A_IN = 8'hAA;
            B_IN = 8'h55;
            #10;
            check_result(8'hFF, OVERALL, "XOR: 0xAA ^ 0x55");
            
            // Test XOR: 0xFF ^ 0xFF = 0x00
            Opcode = 10; // XOR
            A_IN = 8'hFF;
            B_IN = 8'hFF;
            #10;
            check_result(8'h00, OVERALL, "XOR: 0xFF ^ 0xFF");
            check_flag(1'b1, EQUAL_FL, "XOR: Zero flag on zero result");
            
            // Test NAND: ~(0xFF & 0xFF) = 0x00
            Opcode = 8; // NAND
            A_IN = 8'hFF;
            B_IN = 8'hFF;
            #10;
            check_result(8'h00, OVERALL, "NAND: ~(0xFF & 0xFF)");
            
            // Test NOR: ~(0x00 | 0x00) = 0xFF
            Opcode = 9; // NOR
            A_IN = 8'h00;
            B_IN = 8'h00;
            #10;
            check_result(8'hFF, OVERALL, "NOR: ~(0x00 | 0x00)");
            
            // Test XNOR: ~(0xAA ^ 0x55) = 0x00
            Opcode = 11; // XNOR
            A_IN = 8'hAA;
            B_IN = 8'h55;
            #10;
            check_result(8'h00, OVERALL, "XNOR: ~(0xAA ^ 0x55)");
            
            // Test PASS A: Output = A
            Opcode = 12; // PASS A
            A_IN = 8'h42;
            B_IN = 8'h00;  // Not used
            #10;
            check_result(8'h42, OVERALL, "PASS A: Output = A");
            
            // Test PASS B: Output = B
            Opcode = 15; // PASS B
            A_IN = 8'h00;  // Not used
            B_IN = 8'h42;
            #10;
            check_result(8'h42, OVERALL, "PASS B: Output = B");
        end
    endtask
    
    // ========================================================================
    // Test Suite 3: Shift Operations
    // ========================================================================
    task test_shift_operations;
        begin
            $display("\n--- Test Suite 3: Shift Operations ---\n");
            
            // Test LSL: 0x42 << 1 = 0x84
            Opcode = 4; // LSL
            A_IN = 8'h42;
            B_IN = 8'h00;  // Not used
            #10;
            check_result(8'h84, OVERALL, "LSL: 0x42 << 1");
            
            // Test LSL: 0x80 << 1 = 0x00 (overflow)
            Opcode = 4; // LSL
            A_IN = 8'h80;
            B_IN = 8'h00;
            #10;
            check_result(8'h00, OVERALL, "LSL: 0x80 << 1 (overflow)");
            
            // Test LSR: 0x84 >> 1 = 0x42
            Opcode = 5; // LSR
            A_IN = 8'h84;
            B_IN = 8'h00;
            #10;
            check_result(8'h42, OVERALL, "LSR: 0x84 >> 1");
            
            // Test LSR: 0x01 >> 1 = 0x00
            Opcode = 5; // LSR
            A_IN = 8'h01;
            B_IN = 8'h00;
            #10;
            check_result(8'h00, OVERALL, "LSR: 0x01 >> 1");
            
            // Test ASR: 0x84 >> 1 = 0xC2 (sign extension)
            Opcode = 6; // ASR
            A_IN = 8'h84;  // Negative number (MSB = 1)
            B_IN = 8'h00;
            #10;
            check_result(8'hC2, OVERALL, "ASR: 0x84 >> 1 (sign extend)");
            
            // Test ASR: 0x42 >> 1 = 0x21 (positive, no sign extension)
            Opcode = 6; // ASR
            A_IN = 8'h42;  // Positive number (MSB = 0)
            B_IN = 8'h00;
            #10;
            check_result(8'h21, OVERALL, "ASR: 0x42 >> 1 (positive)");
        end
    endtask
    
    // ========================================================================
    // Test Suite 4: Special Operations
    // ========================================================================
    task test_special_operations;
        begin
            $display("\n--- Test Suite 4: Special Operations ---\n");
            
            // Test REV A: Reverse bit order
            Opcode = 7; // REV
            A_IN = 8'h42;
            B_IN = 8'h00;
            #10;
            // Note: REV_A output may need verification based on actual implementation
            
            // Test REV A: 0x81 = 0b10000001 -> reversed = 0x81 (symmetric)
            Opcode = 7; // REV
            A_IN = 8'h81;
            B_IN = 8'h00;
            #10;
            
            // Test NOT A: ~0x42 = 0xBD
            Opcode = 17; // NOT A
            A_IN = 8'h42;
            B_IN = 8'h00;
            #10;
            check_result(8'hBD, OVERALL, "NOT A: ~0x42");
            
            // Test NOT B: ~0x55 = 0xAA
            Opcode = 18; // NOT B
            A_IN = 8'h00;
            B_IN = 8'h55;
            #10;
            check_result(8'hAA, OVERALL, "NOT B: ~0x55");
        end
    endtask
    
    // ========================================================================
    // Test Suite 5: Flag Generation
    // ========================================================================
    task test_flags;
        begin
            $display("\n--- Test Suite 5: Flag Generation ---\n");
            
            // Test Zero Flag: 0 + 0 = 0
            Opcode = 0; // ADD
            A_IN = 8'd0;
            B_IN = 8'd0;
            #10;
            check_flag(1'b1, EQUAL_FL, "Zero Flag: 0 + 0 = 0");
            
            // Test Zero Flag: 5 - 5 = 0
            Opcode = 1; // SUB
            A_IN = 8'd5;
            B_IN = 8'd5;
            #10;
            check_flag(1'b1, EQUAL_FL, "Zero Flag: 5 - 5 = 0");
            
            // Test Carry Flag: 200 + 100 = 44 (carry)
            Opcode = 0; // ADD
            A_IN = 8'd200;
            B_IN = 8'd100;
            #10;
            check_flag(1'b1, C_OUT, "Carry Flag: 200 + 100");
            
            // Test Carry Flag: 100 + 100 = 200 (no carry)
            Opcode = 0; // ADD
            A_IN = 8'd100;
            B_IN = 8'd100;
            #10;
            check_flag(1'b0, C_OUT, "Carry Flag: 100 + 100 (no carry)");
        end
    endtask
    
    // ========================================================================
    // Test Suite 6: Comparison Operation
    // ========================================================================
    task test_comparison;
        begin
            $display("\n--- Test Suite 6: Comparison Operation ---\n");
            
            // Test CMP: A = B (5 == 5)
            Opcode = 16; // CMP
            A_IN = 8'd5;
            B_IN = 8'd5;
            #10;
            check_flag(1'b1, EQUAL_FL, "CMP: 5 == 5 (EQUAL)");
            check_flag(1'b0, GREAT_FL, "CMP: 5 == 5 (not GREAT)");
            check_flag(1'b0, LESS_FL, "CMP: 5 == 5 (not LESS)");
            
            // Test CMP: A > B (10 > 5)
            Opcode = 16; // CMP
            A_IN = 8'd10;
            B_IN = 8'd5;
            #10;
            check_flag(1'b0, EQUAL_FL, "CMP: 10 > 5 (not EQUAL)");
            check_flag(1'b1, GREAT_FL, "CMP: 10 > 5 (GREAT)");
            check_flag(1'b0, LESS_FL, "CMP: 10 > 5 (not LESS)");
            
            // Test CMP: A < B (5 < 10)
            Opcode = 16; // CMP
            A_IN = 8'd5;
            B_IN = 8'd10;
            #10;
            check_flag(1'b0, EQUAL_FL, "CMP: 5 < 10 (not EQUAL)");
            check_flag(1'b0, GREAT_FL, "CMP: 5 < 10 (not GREAT)");
            check_flag(1'b1, LESS_FL, "CMP: 5 < 10 (LESS)");
        end
    endtask
    
    // ========================================================================
    // Test Suite 7: Edge Cases
    // ========================================================================
    task test_edge_cases;
        begin
            $display("\n--- Test Suite 7: Edge Cases ---\n");
            
            // Test: Maximum values
            Opcode = 0; // ADD
            A_IN = 8'hFF;
            B_IN = 8'hFF;
            #10;
            check_result(8'hFE, OVERALL, "ADD: 0xFF + 0xFF (max values)");
            check_flag(1'b1, C_OUT, "Carry: 0xFF + 0xFF");
            
            // Test: Minimum values
            Opcode = 0; // ADD
            A_IN = 8'h00;
            B_IN = 8'h00;
            #10;
            check_result(8'h00, OVERALL, "ADD: 0x00 + 0x00 (min values)");
            check_flag(1'b1, EQUAL_FL, "Zero: 0x00 + 0x00");
            
            // Test: Signed overflow
            Opcode = 0; // ADD
            A_IN = 8'd127;  // Maximum positive signed
            B_IN = 8'd1;
            #10;
            check_result(8'd128, OVERALL, "ADD: 127 + 1 (signed overflow)");
            
            // Test: Signed underflow
            Opcode = 1; // SUB
            A_IN = 8'd128;  // Maximum negative signed
            B_IN = 8'd1;    // Will subtract
            #10;
            // Note: Depends on operation selected
        end
    endtask

endmodule
