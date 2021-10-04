class top_case0_sequence extends uvm_sequence #(top_transaction);
   top_transaction m_trans;

   function  new(string name= "top_case0_sequence");
      super.new(name);
   endfunction 
   
   virtual task body();

      if(starting_phase != null) 
         starting_phase.raise_objection(this);



      if(starting_phase != null) 
         starting_phase.drop_objection(this);
   endtask

   `uvm_object_utils(top_case0_sequence)
endclass


class top_case0 extends top_base_test;

   function new(string name = "top_case0", uvm_component parent = null);
      super.new(name,parent);
   endfunction 
   extern virtual function void build_phase(uvm_phase phase); 
   `uvm_component_utils(top_case0)
endclass


function void top_case0::build_phase(uvm_phase phase);
   super.build_phase(phase);

   uvm_config_db#(uvm_object_wrapper)::set(this, 
                                           "env.i_agt.sqr.main_phase", 
                                           "default_sequence", 
                                           top_case0_sequence::type_id::get());
endfunction

