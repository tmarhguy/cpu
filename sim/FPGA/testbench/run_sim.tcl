################################################################################
# Vivado Simulation Script for ALU Testbench
#
# This script sets up and runs the ALU testbench simulation in Vivado.
#
# Usage:
#   vivado -mode batch -source run_sim.tcl
#   or
#   vivado -mode gui -source run_sim.tcl
#
################################################################################

# Set project name and directory
set project_name "alu_sim"
set project_dir "./${project_name}"

# Create project
create_project ${project_name} ${project_dir} -part xc7a35tftg256-1 -force

# Set project properties
set_property target_language Verilog [current_project]
set_property default_lib work [current_project]

# Add source files
puts "Adding source files..."

# Main ALU module
add_files -fileset sources_1 {
    ../verilog/circuit/main.v
}

# Arithmetic modules
add_files -fileset sources_1 {
    ../verilog/arith/Adder.v
}

# Gate modules
add_files -fileset sources_1 {
    ../verilog/gates/AND_GATE.v
    ../verilog/gates/AND_GATE_3_INPUTS.v
    ../verilog/gates/AND_GATE_4_INPUTS.v
    ../verilog/gates/NAND_GATE_BUS.v
    ../verilog/gates/NOR_GATE.v
    ../verilog/gates/NOR_GATE_8_INPUTS.v
    ../verilog/gates/NOR_GATE_BUS.v
    ../verilog/gates/OR_GATE.v
    ../verilog/gates/XOR_GATE_BUS_ONEHOT.v
}

# Multiplexer modules
add_files -fileset sources_1 {
    ../verilog/plexers/Multiplexer_bus_2.v
    ../verilog/plexers/Multiplexer_bus_4.v
    ../verilog/plexers/Multiplexer_bus_8.v
}

# Memory modules
add_files -fileset sources_1 {
    ../verilog/memory/LogisimCounter.v
}

# Base modules (clock generation)
add_files -fileset sources_1 {
    ../verilog/base/LogisimClockComponent.v
    ../verilog/base/logisimTickGenerator.v
    ../verilog/base/synthesizedClockGenerator.v
}

# Top-level wrapper
add_files -fileset sources_1 {
    ../verilog/toplevel/logisimTopLevelShell.v
}

# Add testbench
puts "Adding testbench..."
add_files -fileset sim_1 {
    alu_tb.v
    test_vectors.v
}

# Set top module for simulation
set_property top alu_tb [get_filesets sim_1]
set_property top_lib xil_defaultlib [get_filesets sim_1]

# Update compile order
update_compile_order -fileset sim_1

# Launch simulation
puts "Launching simulation..."
launch_simulation

# Run simulation for sufficient time
# Adjust time based on testbench requirements
run 50000ns

# Optional: Save waveform
# open_vcd
# log_vcd /alu_tb/*
# run 50000ns
# close_vcd

puts "Simulation complete!"
puts "Check the console for test results."

# Keep GUI open if in GUI mode
if {[info exists ::env(VIVADO_MODE)] && $::env(VIVADO_MODE) == "gui"} {
    puts "Simulation finished. GUI will remain open for inspection."
} else {
    # Exit in batch mode
    quit
}
