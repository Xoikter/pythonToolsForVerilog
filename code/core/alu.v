module alu(
    input clk,
    input rst_n,
    input lsu_wready,
    input lsu_rready,
    output [`ADDR_WIDTH -1 : 0] exu_addr,
    output exu_addr_vld,
    output lsu_wr,
    output [31:0] o_data,
    input  [31:0] i_data,
    output o_datavld,
    input  i_datavld,
    input [`DEC_INFO_BUS_WIDTH - 1 : 0] i_dec_info_bus,
    input [31:0] i_rs1,
    input [31:0] i_rs2,
    input [31:0] i_imm,
    output [`RFIDX_WIDTH - 1 : 0] o_rd_index,
    output [31:0] o_rd,
    input [`PC_WIDTH - 1 : 0] i_pc,
    output [`PC_WIDTH - 1 : 0] o_exu_ifu_pc,
    output pipe_flush,
    input i_predict_flag);

wire [`DEC_INFO_BUS_WIDTH - 1 : 0] info_bus = i_dec_info_bus;

wire alu_op = info_bus[2:0] == `decode_alu_grp;
wire agu_op = info_bus[2:0] == `decode_agu_grp;
wire bjp_op = info_bus[2:0] == `decode_bjp_grp;



wire alu_req_alu_addsub = alu_op && (info_bus[`alu_info_add] || info_bus[`alu_info_sub]);
wire alu_req_alu_sub = alu_op && (info_bus[`alu_info_sub]);
// wire alu_req_alu_shift_right = alu_op && (info_bus[`alu_info_srl] || info_bus[`alu_info_sra]);
// wire alu_req_alu_shift_left = alu_op && (info_bus[`alu_info_sll]);
// wire alu_req_alu_shift = alu_req_alu_shift_left | alu_req_alu_shift_right;
wire alu_req_alu_sll = alu_op && (info_bus[`alu_info_sll]);
wire alu_req_alu_srl = alu_op && (info_bus[`alu_info_srl]);
wire alu_req_alu_sra = alu_op && (info_bus[`alu_info_sra]);
wire alu_req_alu_xor = alu_op && (info_bus[`alu_info_xor]);
wire alu_req_alu_and = alu_op && (info_bus[`alu_info_and]);
wire alu_req_alu_or = alu_op && (info_bus[`alu_info_or]);
wire alu_req_alu_op2imm = alu_op && (info_bus[`alu_info_op2imm]);
wire alu_req_alu_op1pc = alu_op && (info_bus[`alu_info_op1pc]);
wire [31:0] alu_req_alu_op1 = alu_req_alu_op1pc ? i_pc : i_rs1;
wire [31:0] alu_req_alu_op2 = alu_req_alu_op2imm ? i_imm : i_rs2;


wire agu_req_alu_add  = agu_op;
// wire agu_req_alu_op2imm = agu_op && ( info_bus[`agu_info_op2imm]);
wire agu_req_alu_op1 = i_rs1;
wire agu_req_alu_op2 = i_imm;


wire [31:0]bjp_req_alu_add_op1,bjp_req_alu_add_op2,bjp_req_alu_xor_op1,bjp_req_alu_xor_op2;





wire [31:0] res_logic, res_addsub, res_shift;
exu_bjp bjp_inst(
                .i_info_bus(info_bus),
                .i_bjp_op(bjp_op),
                .i_predict_flag(i_predict_flag),
                .o_pipe_flush(pipe_flush),
                .o_bjp_req_alu_xor(bjp_req_alu_xor),
                .o_bjp_req_alu_add(bjp_req_alu_add),
                .o_op1_add(bjp_req_alu_add_op1),
                .o_op2_add(bjp_req_alu_add_op2),
                .o_op1_xor(bjp_req_alu_xor_op1),
                .o_op2_xor(bjp_req_alu_xor_op2),
                .i_imm(i_imm),
                .i_rs1(i_rs1),
                .i_rs2(i_rs2),
                .i_pc(i_pc),
                .o_pc(o_exu_ifu_pc),
                .i_alu_add_res(res_addsub),
                .i_alu_xor_res(res_logic)
);



wire alu_addsub = alu_req_alu_addsub | agu_req_alu_add | bjp_op & bjp_req_alu_add;
wire alu_sub = alu_req_alu_sub;
wire alu_xor = alu_req_alu_xor | bjp_op & bjp_req_alu_xor;
wire alu_and = alu_req_alu_and;
wire alu_or = alu_req_alu_or;
wire alu_logic = alu_req_alu_and | alu_req_alu_or | alu_req_alu_xor;
wire alu_shift = alu_req_alu_sll | alu_req_alu_sra | alu_req_alu_srl;


wire [31:0] alu_addsub_op1 = ({32{alu_op & alu_req_alu_addsub}} & alu_req_alu_op1) | ({32{agu_op & agu_req_alu_add}} & agu_req_alu_op1) | ({32{bjp_req_alu_add & bjp_op}} & bjp_req_alu_add_op1);
wire [31:0] alu_addsub_op2 = ({32{alu_op & alu_req_alu_addsub}} & alu_req_alu_op2) | ({32{agu_op & agu_req_alu_add}} & agu_req_alu_op2) | ({32{bjp_req_alu_add & bjp_op}} & bjp_req_alu_add_op2);

wire [31:0] alu_logic_op1 = ({32{alu_op}} & alu_req_alu_op1) | ({32{bjp_op & bjp_req_alu_xor}} & bjp_req_alu_xor_op1);
wire [31:0] alu_logic_op2 = ({32{alu_op}} & alu_req_alu_op2) | ({32{bjp_op & bjp_req_alu_xor}} & bjp_req_alu_xor_op2);

wire [31:0] alu_shift_op1 = alu_op & alu_req_alu_op1;
wire [31:0] alu_shift_op2 = alu_op & alu_req_alu_op2;

dpath dpath_inst(
             .i_addsub_op1(alu_addsub_op1),
             .i_addsub_op2(alu_addsub_op2),
             .i_logic_op1(alu_logic_op1),
             .i_logic_op2(alu_logic_op2),
             .i_shift_op1(alu_shift_op1),
             .i_shift_op2(alu_shift_op2),
             .req_add(alu_addsub),
             .req_sub(alu_sub),
             .req_sll(alu_req_alu_sll),
             .req_sra(alu_req_alu_sra),
             .req_srl(alu_req_alu_srl),
             .req_xor(alu_xor),
             .req_or(alu_or),
             .req_and(alu_and),
             .res_logic(res_logic),
             .res_addsub(res_addsub),
             .res_shift(res_shift)
);
// assign o_rd = {32{alu_addsub}} & res_addsub |
//                 {32{alu_logic}} & res_logic |
//                 {32{alu_shift}} & res_shift ;

assign o_rd = {32{alu_op}} & (res_addsub | res_logic | res_shift);


endmodule