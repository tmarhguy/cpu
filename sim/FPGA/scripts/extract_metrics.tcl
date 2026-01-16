################################################################################
# Extract Performance Metrics from Synthesis/Implementation
#
# This script extracts key metrics from Vivado reports and generates
# a summary document for performance analysis.
#
# Usage:
#   vivado -mode batch -source extract_metrics.tcl
#
################################################################################

# Open project
open_project ./vp/vp.xpr

# Open implementation run (or synthesis if implementation not run)
if {[get_runs impl_1] != ""} {
    open_run impl_1
    set report_type "Implementation"
} else {
    open_run synth_1
    set report_type "Synthesis"
}

puts "Extracting metrics from $report_type reports..."

# Create reports directory
file mkdir reports

# Extract utilization
report_utilization -file reports/utilization.txt
puts "  - Utilization report: reports/utilization.txt"

# Extract timing
report_timing_summary -file reports/timing.txt
puts "  - Timing report: reports/timing.txt"

# Extract power (if available)
if {[get_runs impl_1] != ""} {
    report_power -file reports/power.txt
    puts "  - Power report: reports/power.txt"
}

# Generate summary
set summary_file [open "reports/metrics_summary.txt" w]

puts $summary_file "========================================"
puts $summary_file "FPGA ALU Performance Metrics Summary"
puts $summary_file "========================================"
puts $summary_file ""
puts $summary_file "Report Type: $report_type"
puts $summary_file "Date: [clock format [clock seconds]]"
puts $summary_file ""
puts $summary_file "See detailed reports in reports/ directory:"
puts $summary_file "  - utilization.txt"
puts $summary_file "  - timing.txt"
if {[get_runs impl_1] != ""} {
    puts $summary_file "  - power.txt"
}
puts $summary_file ""
puts $summary_file "To update PERFORMANCE.md:"
puts $summary_file "  1. Review reports/metrics_summary.txt"
puts $summary_file "  2. Extract key values"
puts $summary_file "  3. Update docs/PERFORMANCE.md with actual numbers"
puts $summary_file ""

close $summary_file

puts ""
puts "Metrics extraction complete!"
puts "Summary: reports/metrics_summary.txt"
puts ""
puts "Next steps:"
puts "  1. Review reports/metrics_summary.txt"
puts "  2. Extract key metrics (LUTs, FFs, timing)"
puts "  3. Update docs/PERFORMANCE.md with actual values"

close_project
