module regfile(
            input clk,
            input rst_n,
            input i_rs1en,
            input i_rs2en,
            input [`RFIDX_WIDTH - 1 : 0] i_rs1idx,
            input [`RFIDX_WIDTH - 1 : 0] i_rs2idx,
            input [`RFIDX_WIDTH - 1 : 0] i_rdidx,
            input i_rden,
            output reg [31:0] o_rs1,
            output reg [31:0] o_rs2,
            input [31:0] i_rd
);
reg [31:0] regm [31:0];

`ifdef DEBUG
initial begin
    $vcdpluson();
end
always@(posedge clk) begin
    $vcdplusmemon(regm);
    
end
`endif

genvar i;
generate
    for(i = 1; i < 32 ; i = i + 1) begin:register
        always@(posedge clk or negedge rst_n) begin
            if(!rst_n)
                regm[i] <= 0;
            else if(i_rden && i_rdidx == i)
                regm[i] <= i_rd;
            else
                regm[i] <= regm[i];
        end
    end
endgenerate


always@(posedge clk or negedge rst_n) begin
    if(!rst_n)
    regm[0] <= 0;
    else
    regm[0] <= 0;
end



always@* begin
    if(i_rs1en) begin
        case(i_rs1idx)
            `RFIDX_WIDTH'd1: o_rs1 = regm[1];
            `RFIDX_WIDTH'd2: o_rs1 = regm[2];
            `RFIDX_WIDTH'd3: o_rs1 = regm[3];
            `RFIDX_WIDTH'd4: o_rs1 = regm[4];
            `RFIDX_WIDTH'd5: o_rs1 = regm[5];
            `RFIDX_WIDTH'd6: o_rs1 = regm[6];
            `RFIDX_WIDTH'd7: o_rs1 = regm[7];
            `RFIDX_WIDTH'd8: o_rs1 = regm[8];
            `RFIDX_WIDTH'd9: o_rs1 = regm[9];
            `RFIDX_WIDTH'd10: o_rs1 = regm[10];
            `RFIDX_WIDTH'd11: o_rs1 = regm[11];
            `RFIDX_WIDTH'd12: o_rs1 = regm[12];
            `RFIDX_WIDTH'd13: o_rs1 = regm[13];
            `RFIDX_WIDTH'd14: o_rs1 = regm[14];
            `RFIDX_WIDTH'd15: o_rs1 = regm[15];
            `RFIDX_WIDTH'd16: o_rs1 = regm[16];
            `RFIDX_WIDTH'd17: o_rs1 = regm[17];
            `RFIDX_WIDTH'd18: o_rs1 = regm[18];
            `RFIDX_WIDTH'd19: o_rs1 = regm[19];
            `RFIDX_WIDTH'd20: o_rs1 = regm[20];
            `RFIDX_WIDTH'd21: o_rs1 = regm[21];
            `RFIDX_WIDTH'd22: o_rs1 = regm[22];
            `RFIDX_WIDTH'd23: o_rs1 = regm[23];
            `RFIDX_WIDTH'd24: o_rs1 = regm[24];
            `RFIDX_WIDTH'd25: o_rs1 = regm[25];
            `RFIDX_WIDTH'd26: o_rs1 = regm[26];
            `RFIDX_WIDTH'd27: o_rs1 = regm[27];
            `RFIDX_WIDTH'd28: o_rs1 = regm[28];
            `RFIDX_WIDTH'd29: o_rs1 = regm[29];
            `RFIDX_WIDTH'd30: o_rs1 = regm[30];
            `RFIDX_WIDTH'd31: o_rs1 = regm[31];
            default: o_rs1 = 0;
        endcase
    end
    else
        o_rs1 = 0;
end
always@* begin
    if(i_rs2en) begin
        case(i_rs2idx)
            `RFIDX_WIDTH'd1: o_rs2 = regm[1];
            `RFIDX_WIDTH'd2: o_rs2 = regm[2];
            `RFIDX_WIDTH'd3: o_rs2 = regm[3];
            `RFIDX_WIDTH'd4: o_rs2 = regm[4];
            `RFIDX_WIDTH'd5: o_rs2 = regm[5];
            `RFIDX_WIDTH'd6: o_rs2 = regm[6];
            `RFIDX_WIDTH'd7: o_rs2 = regm[7];
            `RFIDX_WIDTH'd8: o_rs2 = regm[8];
            `RFIDX_WIDTH'd9: o_rs2 = regm[9];
            `RFIDX_WIDTH'd10: o_rs2 = regm[10];
            `RFIDX_WIDTH'd11: o_rs2 = regm[11];
            `RFIDX_WIDTH'd12: o_rs2 = regm[12];
            `RFIDX_WIDTH'd13: o_rs2 = regm[13];
            `RFIDX_WIDTH'd14: o_rs2 = regm[14];
            `RFIDX_WIDTH'd15: o_rs2 = regm[15];
            `RFIDX_WIDTH'd16: o_rs2 = regm[16];
            `RFIDX_WIDTH'd17: o_rs2 = regm[17];
            `RFIDX_WIDTH'd18: o_rs2 = regm[18];
            `RFIDX_WIDTH'd19: o_rs2 = regm[19];
            `RFIDX_WIDTH'd20: o_rs2 = regm[20];
            `RFIDX_WIDTH'd21: o_rs2 = regm[21];
            `RFIDX_WIDTH'd22: o_rs2 = regm[22];
            `RFIDX_WIDTH'd23: o_rs2 = regm[23];
            `RFIDX_WIDTH'd24: o_rs2 = regm[24];
            `RFIDX_WIDTH'd25: o_rs2 = regm[25];
            `RFIDX_WIDTH'd26: o_rs2 = regm[26];
            `RFIDX_WIDTH'd27: o_rs2 = regm[27];
            `RFIDX_WIDTH'd28: o_rs2 = regm[28];
            `RFIDX_WIDTH'd29: o_rs2 = regm[29];
            `RFIDX_WIDTH'd30: o_rs2 = regm[30];
            `RFIDX_WIDTH'd31: o_rs2 = regm[31];
            default: o_rs2 = 0;
        endcase
    end
    else
        o_rs2 = 0;
end
endmodule