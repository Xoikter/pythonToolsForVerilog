class test_monitor extends uvm_monitor;

   virtual test_interface_port vif;
   virtual test_interface_inner vif_i;
   uvm_active_passive_enum is_active = UVM_ACTIVE;
   uvm_analysis_port #(test_transaction)  ap;
   
   `uvm_component_utils(test_monitor)
   function new(string name = "test_monitor", uvm_component parent = null);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      int active;
      super.build_phase(phase);
      if(!uvm_config_db#(virtual test_interface_port)::get(this, "", "vif", vif))
         `uvm_fatal("test_monitor", "virtual interface must be set for vif!!!")
      if(!uvm_config_db#(virtual test_interface_inner)::get(this, "", "vif_i", vif_i))
         `uvm_fatal("test_monitor", "virtual interface must be set for vif_i!!!")
      ap = new("ap", this);      
      if(get_config_int("is_active", active)) is_active = uvm_active_passive_enum'(active);
   endfunction

   extern task main_phase(uvm_phase phase);
   extern task collect_one_pkt(test_transaction tr);
endclass

task test_monitor::main_phase(uvm_phase phase);
   test_transaction tr;
   //------------forever------//
   // while(1) begin
   //    tr = new("tr");
   //    collect_one_pkt(tr);
   //    ap.write(tr);
   // end

   //------------repeat-------//
   repeat(1) begin
      tr = new("tr");
      collect_one_pkt(tr);
      ap.write(tr);
   end


endtask

task test_monitor::collect_one_pkt(test_transaction tr);
      if(is_active == UVM_ACTIVE) begin

      end
      else begin

      end

endtask


