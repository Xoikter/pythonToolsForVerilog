class my_transation extends uvm_sequence_item;

    constraint pload_cons{
 
   }



   function void post_randomize();
      // crc = calc_crc;  
      endfunction

   `uvm_object_utils_begin(my_transation)
   `uvm_object_utils_end

   function new(string name = "my_transation");
      super.new();
   endfunction

endclass
