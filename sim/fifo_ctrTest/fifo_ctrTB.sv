`include "uvm_macros.svh"
module fifo_ctrTB;
fifo_ctr_interface_port ifo ();
fifo_ctr_interface_inner ifi ();
logic clk;
logic rst_n;
logic rst_p;
fifo_ctr fifo_ctr_inst (
        .clk_wr   (ifo.clk_wr ) ,//input   
        .clk_rd   (ifo.clk_rd ) ,//input   
        .rst_n    (ifo.rst_n  ) ,//input   
        .w_valid  (ifo.w_valid) ,//input   
        .r_valid  (ifo.r_valid) ,//input   
        .w_data   (ifo.w_data ) ,//input   [`data_width-1:0]
        .r_data   (ifo.r_data ) ,//output  [`data_width-1:0]
        .full     (ifo.full   ) ,//output  
        .empty    (ifo.empty  ));//output  
initial begin
clk = 0;
rst_n = 0;
rst_p = 1;
#8 rst_n = 1;
#6 rst_p = 0;

end


always #5 clk = ~clk;

always@ * begin
ifo.clk <= clk;
ifo.rst_n <= rst_n;
asadasdad;


end

initial begin
   run_test();
end
initial begin
   uvm_config_db#(virtual fifo_ctr_interface_port)::set(null, "uvm_test_top.env.i_agt.drv", "vif", ifo);
   uvm_config_db#(virtual fifo_ctr_interface_port)::set(null, "uvm_test_top.env.i_agt.mon", "vif", ifo);
   uvm_config_db#(virtual fifo_ctr_interface_port)::set(null, "uvm_test_top.env.o_agt.mon", "vif", ifo);
   uvm_config_db#(virtual fifo_ctr_interface_inner)::set(null, "uvm_test_top.env.i_agt.drv", "vif_i", ifi);
   uvm_config_db#(virtual fifo_ctr_interface_inner)::set(null, "uvm_test_top.env.i_agt.mon", "vif_i", ifi);
   uvm_config_db#(virtual fifo_ctr_interface_inner)::set(null, "uvm_test_top.env.o_agt.mon", "vif_i", ifi);
end





endmodule
