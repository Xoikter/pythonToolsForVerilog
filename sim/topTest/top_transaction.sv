class top_transaction extends uvm_sequence_item;
rand bit variable_for_test;



constraint con{
variable_for_test == 0;

}
`uvm_object_utils_begin(top_transaction)


`uvm_object_utils_end
function new(string name = "top_transaction");
super.new();
endfunction
endclass
