class fifo_ctr_model extends uvm_component;
   
   uvm_blocking_get_port #(fifo_ctr_transaction)  port;
   uvm_analysis_port #(fifo_ctr_transaction)  ap;

   extern function new(string name, uvm_component parent);
   extern function void build_phase(uvm_phase phase);
   extern virtual  task main_phase(uvm_phase phase);

   `uvm_component_utils(fifo_ctr_model)
endclass 

function fifo_ctr_model::new(string name, uvm_component parent);
   super.new(name, parent);
endfunction 

function void fifo_ctr_model::build_phase(uvm_phase phase);
   super.build_phase(phase);
   port = new("port", this);
   ap = new("ap", this);
endfunction

task fifo_ctr_model::main_phase(uvm_phase phase);
   fifo_ctr_transaction tr;
   fifo_ctr_transaction old_tr;
   super.main_phase(phase);
   while(1) begin
      port.get(old_tr);
      tr = new("tr");
      ap.write(tr);
   end
endtask