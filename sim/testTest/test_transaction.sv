import uvm_pkg::*;
class test_transaction extends uvm_sequence_item;
rand bit [3:0] a,b;
rand bit [4:0] c;


constraint con{
a == 5;
b == 8;

}
`uvm_object_utils(test_transaction)
function new(string name = "test_transaction");
super.new();
endfunction
endclass
