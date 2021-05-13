from pythonToolsForVerilog import func as fc

import sys
print (sys.path)
targetpath = fc.make_sim_dic("uart_byte_tx")
fc.makefile_src_gen(targetpath,"uart_byte_tx")
    # tb_inst(path,targetpath,"uart_byte_tx")
fc.filelist_gen(path,targetpath,"uart_byte_txTB")