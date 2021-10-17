class fifo_ctr_driver extends uvm_driver#(fifo_ctr_transaction);

   virtual fifo_ctr_interface_port vif;
   virtual fifo_ctr_interface_inner vif_i;

   `uvm_component_utils(fifo_ctr_driver)
   function new(string name = "fifo_ctr_driver", uvm_component parent = null);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if(!uvm_config_db#(virtual fifo_ctr_interface)::get(this, "", "vif", vif))
         `uvm_fatal("fifo_ctr_driver", "virtual interface must be set for vif!!!")
   endfunction

   extern task main_phase(uvm_phase phase);
   extern task drive_one_pkt(fifo_ctr_transaction tr);
endclass

task fifo_ctr_driver::main_phase(uvm_phase phase);
   while(1) begin
      seq_item_port.get_next_item(req);
      drive_one_pkt(req);
      seq_item_port.item_done();
   end
endtask

task fifo_ctr_driver::drive_one_pkt(fifo_ctr_transaction tr);
   // `uvm_info("fifo_ctr_driver", "begin to drive one pkt", UVM_LOW);

   // `uvm_info("fifo_ctr_driver", "end drive one pkt", UVM_LOW);
endtask


