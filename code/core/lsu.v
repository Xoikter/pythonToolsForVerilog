module lsu(
            input clk,
            input rst_n,
            //exu_interface
            input [`ADDR_WIDTH - 1 : 0] addr,
            input addr_vld,
            output lsu_wready,
            output lsu_rready,
            input lsu_wr,
            input [31:0] i_data,
            output [31:0] o_data,
            input i_datavld,
            output o_datavld,


            //axi_interface
            output reg [`ADDR_WIDTH - 1 : 0] awaddr,
            output reg awvalid,
            output [7:0] awlen,
            output [2:0] awsize,
            output [1:0] awburst,
            input  awready,

            output reg [31:0] wdata,
            output reg wvalid,
            output wlast,
            input  wready,

            input [1:0] bresp,
            input bvalid,
            output bready,

            output [`ADDR_WIDTH - 1 : 0] araddr,
            output arvalid,
            output [7:0] arlen,
            output [2:0] arsize,
            output [1:0] arburst,
            input  arready,

            input [31:0] rdata,
            input rlast,
            input rvalid,
            output rready);
            




assign awlen = 0;
assign arlen = 0;
assign awsize = 3'b010;
assign arsize = 3'b010;
assign awburst = 2'b01;
assign arburst = 2'b01;
assign bready = 1;
assign rready = 1;

//write address channel
always@(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            awvalid <= 0;
            awaddr <= 0;
        end
        else if(addr_vld && lsu_wready && lsu_wr ) begin
            awvalid <= 1;
            awaddr <= addr;
        end   
        else if(awvalid && awready) begin
            awvalid <= 0;
        end
        else 
            awvalid <= awvalid;
end

always@(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            wvalid <= 0;
            wdata <= 0;
            wlast <= 0;
        end
        else if(lsu_wready && lsu_wr && i_datavld) begin
            wvalid <= 1;
            wdata <= i_data;
            wlast <= 1;
        end   
        else if(awvalid && awready) begin
            wvalid <= 0;
            wdata <= 0;
        end
        else begin
            wvalid <= wvalid;
            wdata <= wdata;
        end
end

always@(posedge clk or negedge rst_n) begin
    if(~rst_n) begin
        rvalid <= 0;
        raddr <= 0;
    end
    else if(addr_vld && lsu_rready && ~lsu_wr) begin
        rvalid <= 1;
        raddr <= addr;
    end
    else if(rvalid && rready) begin
        rvalid <= 0;
        raddr <= 0;
    end
    else begin
        rvalid <= rvalid;
        raddr <= raddr;
    end
end

assign bready = 1'b1;
// assign awvalid = addr_vld & lsu_wr;
// assign awaddr = addr;
// assign lsu_wready = awready;
// assign lsu_rready = arready;


//write date channel
assign wvalid = addr_vld & lsu_wr;
assign wdata = i_data;
assign wlast = wvalid;


//
