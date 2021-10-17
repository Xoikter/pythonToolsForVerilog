class test_transaction extends uvm_sequence_item;
rand bit variable_for_test;



constraint con{
variable_for_test == 0;

}
`uvm_object_utils_begin(test_transaction)


`uvm_object_utils_end
function new(string name = "test_transaction");
super.new();
endfunction
endclass
