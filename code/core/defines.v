`define INSTR_WIDTH  32
`define RFIDX_WIDTH  5
`define ADDR_WIDTH 32
`define PC_WIDTH 32
`define INSTR_SIZE 32
`define INSTR_ICR 4
`define ALU_INFO_BUS_WIDTH 15
`define alu_info_add 3
`define alu_info_sub 4
`define alu_info_sll 5
`define alu_info_slt 6
`define alu_info_sltu 7
`define alu_info_xor 8
`define alu_info_srl 9
`define alu_info_sra 10
`define alu_info_and 11
`define alu_info_or 12
`define alu_info_op2imm 13
`define alu_info_op1pc 14
`define info_bus_grp  2:0
`define decode_alu_grp 3'b000
`define decode_agu_grp 3'b001
`define decode_bjp_grp 3'b010


`define INSTR_NOP 32'b0000000_00000_00000_000_00000_0110011

// `define alu_info_addi 10
// `define alu_info_subi 11
// `define alu_info_slli 12
// `define alu_info_slti 13
// `define alu_info_sltui 14
// `define alu_info_xori 15
// `define alu_info_srli 16
// `define alu_info_srai 17
// `define alu_info_andi 18
// `define alu_info_ori 19
`define DEC_INFO_BUS_WIDTH 15


`define AGU_INFO_BUS_WIDTH 11
`define agu_info_lb  3
`define agu_info_lh  4
`define agu_info_lw  5
`define agu_info_lbu  6
`define agu_info_lhu  7
`define agu_info_sb  8
`define agu_info_sh  9
`define agu_info_sw  10

`define BJP_INFO_BUS_WIDTH 9
`define bjp_info_beq 3
`define bjp_info_bne 4
`define bjp_info_blt 5
`define bjp_info_bge 6
`define bjp_info_bltu 7
`define bjp_info_bgeu 8


`define X0 0
