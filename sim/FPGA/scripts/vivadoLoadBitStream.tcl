open_hw
connect_hw_server
open_hw_target
set_property PROGRAM.FILE {/Users/tmarhguy/logisim_evolution_workspace/alu_top/main/sandbox//vp/vp.runs/impl_1/logisimTopLevelShell.bit} [lindex [get_hw_devices] 1]
current_hw_device [lindex [get_hw_devices] 1]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices] 1]
program_hw_device [lindex [get_hw_devices] 1]
close_hw
exit
