class fifo_ctr_sequencer extends uvm_sequencer #(fifo_ctr_transaction);
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction 
    `uvm_component_utils(fifo_ctr_sequencer)
endclass
