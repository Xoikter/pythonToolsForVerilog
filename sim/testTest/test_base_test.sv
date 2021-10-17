class test_base_test extends uvm_test;

   test_env         env;
   
   function new(string name = "test_base_test", uvm_component parent = null);
      super.new(name,parent);
   endfunction
   
   extern virtual function void build_phase(uvm_phase phase);
   extern virtual function void report_phase(uvm_phase phase);
   extern task main_phase(uvm_phase phase);
   `uvm_component_utils(test_base_test)
endclass

task test_base_test::main_phase(uvm_phase phase);
   phase.phase_done.set_drain_time(this,20);
endtask

function void test_base_test::build_phase(uvm_phase phase);
   super.build_phase(phase);
   env  =  test_env::type_id::create("env", this); 
endfunction

function void test_base_test::report_phase(uvm_phase phase);
   uvm_report_server server;
   int err_num;
   super.report_phase(phase);

   server = get_report_server();
   err_num = server.get_severity_count(UVM_ERROR);

   if (err_num != 0) begin
      $display("TEST CASE FAILED");
   end
   else begin
      $display("TEST CASE PASSED");
   end
endfunction

