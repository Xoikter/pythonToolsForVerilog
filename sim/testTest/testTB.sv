`include "uvm_macros.svh"
import uvm_pkg::*;
module testTB;
<<<<<<< HEAD
logic clk;
test_interface test_if();
test test_inst (
        .clk  (test_if.ifo.clk) ,//input   
        .a    (test_if.ifo.a  ) ,//input   [3:0]
        .b    (test_if.ifo.b  ) ,//input   [3:0]
        .c    (test_if.ifo.c  ));//output  [4:0]
initial begin
clk = 0;
=======
logic vld;
logic clk;
test_interface test_if();
test test_inst (
      //   .clk  (test_if.ifo.clk) ,//input   
      //   .clk  (test_if.ifo.clk) ,//input   
        .a    (test_if.a  ) ,//input   [3:0]
        .b    (test_if.b  ) ,//input   [3:0]
        .c    (test_if.c  ));//output  [4:0]

always #5 clk = ~clk;
// assign test_if.clk = clk;
always @(*) begin
   test_if.clk <= clk;
   // test_if.vld <= vld;
end
initial begin
// clk = 0;
clk = 0;
vld = 0;
@(posedge clk);
vld = 1;
>>>>>>> 51f05884d12d5605490827a74c95fc41601c853c
end
initial begin
   run_test();
end
initial begin
   uvm_config_db#(virtual test_interface)::set(null, "uvm_test_top.env.i_agt.drv", "vif", test_if);
   uvm_config_db#(virtual test_interface)::set(null, "uvm_test_top.env.i_agt.mon", "vif", test_if);
   uvm_config_db#(virtual test_interface)::set(null, "uvm_test_top.env.o_agt.mon", "vif", test_if);
end

<<<<<<< HEAD
always #5 clk = ~clk;
always@* test_if.ifo.clk <= clk;

=======
// always #5 clk = ~clk;
>>>>>>> 51f05884d12d5605490827a74c95fc41601c853c


endmodule
