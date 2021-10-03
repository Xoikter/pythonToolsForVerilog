module ram(
        input clk,
        input rst_n,
        input [`PC_WIDTH - 1 : 0] pc,
        input pc_vld,
        output reg [`INSTR_WIDTH - 1 : 0]instr
);

reg [31:0] INSTR [255:0];

`ifdef DEBUG
initial begin
   $readmemb("/mnt/hgfs/xsc/pro/git_pro/RTL_PRO/RISC_V/sim/instr.txt",INSTR);
end
`endif

always@(posedge clk or negedge rst_n) begin
    if(!rst_n)
    instr <= 0;
    else if(pc_vld)
    instr <= INSTR[pc/4];
end


endmodule