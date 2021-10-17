class my_driver extends uvm_driver#(my_transaction);

   virtual my_interface_port vif;
   virtual my_interface_inner vif_i;

   `uvm_component_utils(my_driver)
   function new(string name = "my_driver", uvm_component parent = null);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if(!uvm_config_db#(virtual my_interface_port)::get(this, "", "vif", vif))
         `uvm_fatal("my_driver", "virtual interface must be set for vif!!!")
      if(!uvm_config_db#(virtual my_interface_inner)::get(this, "", "vif_i", vif_i))
         `uvm_fatal("my_driver", "virtual interface must be set for vif_i!!!")
   endfunction

   extern task main_phase(uvm_phase phase);
   extern task drive_one_pkt(my_transaction tr);
endclass

task my_driver::main_phase(uvm_phase phase);
   while(1) begin
      seq_item_port.get_next_item(req);
      drive_one_pkt(req);
      seq_item_port.item_done();
   end
endtask

task my_driver::drive_one_pkt(my_transaction tr);
   // `uvm_info("my_driver", "begin to drive one pkt", UVM_LOW);

   // `uvm_info("my_driver", "end drive one pkt", UVM_LOW);
endtask


