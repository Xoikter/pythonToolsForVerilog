OUTPUT = topTB
export name = ${OUTPUT}
VCS:
	vcs -full64 +v2k -timescale=1ns/1ps -debug_all -rdynamic -LDFLAGS -P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a  -f filelist.f -o ${OUTPUT} -l sim.log ./topTB.sv
VERDI:
	verdi -f file_list.f-ssf ${OUTPUT}.fsdb -nologo  -l v.log 
SIM:
	./${OUTPUT}  -ucli -i ./run.scr  +fsdb+autoflush  -l sim.log
CLEAN:
	rm -rf  ./verdiLog  ./dff ./csrc *.daidir *log *.vpd *.vdb simv* *.key *race.out* *.rc *.fsdb *.vpd *.log *.conf *.dat *.conf