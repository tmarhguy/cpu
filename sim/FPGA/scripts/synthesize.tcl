################################################################################
# Vivado Synthesis Script for ALU
#
# This script synthesizes the ALU design and generates reports.
#
# Usage:
#   vivado -mode batch -source synthesize.tcl
#
################################################################################

# Open project (assumes project already created)
# If project doesn't exist, create it first using vivadoCreateProject.tcl
open_project ./vp/vp.xpr

# Set synthesis strategy
set_property strategy Flow_AreaOptimized_high [get_runs synth_1]

# Run synthesis
puts "Running synthesis..."
launch_runs synth_1 -jobs 4
wait_on_run synth_1

# Check synthesis status
if {[get_property PROGRESS [get_runs synth_1]] != "100%"} {
    puts "ERROR: Synthesis failed!"
    exit 1
}

puts "Synthesis completed successfully!"

# Generate reports
puts "Generating reports..."

# Resource utilization report
report_utilization -file reports/utilization_synth.rpt
puts "  - Utilization report: reports/utilization_synth.rpt"

# Timing report
report_timing_summary -file reports/timing_synth.rpt
puts "  - Timing report: reports/timing_synth.rpt"

# Power report (if available)
# report_power -file reports/power_synth.rpt
# puts "  - Power report: reports/power_synth.rpt"

puts "\nSynthesis complete! Check reports/ directory for results."

# Close project
close_project
