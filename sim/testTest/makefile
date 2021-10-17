OUTPUT = testTB
export name = ${OUTPUT}
VCS:
	vcs  +acc +vpi  -full64 +v2k -sverilog +incdir+${UVM_HOME}/src  ${UVM_HOME}/src/uvm_pkg.sv ${UVM_HOME}/src/dpi/uvm_dpi.cc -CFLAGS -DVCS -lca -kdb -timescale=1ns/1ps -debug_acc+all -debug_region+cell+encrypt -LDFLAGS -rdynamic  -P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a  -f filelist.f  -l sim.log ./testTB.sv
VERDI:
	verdi -f file_list.f -ssf ${OUTPUT}.fsdb -nologo  -l v.log 
SIM:
	./simv  +UVM_TESTNAME=test_case0 -gui=verdi -i   ./run.scr  +fsdbfile+${OUTPUT}.fsdb + autoflush  -l sim.log
SIM_NO_GUI:
	./simv  +UVM_TESTNAME=test_case0  -l sim.log
CLEAN:
	rm -rf  ./verdiLog  ./dff ./csrc *.daidir *log *.vpd *.vdb simv* *.key *race.out* *.rc *.fsdb *.vpd *.log *.conf *.dat *.conf
TEST: VCS SIM
CASE: VCS SIM_NO_GUI