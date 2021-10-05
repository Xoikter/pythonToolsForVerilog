module pre_fetch(
    input wire clk,
    input wire rst_n,
    input wire pc_vld,
    input wire [`PC_WIDTH-1:0] pc,
    output reg [`INSTR_WIDTH-1:0] pre_instr
    // input wire [`INSTR_WIDTH-1:0] instr_rom
);


reg [`INSTR_WIDTH-1:0] instr_rom [`INSTR_LENTH-1:0];
always@(posedge clk or negedge rst_n) begin
    if(~rst_n) begin
        pre_instr <= 0;
    end
    else if(pc_vld) begin
        pre_instr <= instr_rom[pc];
end
    end
`ifdef DUBUG
initial begin
    $readmemh("./instr.txt",instr_rom);
end
`endif

endmodule