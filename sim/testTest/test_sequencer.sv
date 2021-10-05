class test_sequencer extends uvm_sequencer #(test_transaction);
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction 
    `uvm_component_utils(test_sequencer)
endclass
