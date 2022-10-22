class my_case0_sequence extends uvm_sequence #(my_transation);
   my_transation m_trans;

   function  new(string name= "my_case0_sequence");
      super.new(name);
   endfunction 
   
   virtual task body();

      if(starting_phase != null) 
         starting_phase.raise_objection(this);
      repeat(10) begin
         `uvm_do(m_trans)
      end


      if(starting_phase != null) 
         starting_phase.drop_objection(this);
   endtask

   `uvm_object_utils(my_case0_sequence)
endclass


class my_case0 extends my_base_test;

   function new(string name = "case0", uvm_component parent = null);
      super.new(name,parent);
   endfunction 
   extern virtual function void build_phase(uvm_phase phase); 
   `uvm_component_utils(my_case0)
endclass


function void my_case0::build_phase(uvm_phase phase);
   super.build_phase(phase);

   uvm_config_db#(uvm_object_wrapper)::set(this, 
                                           "env.i_agt.sqr.main_phase", 
                                           "default_sequence", 
                                           my_case0_sequence::type_id::get());
endfunction

