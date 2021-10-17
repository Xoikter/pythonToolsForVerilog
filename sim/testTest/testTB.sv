`include "uvm_macros.svh"
import uvm_pkg::*;
module testTB;
logic clk;
test_interface test_if();
test test_inst (
        .clk  (test_if.ifo.clk) ,//input   
        .a    (test_if.ifo.a  ) ,//input   [3:0]
        .b    (test_if.ifo.b  ) ,//input   [3:0]
        .c    (test_if.ifo.c  ));//output  [4:0]
initial begin
clk = 0;
end
initial begin
   run_test();
end
initial begin
   uvm_config_db#(virtual test_interface)::set(null, "uvm_test_top.env.i_agt.drv", "vif", test_if);
   uvm_config_db#(virtual test_interface)::set(null, "uvm_test_top.env.i_agt.mon", "vif", test_if);
   uvm_config_db#(virtual test_interface)::set(null, "uvm_test_top.env.o_agt.mon", "vif", test_if);
end

always #5 clk = ~clk;
always@* test_if.ifo.clk <= clk;



endmodule
