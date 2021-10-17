interface fifo_ctr_interface_port;
logic clk_wr;
logic clk_rd;
logic rst_n;
logic w_valid;
logic r_valid;
logic [`data_width-1:0] w_data;
logic [`data_width-1:0] r_data;
logic full;
logic empty;




endinterface