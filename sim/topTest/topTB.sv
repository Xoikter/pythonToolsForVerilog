module topTB;
top_interface top_if;
top topInst(
top top_inst (
        .clk    (if.ifo.clk  ) ,//input   
        .rst_n  (if.ifo.rst_n));//input   
initial begin

end
initial begin
   uvm_config_db#(virtual top_interface)::set(null, "uvm_test_top.env.i_agt.drv", "vif", top_if);
   uvm_config_db#(virtual top_interface)::set(null, "uvm_test_top.env.o_agt.drv", "vif", top_if);
   uvm_config_db#(virtual top_interface)::set(null, "uvm_test_top.env.o_agt.drv", "vif", top_if);
end





endmodule
