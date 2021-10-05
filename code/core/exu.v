module exu(
    input wire clk,
    input wire rst_n,
    input wire [`INSTR_WIDTH-1:0] instr,
    input [`PC_WIDTH - 1 : 0] i_pc,
    input [`PC_WIDTH - 1 : 0] o_pc,
    input i_predict_flag,
    output wire pipe_flush,
    output wire pipe_stall,
    //lsu interface
    input lsu_wready,
    input lsu_rready,
    output [`ADDR_WIDTH - 1 : 0] exu_addr,
    output exu_addr_vld,
    output lsu_wr,
    output [31:0] o_data,
    output [31:0] i_data,
    output o_datavld,
    input  i_datavld);
reg [`INSTR_WIDTH - 1 : 0] instr_i;

always@(posedge clk or negedge rst_n) begin
    if(!rst_n)
        instr_i <= 0;
    else
        instr_i <= instr;
end
// always@(posedge clk or negedge rst_n) begin
//    if(rst_n) begin
//        pipe_flush <= 0;
//        pipe_stall <= 0;
//    end
//    else begin
//        pipe_stall <= 1;
//        pipe_flush <= 1;
//    end
// end
// wire [`INSTR_SIZE-1:0] instr_i;
wire dec_rs1en;
wire dec_rs2en;
wire dec_rden;
wire [`RFIDX_WIDTH-1:0] dec_rs1idx;
wire [`RFIDX_WIDTH-1:0] dec_rs2idx;
wire [`RFIDX_WIDTH-1:0] dec_rdidx;
wire [31:0] rs1;
wire [31:0] rs2;
wire [31:0] rd;
// wire lsu_rready,lsu_wready,exu_addr_vld,o_datavld,i_datavld;
// wire [31:0] o_data,i_data;
// wire [`ADDR_WIDTH - 1 : 0] exu_addr;
// wire dec_bjp;
// wire dec_jal;
// wire dec_jalr;
wire [31:0] dec_imm;
wire [`DEC_INFO_BUS_WIDTH - 1 : 0] dec_info_bus;

decode exu_decode(
                        .instr(instr_i),
                        .dec_rs1en(dec_rs1en),
                        .dec_rs2en(dec_rs2en),
                        .dec_rs1idx(dec_rs1idx),
                        .dec_rs2idx(dec_rs2idx),
                        .dec_bjp(),
                        .dec_rden(dec_rden),
                        .dec_rdidx(dec_rdidx),
                        .dec_jal(),
                        .dec_jalr(),
                        .dec_imm(dec_imm),
                        .dec_info_bus(dec_info_bus));

alu alu_inst(
    .clk(clk),
    .rst_n(rst_n),
    .i_dec_info_bus(dec_info_bus),
    .i_predict_flag(i_predict_flag),
    .i_rs1(rs1),
    .i_rs2(rs2),
    .i_imm(dec_imm),
    .o_rd_index(dec_rdidx),
    .o_rd(rd),
    .i_pc(i_pc),
    .pipe_flush(pipe_flush),
    .o_exu_ifu_pc(o_pc),
    .exu_addr(exu_addr),
    .exu_addr_vld(exu_addr_vld),
    .lsu_wready(lsu_wready),
    .lsu_rready(lsu_rready),
    .lsu_wr(lsu_wr),
    .o_data(o_data),
    .i_data(i_data),
    .o_datavld(o_datavld),
    .i_datavld(i_datavld)
);

regfile regfile_inst(
                    .clk(clk),
                    .rst_n(rst_n),
                    .i_rs1en(dec_rs1en),
                    .i_rs2en(dec_rs2en),
                    .i_rden(dec_rden),
                    .i_rs1idx(dec_rs1idx),
                    .i_rs2idx(dec_rs2idx),
                    .i_rdidx(dec_rdidx),
                    .o_rs1(rs1),
                    .o_rs2(rs2),
                    .i_rd(rd)

);
assign pipe_stall = 0;


endmodule