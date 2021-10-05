// `include "defines.v"

module ifu(
            input clk,
            input rst_n,
            //mem interface
            output pc_vld,
            input wire [`INSTR_WIDTH - 1: 0] pre_instr,
            output [`PC_WIDTH - 1 : 0] pc_ram,
            input [`PC_WIDTH - 1 : 0] exu_pc,
            output reg [`PC_WIDTH - 1 : 0] last_pc,
            output  [`INSTR_WIDTH - 1 : 0] instr_exu,
            input wire pipe_flush,
            input wire pipe_stall,
            output wire o_predict_flag
            );

reg [`PC_WIDTH - 1 : 0] pc;
wire [`PC_WIDTH - 1 : 0] pc_inner;
wire [`PC_WIDTH - 1 : 0] next_pc;
assign  pc_ram = pipe_flush ? exu_pc : pc;
// reg [`PC_WIDTH - 1 : 0] last_pc;
assign next_pc = pc_inner;
// wire [`INSTR_WIDTH - 1 : 0] instr_exu;
// reg [`INSTR_WIDTH - 1 : 0] instr;
always@(posedge clk or negedge rst_n) begin
    if(~rst_n) begin
        pc <= 0;
        last_pc <= 0;
    end
    // else if(~exu_flush) begin
        // pc <= next_pc;
        // last_pc <= pc;
    // end
    else begin
        pc <= next_pc;
        last_pc <= pc;
    end
end
wire [31:0] dec_imm;
wire dec_bjp,dec_jal,dec_jalr,pre_flag;
ifu_predict ifu_predict_inst(
                        .dec_bjp(dec_bjp),
                        .dec_jal(dec_jal),
                        .dec_jalr(dec_jalr),
                        .dec_imm(dec_imm),
                        .pre_flag(pre_flag)

);
decode ifu_decode(
                        .instr(pre_instr),
                        .dec_rs1en(),
                        .dec_rs2en(),
                        .dec_rs1idx(),
                        .dec_rs2idx(),
                        .dec_bjp(dec_bjp),
                        .dec_rden(),
                        .dec_rdidx(),
                        .dec_jal(dec_jal),
                        .dec_jalr(dec_jalr),
                        .dec_imm(dec_imm),
                        .dec_info_bus());

wire signed [`PC_WIDTH - 1 : 0] op_a;
wire signed [`PC_WIDTH - 1 : 0] op_b;
assign pc_inner = op_a + op_b;
// assign op_a = pipe_flush ? exu_pc : pc;
assign op_a = pipe_flush ? exu_pc : pc;
assign op_b = ~pre_flag ? 4 : dec_imm; 
assign pc_vld = 1;
assign instr_exu = (pipe_flush | pipe_stall) ? `INSTR_NOP : pre_instr;
// assign instr_i = ( pipe_stall) ? `INSTR_NOP : instr;

reg predict_flag_r;
assign o_predict_flag = predict_flag_r;
always@(posedge clk or negedge rst_n) begin
    if(!rst_n)
    predict_flag_r <= 0;
    else
    predict_flag_r <= pre_flag;
end

// always@(posedge clk or negedge rst_n) begin
//     if(~rst_n) begin
//         instr <= 0;
//     end
//     else begin
//         instr <= pre_instr;
//     end
// end















endmodule