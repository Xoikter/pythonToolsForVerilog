class top_driver extends uvm_driver#(top_transaction);

   virtual top_interface_port vif;
   virtual top_interface_inner vif_i;

   `uvm_component_utils(top_driver)
   function new(string name = "top_driver", uvm_component parent = null);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if(!uvm_config_db#(virtual top_interface_port)::get(this, "", "vif", vif))
         `uvm_fatal("top_driver", "virtual interface must be set for vif!!!")
      if(!uvm_config_db#(virtual top_interface_inner)::get(this, "", "vif_i", vif_i))
         `uvm_fatal("top_driver", "virtual interface must be set for vif_i!!!")

   endfunction

   extern task main_phase(uvm_phase phase);
   extern task drive_one_pkt(top_transaction tr);
endclass

task top_driver::main_phase(uvm_phase phase);
   while(1) begin
      seq_item_port.get_next_item(req);
      drive_one_pkt(req);
      seq_item_port.item_done();
   end
endtask

task top_driver::drive_one_pkt(top_transaction tr);
   // `uvm_info("top_driver", "begin to drive one pkt", UVM_LOW);

   // `uvm_info("top_driver", "end drive one pkt", UVM_LOW);
endtask


