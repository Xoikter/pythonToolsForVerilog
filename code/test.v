module test(
        // input clk,
        // input vld,
        input [3:0] a,
        input [3:0] b,
        output [4:0]c,
        output l,
        input as
);
       assign  c = a + b;
//        always @(posedge clk) begin
//               vld <= 1; 
//        end
endmodule
