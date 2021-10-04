class top_sequencer extends uvm_sequence #(top_transaction);
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction     `uvm_component_utils(top_sequencer)