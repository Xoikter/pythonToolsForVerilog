class test_scoreboard extends uvm_scoreboard;
   test_transaction  expect_queue[$];
   uvm_blocking_get_port #(test_transaction)  exp_port;
   uvm_blocking_get_port #(test_transaction)  act_port;
   `uvm_component_utils(test_scoreboard)

   extern function new(string name, uvm_component parent = null);
   extern virtual function void build_phase(uvm_phase phase);
   extern virtual task main_phase(uvm_phase phase);
endclass 

function test_scoreboard::new(string name, uvm_component parent = null);
   super.new(name, parent);
endfunction 

function void test_scoreboard::build_phase(uvm_phase phase);
   super.build_phase(phase);
   exp_port = new("exp_port", this);
   act_port = new("act_port", this);
endfunction 

task test_scoreboard::main_phase(uvm_phase phase);
   test_transaction  get_expect,  get_actual, tmp_tran;
   bit result;
 
   super.main_phase(phase);
   fork 
      // while (1) begin
      //    exp_port.get(get_expect);
      //    expect_queue.push_back(get_expect);
      // end
      while (1) begin
         act_port.get(get_actual);
         exp_port.get(get_expect);
         // if(expect_queue.size() > 0) begin
            // tmp_tran = expect_queue.pop_front();
            result = get_actual.c == get_expect.c;
            if(result) begin 
               `uvm_info("test_scoreboard", "Compare SUCCESSFULLY", UVM_LOW);
            end
            else begin
               `uvm_error("test_scoreboard", "Compare FAILED");
            end
         end
         // else begin
         //    `uvm_error("test_scoreboard", "Received from DUT, while Expect Queue is empty");
         // end 
      // end
   join
endtask