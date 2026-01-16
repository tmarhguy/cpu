`timescale 1ns / 1ps

module top_tb;

    logic clk;
    logic btnC;
    wire [7:0] led;

    // Instantiate Top Level
    FPGA_Top uut (
        .clk(clk),
        .btnC(btnC),
        .led(led)
    );

    // Clock Generation
    always #5 clk = ~clk; // 100MHz

    initial begin
        // Initialize
        clk = 0;
        btnC = 1; // Reset
        #100;
        
        btnC = 0; // Release Reset
        
        // Wait for some cycles
        // Since divider is 1Hz (100M cycles), we won't see changes in simulation easily unless we override params
        // But for compilation check it's enough.
        
        #1000;
        $finish;
    end

endmodule
