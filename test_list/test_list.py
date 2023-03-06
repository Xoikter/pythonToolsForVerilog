sim_opts = "../../build/simv -licqueue -ucli  -i   ../../sim_ctrl/run.tcl  +fsdbfile+hw.fsdb   -l sim.log"

lists = {
    self.filename+"_case0":{"sim_opts":sim_opts +" +UVM_TESTNAME="+ self.filename+"_case0"+" +UVM_TIMEOUT=\"90000000ns, yes\"", "repeat_num":1}
}


for key in lists.keys():
    print("add test case: "+ key)
    self.test_list[key] = lists[key]