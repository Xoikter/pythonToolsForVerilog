module test(
        // input clk,
        // input vld,
        input clk,
        input rst_n,
        input in_valid,
        output in_ready,
        input [7:0] in_data,
        input out_ready,
        output out_valid,
        output [7:0] out_data
);
       always @(posedge clk or negedge rst_n) begin
                if( ~rst_n) begin
                        out_data <= 0;
                end
                if( in_valid && in_ready)
                        out_data <= ~in_data + 5;

       end
endmodule
