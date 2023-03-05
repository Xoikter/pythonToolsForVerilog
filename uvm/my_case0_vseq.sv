class my_case0_vseq extends uvm_sequence;

   `uvm_object_utils(my_case0_vseq)
   `uvm_declare_p_sequencer(my_vsqr)
   
   function  new(string name= "my_case0_vseq");
      super.new(name);
   endfunction 
   
   virtual task body();
      my_case0_sequence dseq;
      if(starting_phase != null) 
         starting_phase.raise_objection(this);
      dseq = my_case0_sequence::type_id::create("dseq");
      dseq.start(p_sequencer.sqr0);
      
      if(starting_phase != null) 
         starting_phase.drop_objection(this);
   endtask

endclass