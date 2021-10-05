module dpath(
            input [31:0] i_addsub_op1,
            input [31:0] i_addsub_op2,
            input [31:0] i_logic_op1,
            input [31:0] i_logic_op2,
            input [31:0] i_shift_op1,
            input [31:0] i_shift_op2,
            input req_add,
            input req_sub,
            input req_sll,
            input req_sra,
            input req_srl,
            input req_xor,
            input req_or,
            input req_and,
            output [31:0] res_logic,
            output [31:0] res_addsub,
            output [31:0] res_shift
);



wire req_addsub = req_add | req_sub;
wire [31:0] addsub_op1 = i_addsub_op1;
wire [31:0] addsub_op2 = req_sub ? ~i_addsub_op2 : i_addsub_op2;
assign res_addsub = addsub_op1 + addsub_op2 + req_sub;
wire [31:0] shift_right_op1 = {
    i_shift_op1[0],i_shift_op1[1],i_shift_op1[2],i_shift_op1[3],i_shift_op1[4],i_shift_op1[5],i_shift_op1[6],i_shift_op1[7],
    i_shift_op1[8],i_shift_op1[9],i_shift_op1[10],i_shift_op1[11],i_shift_op1[12],i_shift_op1[13],i_shift_op1[14],i_shift_op1[15],
    i_shift_op1[16],i_shift_op1[17],i_shift_op1[18],i_shift_op1[19],i_shift_op1[20],i_shift_op1[21],i_shift_op1[22],i_shift_op1[23],
    i_shift_op1[24],i_shift_op1[25],i_shift_op1[26],i_shift_op1[27],i_shift_op1[28],i_shift_op1[29],i_shift_op1[30],i_shift_op1[31]
};
wire [31:0] shift_op2 = i_shift_op2;
wire [31:0] shift_op1 = (req_sra | req_srl) ? shift_right_op1 : i_shift_op1;
wire [31:0] res_shift_temp = shift_op1 << shift_op2;
wire [31:0] res_sll = res_shift_temp;
wire [31:0] res_srl = {
    res_shift_temp[0],res_shift_temp[1],res_shift_temp[2],res_shift_temp[3],res_shift_temp[4],res_shift_temp[5],res_shift_temp[6],res_shift_temp[7],
    res_shift_temp[8],res_shift_temp[9],res_shift_temp[10],res_shift_temp[11],res_shift_temp[12],res_shift_temp[13],res_shift_temp[14],res_shift_temp[15],
    res_shift_temp[16],res_shift_temp[17],res_shift_temp[18],res_shift_temp[19],res_shift_temp[20],res_shift_temp[21],res_shift_temp[22],res_shift_temp[23],
    res_shift_temp[24],res_shift_temp[25],res_shift_temp[26],res_shift_temp[27],res_shift_temp[28],res_shift_temp[29],res_shift_temp[30],res_shift_temp[31]
};
wire [31:0] mask_rsa = {32{1'b1}} >> i_shift_op2;

wire [31:0] res_rsa = ({32{i_shift_op1[31]}} & ~mask_rsa) | (res_shift_temp & mask_rsa);
assign res_shift = req_sll ? res_sll : req_srl ? res_srl : res_rsa;

wire [31:0] res_xor = i_logic_op1 ^ i_logic_op2;
wire [31:0] res_or = i_logic_op1 | i_logic_op2;
wire [31:0] res_and = i_logic_op1 & i_logic_op2;
assign res_logic = req_or ? res_or : req_xor ? res_xor : res_and;




endmodule
























