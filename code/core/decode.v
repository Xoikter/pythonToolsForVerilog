// `include "defines.v"
module decode(
                        input [`INSTR_SIZE-1:0] instr,
                        output dec_rs1en,
                        output dec_rs2en,
                        output dec_rden,
                        output [`RFIDX_WIDTH-1:0] dec_rs1idx,
                        output [`RFIDX_WIDTH-1:0] dec_rdidx,
                        output [`RFIDX_WIDTH-1:0] dec_rs2idx,
                        // output dec_rv32,
                        output dec_bjp,
                        output dec_jal,
                        output dec_jalr,
                        // output dec_bjpu,
                        // output [11:0] imm_12,
                        // output [19:0] imm_20,
                        output [31:0] dec_imm,
                        // output add,
                        // output sub,
                        // output sll,
                        // output slt,
                        output [`DEC_INFO_BUS_WIDTH - 1 : 0] dec_info_bus
                        // output [`ALU_INFO_BUS_WIDTH - 1 : 0] alu_info_bus,
                        // output [`BJP_INFO_BUS_WIDTH - 1 : 0] bjp_info_bus
                        // output dec_bxx
                        // output [`RFIDX_WIDTH-1:0] dec_jalr_rs1idx,
                        // output [`XLEN-1:0] 
                        );

wire [6:0] op_code = instr[6:0];
assign dec_jal  = (op_code == 7'b1101111);
assign dec_bjp  = (op_code == 7'b1100011);
assign dec_jalr = (op_code == 7'b1100111);
wire   dec_r    = (op_code == 7'b0110011);
wire   dec_ri   = (op_code == 7'b0010011);
wire   dec_lui  = (op_code == 7'b0110111);
wire   dec_auipc = (op_code == 7'b0010111);
wire   dec_agu_load = (op_code == 7'b0000011);
wire   dec_agu_store = (op_code == 7'b0100011);
wire [2:0] func3_code = instr[14:12];
wire [6:0] func7_code = instr[31:25];
wire [`ALU_INFO_BUS_WIDTH - 1 : 0] alu_info_bus;
wire [`AGU_INFO_BUS_WIDTH - 1 : 0] agu_info_bus;
wire [`BJP_INFO_BUS_WIDTH - 1 : 0] bjp_info_bus;
// wire [`DEC_INFO_BUS_WIDTH - 1 : 0] dec_info_bus;
// wire dec_bjp = 
assign dec_rs1idx = instr[19:15];
assign dec_rs2idx = instr[24:20];
assign dec_rdidx  = instr[11:7];
// assign dec_rs1en = (dec_bjp || dec_jalr || dec_r || dec_ri) && (dec_rs1idx != `X0);
// assign dec_rs2en = (dec_bjp || dec_r) && (dec_rs2idx != `X0);
assign dec_rs1en = (dec_bjp || dec_jalr || dec_r || dec_ri) ;
assign dec_rs2en = (dec_bjp || dec_r);
assign dec_rden = (dec_jal | dec_jalr | dec_lui | dec_auipc | dec_agu_load | dec_r | dec_ri ) && (dec_rdidx != `X0);
wire [12:0] imm_B = {instr[31],instr[7],instr[30:25],instr[11:8],1'b0};
wire [11:0] imm_I = instr[31:20];
wire [20:0] imm_J = {instr[31],instr[19:12],instr[20],instr[30:21],1'b0};
wire [19:0] imm_U = instr[31:12];
wire [11:0] imm_S = {instr[31:25],instr[11:7]};
wire [4:0]  imm_shamt = instr[24:20];
// assign imm_12 = dec_bjp ? imm_B : imm_I;
// assign imm_20 = dec_jal ? imm_J : imm_U;
wire dec_add = dec_r && (func3_code == 3'b000) && (func7_code == 7'b0000000);
wire dec_sub = dec_r && (func3_code == 3'b000) && (func7_code == 7'b0000001);
wire dec_sll = dec_r && (func3_code == 3'b001) && (func7_code == 7'b0000000);
wire dec_slt = dec_r && (func3_code == 3'b010) && (func7_code == 7'b0000000);
wire dec_sltu = dec_r && (func3_code == 3'b011) && (func7_code == 7'b0000000);
wire dec_xor = dec_r && (func3_code == 3'b100) && (func7_code == 7'b0000000);
wire dec_srl = dec_r && (func3_code == 3'b101) && (func7_code == 7'b0000000);
wire dec_sra = dec_r && (func3_code == 3'b101) && (func7_code == 7'b0100000);
wire dec_and = dec_r && (func3_code == 3'b110) && (func7_code == 7'b0000000);
wire dec_or  = dec_r && (func3_code == 3'b111) && (func7_code == 7'b0000000);
wire dec_addi = dec_ri && (func3_code == 3'b000);
wire dec_slti = dec_ri && (func3_code == 3'b010);
wire dec_sltiu = dec_ri && (func3_code == 3'b011);
wire dec_xori = dec_ri && (func3_code == 3'b100);
wire dec_ori = dec_ri && (func3_code == 3'b110);
wire dec_andi = dec_ri && (func3_code == 3'b111);
wire dec_slli = dec_ri && (func3_code == 3'b001) && (func7_code == 7'b0000000);
wire dec_srli = dec_ri && (func3_code == 3'b101) && (func7_code == 7'b0000000);
wire dec_srai = dec_ri && (func3_code == 3'b101) && (func7_code == 7'b0100000);
assign alu_info_bus[`info_bus_grp] = `decode_alu_grp;
assign alu_info_bus[`alu_info_add] = dec_add | dec_addi | dec_auipc;
assign alu_info_bus[`alu_info_sub] = dec_sub;
assign alu_info_bus[`alu_info_sll] = dec_sll | dec_slli;
assign alu_info_bus[`alu_info_slt] = dec_slt | dec_slti;
assign alu_info_bus[`alu_info_sltu] = dec_sltu | dec_sltiu;
assign alu_info_bus[`alu_info_xor] = dec_xor | dec_xori;
assign alu_info_bus[`alu_info_srl] = dec_srl | dec_srli;
assign alu_info_bus[`alu_info_sra] = dec_sra | dec_srai;
assign alu_info_bus[`alu_info_and] = dec_and | dec_andi;
assign aluu_info_bus[`alu_info_op2imm] = dec_addi  | dec_slti  | dec_sltiu | dec_xori  | dec_ori | dec_andi  | dec_slli  | dec_srli  | dec_srai;
assign alu_in_info_bus[`alu_info_or] = dec_or | dec_ori;
// assign alfo_bus[`alu_info_op2imm] = dec_ri | dec_auipc | dec_lui;
assign alu_info_bus[`alu_info_op1pc] = dec_auipc;
wire dec_lb = dec_agu_load && (func3_code == 3'b000);
wire dec_lh = dec_agu_load && (func3_code == 3'b001);
wire dec_lw = dec_agu_load && (func3_code == 3'b010);
wire dec_lbu = dec_agu_load && (func3_code == 3'b100);
wire dec_lhu = dec_agu_load && (func3_code == 3'b101);
wire dec_sb = dec_agu_store && (func3_code == 3'b000);
wire dec_sh = dec_agu_store && (func3_code == 3'b001);
wire dec_sw = dec_agu_store && (func3_code == 3'b010);
assign agu_info_bus[`info_bus_grp] = `decode_agu_grp;
assign agu_info_bus[`agu_info_lb] = dec_lb;
assign agu_info_bus[`agu_info_lh] = dec_lh;
assign agu_info_bus[`agu_info_lw] = dec_lw;
assign agu_info_bus[`agu_info_lbu] = dec_lbu;
assign agu_info_bus[`agu_info_lhu] = dec_lhu;
assign agu_info_bus[`agu_info_sb] = dec_sb;
assign agu_info_bus[`agu_info_sh] = dec_sh;
assign agu_info_bus[`agu_info_sw] = dec_sw;
// assign dec_info_bus[`alu_info_region] = alu_info_bus;
// assign dec_info_bus[`agu_info_region] = agu_info_bus;
// assign dec_info_bus[`bjp_info_region] = bjp_info_bus;
assign bjp_info_bus[`info_bus_grp] = `decode_bjp_grp;
wire dec_beq = dec_bjp && (func3_code == 3'b000);
wire dec_bne = dec_bjp && (func3_code == 3'b001);
wire dec_blt = dec_bjp && (func3_code == 3'b100);
wire dec_bge = dec_bjp && (func3_code == 3'b101);
wire dec_bltu = dec_bjp && (func3_code == 3'b110);
wire dec_bgeu = dec_bjp && (func3_code == 3'b111);
assign bjp_info_bus[`bjp_info_beq] = dec_beq;
assign bjp_info_bus[`bjp_info_bne] = dec_bne;
assign bjp_info_bus[`bjp_info_blt] = dec_blt;
assign bjp_info_bus[`bjp_info_bge] = dec_bge;
assign bjp_info_bus[`bjp_info_bltu] = dec_bltu;
assign bjp_info_bus[`bjp_info_bgeu] = dec_bgeu;

wire alu_sel = dec_r | dec_ri | dec_auipc | dec_lui;
wire agu_sel = dec_agu_load | dec_agu_store;
wire bjp_sel = dec_bjp;
assign dec_info_bus = ({`DEC_INFO_BUS_WIDTH{alu_sel}} & {{(`DEC_INFO_BUS_WIDTH - `ALU_INFO_BUS_WIDTH){1'b0}},alu_info_bus}) |
                        ({`DEC_INFO_BUS_WIDTH{agu_sel}} & {{(`DEC_INFO_BUS_WIDTH - `AGU_INFO_BUS_WIDTH){1'b0}},agu_info_bus}) |
                        ({`DEC_INFO_BUS_WIDTH{bjp_sel}} & {{(`DEC_INFO_BUS_WIDTH - `BJP_INFO_BUS_WIDTH){1'b0}},bjp_info_bus}) ;


// assign dec_imm = /*(dec_addi | dec_slti | dec_xori | dec_ori | dec_addi) ? {20imm_I[12] , imm_I} :*/
//             (dec_sltiu | dec_lbu | dec_lhu) ?  {20'b0 , imm_I} :
//             (dec_slli | dec_srli | dec_srai) ? {27'b0 , imm_shamt} :
//             (dec_agu_load | dec_ri | dec_jlar) ? { 20{imm_I[12]} , imm_I} :
//             (dec_agu_store) ? {20{imm_S[12]} , imm_S} :
//             (dec_bltu | dec_bgeu) ? {19'b0 , imm_B} :
//             (dec_bjp) ? {19{imm_B[12]} , imm_B} :
//             (dec_jal) ? {11{imm_J[20]},imm_J} :
//             {32(dec_auipc || dec_lui)} & {imm_U , 12'b0} ;
assign dec_imm =    (dec_sll | dec_slli | dec_srai) ? {27'b0 , imm_shamt} :
                    (dec_ri | dec_agu_load | dec_jalr) ? { {20{imm_I[11]}} , imm_I} :
                    (dec_bjp) ? {{19{imm_B[12]}} , imm_B} :
                    (dec_agu_store) ? {{20{imm_S[11]}} , imm_S} :
                    (dec_jal) ? {{11{imm_J[20]}},imm_J} :
                    {32{(dec_auipc || dec_lui)}} & {imm_U , 12'b0} ;

























endmodule