OUTPUT = topTB
export name = ${OUTPUT}
VCS:
	vcs  +acc +vpi -j6   -full64 +v2k -sverilog -ntb_options uvm-1.2  +define+DEBUG  -CFLAGS -DVCS -lca -kdb +lint=TFIPC-L -timescale=1ns/1ps -debug_acc+all -debug_region+cell+encrypt -LDFLAGS -rdynamic  -P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a  -f filelist.f  -l sim.log ./${OUTPUT}TB.sv
VERDI:
	verdi -f file_list.f -ssf ${OUTPUT}.fsdb -nologo  -l v.log 
SIM:
	./simv   +UVM_TESTNAME=${OUTPUT}_case0 -gui=verdi -i   ./run.scr  +fsdbfile+${OUTPUT}.fsdb + autoflush  -l sim.log
SIM_NO_GUI:
	./simv   +UVM_TESTNAME=${OUTPUT}_case0 -i  ./run.scr -l sim.log
CLEAN:
	rm -rf  ./verdiLog  ./dff ./csrc *.daidir *log *.vpd *.vdb simv* *.key *race.out* *.rc *.fsdb *.vpd *.log *.conf *.dat *.conf
TEST: VCS SIM
CASE: VCS SIM_NO_GUI