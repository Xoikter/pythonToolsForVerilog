class fifo_ctr_agent extends uvm_agent ;
   fifo_ctr_sequencer  sqr;
   fifo_ctr_driver     drv;
   fifo_ctr_monitor    mon;
   
   uvm_analysis_port #(fifo_ctr_transaction)  ap;
   
   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction 
   
   extern virtual function void build_phase(uvm_phase phase);
   extern virtual function void connect_phase(uvm_phase phase);

   `uvm_component_utils(fifo_ctr_agent)
endclass 


function void fifo_ctr_agent::build_phase(uvm_phase phase);
   super.build_phase(phase);
   if (is_active == UVM_ACTIVE) begin
      sqr = fifo_ctr_sequencer::type_id::create("sqr", this);
      drv = fifo_ctr_driver::type_id::create("drv", this);
   end
   mon = fifo_ctr_monitor::type_id::create("mon", this);
   mon.is_active = is_active;
endfunction 

function void fifo_ctr_agent::connect_phase(uvm_phase phase);
   super.connect_phase(phase);
   if (is_active == UVM_ACTIVE) begin
      drv.seq_item_port.connect(sqr.seq_item_export);
   end
   ap = mon.ap;
endfunction

