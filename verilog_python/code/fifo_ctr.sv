module fifo_ctr(
                input wire clk_wr,
                input wire clk_rd,
                input wire rst_n,
                input wire w_valid,
                input wire r_valid,
                input wire [`data_width-1:0] w_data,
                output reg [`data_width-1:0] r_data,
                output reg full,
                output reg empty);
// wire clk_wr,clk_rd,rst_n;
reg [15:0] i;
// wire [`data_width-1:0] w_data;
// reg [`data_width-1:0] r_data;
// wire full,empty,nearly_full,nerly_empty;
// wire wr_valid_inner,rd_valid_inner;
reg [`ram_addr_width:0] wr_ptr_gray,wr_ptr_gray_r,wr_ptr_gray_rr;
reg [`ram_addr_width:0] rd_ptr_gray,rd_ptr_gray_r,rd_ptr_gray_rr;
// reg full_r,empty_r;
reg [`ram_addr_width-1:0]wr_ptr_sync,rd_ptr_sync;
reg [`ram_addr_width-1:0]wr_ptr;
reg [`ram_addr_width-1:0]rd_ptr;
always@(posedge clk_wr or negedge rst_n)
begin
    if(!rst_n)
    begin
        wr_ptr <= 0;
        wr_ptr_gray <= 0;
    end
    else if(w_valid && !full)
    begin
        wr_ptr <= wr_ptr + 1;
        wr_ptr_gray <= ((wr_ptr + 1) >> 1) ^ (wr_ptr + 1);
    end
end

always@(posedge clk_rd or negedge rst_n)
begin
    if(!rst_n)
    begin
        rd_ptr <= 0;
        rd_ptr_gray <= 0;
    end
    else if(r_valid && !empty)
    begin
        rd_ptr <= rd_ptr + 1;
        rd_ptr_gray <= ((rd_ptr + 1) >> 1) ^ (rd_ptr + 1);
    end
end


always@(posedge clk_wr or negedge rst_n)
begin
    if(!rst_n)
    begin
        rd_ptr_gray_r <=0;
        rd_ptr_gray_rr <=0;
    end
    else
    begin
        rd_ptr_gray_r <= rd_ptr_gray;
        rd_ptr_gray_rr <= rd_ptr_gray_r;
    end
end

always@(posedge clk_rd or negedge rst_n)
begin
    if(!rst_n)
    begin
        wr_ptr_gray_r <=0;
        wr_ptr_gray_rr <=0;
    end
    else
    begin
        wr_ptr_gray_r <= wr_ptr_gray;
        wr_ptr_gray_rr <= wr_ptr_gray_r;
    end
end
always@(wr_ptr_gray_rr)
begin
    for ( i = 0; i <`ram_addr_width ; i = i + 1)
        wr_ptr_sync[i] = ^(wr_ptr_gray_rr >> i);

end
always@(rd_ptr_gray_rr)
begin
    for ( i = 0; i <`ram_addr_width ; i = i + 1)
        rd_ptr_sync[i] = ^(rd_ptr_gray_rr >> i);

end
assign empty= ((wr_ptr_sync[(`ram_addr_width-2):0]==rd_ptr[(`ram_addr_width-2):0])&&(wr_ptr_sync[`ram_addr_width-1]==rd_ptr[`ram_addr_width-1]))?1:0;
assign full = ((rd_ptr_sync[(`ram_addr_width-2):0]==wr_ptr[(`ram_addr_width-2):0])&&(rd_ptr_sync[`ram_addr_width-1]!=wr_ptr[`ram_addr_width-1]))?1:0;
// assign nearly_empty= ((rd_ptr_sync[ram_addr_width-1:0]==rd_ptr_sync[ram_addr_width-1:0])&&(rd_ptr_sync[ram_addr_width]==wr_ptr_sync[ram_addr_width]))?1:0;
// assign nearly_full = ((rd_ptr_sync[ram_addr_width-1:0]==rd_ptr_sync[ram_addr_width-1:0])&&(rd_ptr_sync[ram_addr_width]!=w;_ptr_sync[ram_addr_width]))?1:0;
assign w_valid_inner = w_valid && !full;
assign r_valid_inner = r_valid && !empty;
fifo_ram fifo_ram_inst(
                    .clk_wr(clk_wr),
                    .clk_rd(clk_rd),
                    .wr_ptr(wr_ptr),
                    .rd_ptr(rd_ptr),
                    .wr_valid(w_valid_inner),
                    .rd_valid(r_valid_inner),
                    .w_data(w_data),
                    .r_data(r_data),
                    .rst_n_wr(rst_n),
                    .rst_n_rd(rst_n)

);
endmodule