class top_monitor extends uvm_monitor;

   virtual top_interface vif;

   uvm_analysis_port #(top_transaction)  ap;
   
   `uvm_component_utils(top_monitor)
   function new(string name = "top_monitor", uvm_component parent = null);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if(!uvm_config_db#(virtual top_if)::get(this, "", "vif", vif))
         `uvm_fatal("top_monitor", "virtual interface must be set for vif!!!")
      ap = new("ap", this);
   endfunction

   extern task main_phase(uvm_phase phase);
   extern task collect_one_pkt(top_transaction tr);
endclass

task top_monitor::main_phase(uvm_phase phase);
   top_transaction tr;
   while(1) begin
      tr = new("tr");
      collect_one_pkt(tr);
      ap.write(tr);
   end
endtask

task top_monitor::collect_one_pkt(top_transaction tr);


endtask


