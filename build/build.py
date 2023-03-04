build_opts = r"vcs  +acc +vpi -j6   -full64 +v2k -sverilog +incdir+${UVM_HOME}/src  ${UVM_HOME}/src/uvm_pkg.sv ${UVM_HOME}/src/dpi/uvm_dpi.cc +define+DEBUG  -CFLAGS -DVCS -lca -kdb +lint=TFIPC-L -timescale=1ns/1ps -debug_acc+all -debug_region+cell+encrypt -LDFLAGS -rdynamic  -P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a  -f ../filelist/filelist.f " + "../tb/"+ self.filename + "_tb.sv"

lists = {
    "base_build":{"build_opts":build_opts}
}

for key  in lists.keys():
    self.build_list[key] = lists[key]