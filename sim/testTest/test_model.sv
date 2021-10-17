class test_model extends uvm_component;
   
   uvm_blocking_get_port #(test_transaction)  port;
   uvm_analysis_port #(test_transaction)  ap;

   extern function new(string name, uvm_component parent);
   extern function void build_phase(uvm_phase phase);
   extern virtual  task main_phase(uvm_phase phase);

   `uvm_component_utils(test_model)
endclass 

function test_model::new(string name, uvm_component parent);
   super.new(name, parent);
endfunction 

function void test_model::build_phase(uvm_phase phase);
   super.build_phase(phase);
   port = new("port", this);
   ap = new("ap", this);
endfunction

task test_model::main_phase(uvm_phase phase);
   test_transaction tr;
   test_transaction old_tr;
   super.main_phase(phase);
   while(1) begin
      port.get(old_tr);
      tr = new("tr");
      tr.c = old_tr.a + old_tr.b;
      ap.write(tr);
   end
endtask