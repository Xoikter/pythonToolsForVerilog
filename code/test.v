module test(
        input clk,
        // output reg vld,
        input [3:0] a,
        input [3:0] b,
        output [4:0]c
);
       assign  c = a + b;
//        always @(posedge clk) begin
//               vld <= 1; 
//        end
endmodule
