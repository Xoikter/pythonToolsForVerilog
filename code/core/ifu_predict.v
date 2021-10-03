module ifu_predict (
    input wire dec_bjp,
    input wire dec_jal,
    input wire dec_jalr,
    input wire [31:0] dec_imm,
    output wire pre_flag
);

// wire branch_op = dec_bjp | dec_jal | dec_jalr;
// assign pre_flag = (branch_op && ~dec_imm[31]) ? 1'b1 : 1'b0;
assign pre_flag = (dec_jal | dec_jalr) ? 1'b1 : (dec_bjp && dec_imm[31]) ? 1'b1 : 1'b0;
endmodule



