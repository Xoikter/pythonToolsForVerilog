import re
str = "vfu_64b_wrap vfu_blk0(); \
	adsad #(.wd(1))\
	asdasd ( .adad(asds\
	d),\
	.asdasd());	vfu256_wrapper vfu256_wrapper(	\
	.clk(clk),\
	.rst_n({rst_n}),\
	.vfu_cmd_vld(vfu_cmd_vld_q),\
	.VFInst_valid(VFInst_valid),\
	.bd_add_vld(bd_add_vld),\
	.vfu_cmd(vfu_cmd_q),\
	.vfu_cmd_dec(vfu_op_q),\
	.vfu_instr(vfu_instr_q),\
	.shift_imm_op(shift_imm_op),\
	.shift_shl(shift_shl),\
	.shift_cylic(shift_cylic),\
	.shift_op_vld(shift_op_vld),		\
	.vfu_res_byp(vfu_res_byp_q),\
	.vfu_src1(vfu_src1_q),\
	.vfu_src2(vfu_src2_q),\
	.vfu_src3(vfu_src3_q),\
	.vfu_src4(vec_r7),\
	.ml(cmd2_ml_q),\
	.vfu_res(vfu_res_w),\
	.vfu_res_misc({vfu_src4[32], vfu_src4[0]}),\
	.vfu_update_vd1_vld({vfu_instr[`GMEC_VPE_CMD2_FQ_REGION], vfu_instr[`GMEC_VPE_CMD2_IQ_REGION]}),\
		.vfu_update_vd2_vld(vfu_update_vd2_vld_w),\
	.vfu_vd1(vfu_vd1_w),\
	.vfu_vd2(vfu_vd2_w),\
	.vfu_byp_src1(vfu_byp_src1),\
	.vfu_byp_src2(vfu_byp_src2),\
	.vfu_free(vfu_free),\
	.vfu_exception(vfu_exception),\
	.vfu_result_cnflt(vfu_result_cnflt)\
);\
el233 if32();\
vfu_64b_wrap vfu_blk0 (\
  .clk(clk),\
  .rst_n(rst_n),  \
  .bdadd_flag(bd_add_vld),\
  .vec_src1(vec_src1[63:0]),\
  .vec_src2(vec_src2[63:0]),\
  .vec_src3(vec_src3[63:0]),  \
  .randround_bits({vfu_src4[32], vfu_src4[0]}),\
	.vfu_op(vfu_op),	\
	.vfu_op_dec(vfu_cmd_dec),\
	.vfu_imm(vfu_imm),\
	.Width_operand_cell0(vfu_instr[`GMEC_VPE_CMD2_ISZ_REGION]),\
	.AUX_RUD_cell0(vfu_instr[`GMEC_VPE_CMD2_FRND_REGION]),\
	.AUX_SAT_cell0({vfu_instr[`GMEC_VPE_CMD2_FQ_REGION], vfu_instr[`GMEC_VPE_CMD2_IQ_REGION]}),\
	.VFInst_valid_cell0(VFInst_valid),\
	.VFInst_valid_cell1(VFInst_valid),	\
	.idt(vfu_instr[`GMEC_VPE_CMD2_IDT_REGION]),\
	.irnd(vfu_instr[`GMEC_VPE_CMD2_IR_REGION]),\
	.VXADD(special_add_op_vld),\
	.VXADDOP(special_add_sub_opcode),\
	.shift_imm_op(shift_imm_op),\
	.shift_shl(shift_shl),\
	.shift_cylic(shift_cylic),\
	.shift_op_vld(shift_op_vld),	\
	.vec_result_vld(vec_result_vld_blk0),\
	.vec_result(vec_result_blk0),\
	.vec_carry_o(vec_carry_o_blk0),\
	.vec_exception(vec_exception0),\
	.vec_result_cnflt(vec_result_cnflt0)\
);\
\
"

# result = re.findall('(?:;|end|endfunction|endtask|endclass|endinterface|endmodule)\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(\(.*?\))?\s*;', str,flags=re.S)
# a = 0 

# (?:#\( (?:.\(\s*(?:\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)   ) ) \)


str1 = "\s*\((?:\s*\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\([^\(\)]*?\)\s*,)*\s*(?:\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\([^\(\)]*?\)\s*)\s*\)\s*"
str2 = "\s*\((?:[^\(\)]*?\s*,)*[^\(\)]*?\)\s*"
# str2 = "\((?:(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*),)*(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\)"
str3 = "\s*(?:\s*#\s*(?:"+str1 +"|" + str2 + "))?\s*"
str4 = "\s*(?:"+str1 +"|" + str2 + ")\s*;"
str5 = "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str3 + "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str4
result = re.findall(str5, str,flags=re.S)


str1 = "\((?:\s*\.(?:\s*\b[a-zA-Z_][a-zA-Z0-9_$]*\b\s*)\s*\(.*?\)\s*,)*\s*(?:\.(?:\s*\b[a-zA-Z_][a-zA-Z0-9_$]*\b\s*)\s*\(.*?\)\s*)\s*\)"