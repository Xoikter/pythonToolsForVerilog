module top(
            input wire clk,
            input rst_n
);


wire [`INSTR_WIDTH - 1 : 0] pre_instr;
wire [`INSTR_WIDTH - 1 : 0] instr;
wire [`PC_WIDTH - 1 : 0] pc, o_pc,last_pc;

wire [`ADDR_WIDTH - 1 : 0] awaddr;
wire awvalid,awready,wvalid,wlast,wready,bresp,bvalid,bready;
wire arvalid,arready,rlast,rvalid,rready;
wire [7:0] awlen;
wire [7:0] arlen;
wire [2:0] awsize;
wire [2:0] arsize;
wire [1:0] awburst;
wire [1:0] arburst;
wire [1:0] bresp;


wire [`ADDR_WIDTH - 1 : 0] exu_addr;
wire exu_addr_vld;
wire lsu_rready,lsu_wready,lsu_wr;
wire [31:0] i_data;
wire [31:0] o_data;
wire i_datavld,o_datavld;

ram ram_inst(
            .pc(pc),
            .instr(pre_instr),
            .pc_vld(pc_vld),
            .clk(clk),
            .rst_n(rst_n)
);




ifu ifu_inst(
             .clk(clk),
             .rst_n(rst_n),
             .pc_vld(pc_vld),
             .pre_instr(pre_instr),
             .pc_ram(pc),
             .exu_pc(o_pc),
             .instr_exu(instr),
             .pipe_flush(pipe_flush),
             .o_predict_flag(predict_flag),
             .last_pc(last_pc),
             .pipe_stall(pipe_stall));


exu exu_inst(
    .clk (clk),
    .rst_n (rst_n),
    .instr (instr),
    .i_pc (last_pc),
    .o_pc (o_pc),
    .pipe_flush (pipe_flush),
    .i_predict_flag(predict_flag),
    .pipe_stall(pipe_stall),
    .lsu_rready(lsu_rready),
    .lsu_wready(lsu_wready),
    .exu_addr(exu_addr),
    .exu_addr_vld(exu_addr_vld),
    .lsu_wr(lsu_wr),
    .o_data(o_data),
    .i_data(i_data),
    .o_datavld(o_datavld),
    .i_datavld(i_datavld)
    );

lsu lsu_inst(
            .clk(clk),
            .rst_n(rst_n),
            .addr(exu_addr),
            .addr_vld(exu_addr_vld),
            .lsu_wready(lsu_wready),
            .lsu_rready(lsu_rready),
            .lsu_wr(lsu_wr),
            .i_data(o_data),
            .o_data(i_data),
            .i_datavld(o_datavld),
            .o_datavld(i_datavld),
            .awaddr(awaddr),
            .awvalid(awvalid),
            .awlen(awlen),
            .awsize(awsize),
            .awburst(awburst),
            .awready(awready),
            .wdata(wdata),
            .wvalid(wvalid),
            .wlast(wlast),
            .wready(wready),
            .bresp(bresp),
            .bvalid(bvalid),
            .bready(bready),
            .araddr(araddr),
            .arvalid(arvalid),
            .arlen(arlen),
            .arsize(arsize),
            .arburst(arburst),
            .arready(arready),
            .rdata(rdata),
            .rlast(rlast),
            .rvalid(rvalid),
            .rready(rready));

// initial begin
//     $fsdbDumpfile("/home/IC/xsc/RTL/RISCV/tb.fsdb");
//     $fsdbDumpvars(0,"tb");
//     #500 $finish;
// end

endmodule