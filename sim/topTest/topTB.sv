module topTB;
top_interface if;
top topInst(
top top_inst (
        .clk    (if.ifo.clk  ) ,//input   
        .rst_n  (if.ifo.rst_n));//input   
initial begin

end
initial begin
   uvm_config_db#(virtual top_if)::set(null, "uvm_test_top.env.i_agt.drv", "vif", if);
   uvm_config_db#(virtual top_if)::set(null, "uvm_test_top.env.o_agt.drv", "vif", if);
   uvm_config_db#(virtual top_if)::set(null, "uvm_test_top.env.o_agt.drv", "vif", if);
end





endmodule
