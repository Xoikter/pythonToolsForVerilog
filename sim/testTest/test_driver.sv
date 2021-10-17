class test_driver extends uvm_driver#(test_transaction);

   virtual test_interface_port vif;
   virtual test_interface_inner vif_i;

   `uvm_component_utils(test_driver)
   function new(string name = "test_driver", uvm_component parent = null);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if(!uvm_config_db#(virtual test_interface_port)::get(this, "", "vif", vif))
         `uvm_fatal("test_driver", "virtual interface must be set for vif!!!")
      if(!uvm_config_db#(virtual test_interface_inner)::get(this, "", "vif_i", vif_i))
         `uvm_fatal("test_driver", "virtual interface must be set for vif_i!!!")

   endfunction

   extern task main_phase(uvm_phase phase);
   extern task drive_one_pkt(test_transaction tr);
endclass

task test_driver::main_phase(uvm_phase phase);
   while(1) begin
      seq_item_port.get_next_item(req);
      drive_one_pkt(req);
      seq_item_port.item_done();
   end
endtask

task test_driver::drive_one_pkt(test_transaction tr);
   // `uvm_info("test_driver", "begin to drive one pkt", UVM_LOW);

   // `uvm_info("test_driver", "end drive one pkt", UVM_LOW);
endtask


