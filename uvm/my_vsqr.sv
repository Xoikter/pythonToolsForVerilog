class my_vsqr extends uvm_sequencer;
  
   my_sequencer  sqr0;

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction 
   
   `uvm_component_utils(my_vsqr)
endclass