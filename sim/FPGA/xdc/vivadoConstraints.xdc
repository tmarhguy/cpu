set_property PACKAGE_PIN N14 [get_ports {fpgaGlobalClock}]
    set_property IOSTANDARD LVCMOS33 [get_ports {fpgaGlobalClock}]
    create_clock -add -name sys_clk_pin -period 10.00 -waveform {0 5}  [get_ports {fpgaGlobalClock}]

