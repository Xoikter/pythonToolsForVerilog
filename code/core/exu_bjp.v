module exu_bjp(
                input [`DEC_INFO_BUS_WIDTH - 1 : 0] i_info_bus,
                input  i_predict_flag,
                output o_pipe_flush,
                output o_bjp_req_alu_add,
                output o_bjp_req_alu_xor,
                output [31:0]o_op1_add,
                output [31:0]o_op2_add,
                output [31:0]o_op1_xor,
                output [31:0]o_op2_xor,
                input  [31:0] i_imm,
                input  [31:0] i_rs1,
                input i_bjp_op,
                input  [31:0] i_rs2,
                input  [31:0] i_alu_add_res,
                input  [31:0] i_alu_xor_res,
                input  [`PC_WIDTH - 1 : 0] i_pc,
                output [`PC_WIDTH - 1 : 0] o_pc
);

wire [`DEC_INFO_BUS_WIDTH - 1 : 0] info_bus = i_info_bus;
wire bjp_op = i_bjp_op;
wire [31:0] rs1 = i_rs1;
wire [31:0] rs2 = i_rs2;
wire bge  = bjp_op & info_bus[`bjp_info_bge];
wire bne  = bjp_op & info_bus[`bjp_info_bne];
wire blt  = bjp_op & info_bus[`bjp_info_blt];
wire beq  = bjp_op & info_bus[`bjp_info_beq];
wire bltu = bjp_op & info_bus[`bjp_info_bltu];
wire bgeu = bjp_op & info_bus[`bjp_info_bgeu];

wire [31:0] op1,op2;
assign res_bltbge = (blt | bge) & ($signed(op1) < $signed(op2));
assign res_bltubgeu = (bltu | bgeu) & ( op1 <  op2); 
assign res_beq = beq & ~(|i_alu_xor_res);
assign res_bne = bne &  (|i_alu_xor_res);

assign op1 = ({32{blt | bltu}} & rs1) | ({32{bge | bgeu}} & rs2);
assign op2 = ({32{blt | bltu}} & {rs2}) | ({32{bge | bgeu}} & rs1);
wire branch_op = bjp_op  && (res_bltbge | res_bltubgeu | res_beq | res_bne);
wire  predict_wrong =bjp_op  && ((res_bltbge | res_bltubgeu | res_beq | res_bne)^ i_predict_flag);

assign o_bjp_req_alu_add = predict_wrong;
assign o_op1_add = i_pc;
assign o_op2_add = branch_op ? i_imm : 32'h4;

assign o_bjp_req_alu_xor = beq | bne;
assign o_op1_xor = rs1;
assign o_op2_xor = rs2;
assign o_pc = {32{bjp_op}} & i_alu_add_res;
assign o_pipe_flush = predict_wrong;
endmodule