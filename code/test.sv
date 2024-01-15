

module InvSubBytes(
	input	[0:127] din,
	output	[0:127] dout);

	// Instantiate 16 Inverse Sbox transform modules	
	genvar j;
	generate
		for (j = 0; j < 16; j=j+1) begin : invsbox
			S_Box_Enc_Inv InvSbox_u(.i_Din(din[8*j+:8]), .o_Dout(dout[8*j+:8]));
		end
	endgenerate
		
endmodule