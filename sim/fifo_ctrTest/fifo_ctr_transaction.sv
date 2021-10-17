class fifo_ctr_transaction extends uvm_sequence_item;
rand bit variable_for_test;



constraint con{
variable_for_test == 0;

}
`uvm_object_utils_begin(fifo_ctr_transaction)


`uvm_object_utils_end
function new(string name = "fifo_ctr_transaction");
super.new();
endfunction
endclass
