import uvm_pkg::*;
class my_transaction extends uvm_sequence_item;

    constraint pload_cons{
 
   }



   function void post_randomize();
      crc = calc_crc;  
      endfunction

   `uvm_object_utils_begin(my_transaction)
   `uvm_object_utils_end

   function new(string name = "my_transaction");
      super.new();
   endfunction

endclass
