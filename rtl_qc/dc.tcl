set top_design my_top

if{![file exists ./logs]}    {exec mkdir ./logs;}
if{![file exists ./reports]} {exec mkdir ./reports;}
if{![file exists ./outputs]} {exec mkdir ./outputs;}

set filelist{
    -f ../../filelist/filelist_def.f 
    -f ../../filelist/filelist_rtl.f 
            }

analyze -format sverilog $filelist

elaborate $top_design

set clk_src(clk) [get_ports clk]

set Period(300M) [expr 1000/300]

create_clock  -name clk -period $Period(300M) [get_port clk] $clk_src(clk)

set input_ports_grp(clk) [all_inputs]

set output_ports_grp(clk) [all_outputs]

set_input_delay -max [$Period(clk) * 0.6] -clock [get_clock clk] [all_inputs]
set_input_delay -min [$Period(clk) * 0.0] -clock [get_clock clk] [all_inputs]

set_output_delay -max [$Period(clk) * 0.6] -clock [get_clock clk] [all_outputs]
set_output_delay -max [$Period(clk) * 0.0] -clock [get_clock clk] [all_outputs]

set auto_wire_load_selection true

set_operating_conditions

set_clock_transtion 0.2 [all_clocks]

set_max_area 0

current_design $top_design

link > ./logs/link_check.log

uniquify

