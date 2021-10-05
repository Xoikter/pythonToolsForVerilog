class test_monitor extends uvm_monitor;

   virtual test_interface vif;
   uvm_active_passive_enum is_active = UVM_ACTIVE;
   uvm_analysis_port #(test_transaction)  ap;
   
   `uvm_component_utils(test_monitor)
   function new(string name = "test_monitor", uvm_component parent = null);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      int active;
      super.build_phase(phase);
      if(!uvm_config_db#(virtual test_interface)::get(this, "", "vif", vif))
         `uvm_fatal("test_monitor", "virtual interface must be set for vif!!!")
      ap = new("ap", this);      
      if(get_config_int("is_active", active)) is_active = uvm_active_passive_enum'(active);
   endfunction

   extern task main_phase(uvm_phase phase);
   extern task collect_one_pkt(test_transaction tr);
endclass

task test_monitor::main_phase(uvm_phase phase);
   test_transaction tr;
   while(1) begin
      collect_one_pkt(tr);
   end
endtask

task test_monitor::collect_one_pkt(test_transaction tr);
      @(posedge vif.clk)
      tr = new("tr");
      if(is_active == UVM_ACTIVE) begin
         if(vif.vld) begin
        tr.a = vif.a; 
        tr.b = vif.b; 
        $display("i  x = %d\d",tr.a);
        $display("i  b = %d\d",tr.b);
         ap.write(tr);
         end

      end
      else begin
         // if(vif.ifo.clk) begin
         if(vif.vld) begin
         tr.c = vif.c;
         $display("o  c = %d\d",tr.c);
         ap.write(tr);
         end

      end

endtask


