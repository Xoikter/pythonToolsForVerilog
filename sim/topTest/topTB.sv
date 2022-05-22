`include "uvm_macros.svh"
module topTB;
top_interface_port ifo ();
top_interface_inner ifi ();
logic clk;
logic rst_n;
logic rst_p;
top top_inst (
        .clk    (ifo.clk  ) ,//input   
        .rst_n  (ifo.rst_n));//input   
always #5 clk = ~clk;

initial begin
clk = 0;
rst_n = 0;
rst_p = 1;
#8 rst_n = 1;
#6 rst_p = 0;

end

always@ * begin
ifo.clk <= clk;
ifo.rst_n <= rst_n;

end

initial begin
   run_test();
end

initial begin
   uvm_config_db#(virtual top_interface_port)::set(null, "uvm_test_top.env.i_agt.drv", "vif", ifo);
   uvm_config_db#(virtual top_interface_port)::set(null, "uvm_test_top.env.i_agt.mon", "vif", ifo);
   uvm_config_db#(virtual top_interface_port)::set(null, "uvm_test_top.env.o_agt.mon", "vif", ifo);
   uvm_config_db#(virtual top_interface_inner)::set(null, "uvm_test_top.env.i_agt.drv", "vif_i", ifi);
   uvm_config_db#(virtual top_interface_inner)::set(null, "uvm_test_top.env.i_agt.mon", "vif_i", ifi);
   uvm_config_db#(virtual top_interface_inner)::set(null, "uvm_test_top.env.o_agt.mon", "vif_i", ifi);
end





endmodule
