import func as fc
import os

import sys
# os.chdir(os.path.dirname(__file__)) #路径是以此python文件路径为参考 
# SourcePath = "../code/"
# targetpath = fc.make_sim_dic("uart_byte_tx")
# TB = fc.tb_inst(SourcePath,targetpath,'aes_unit')
# fc.makefile_src_gen(targetpath,TB)
#     # tb_inst(path,targetpath,"uart_byte_tx")
# fc.filelist_gen(SourcePath,TB)
fc.simflow('../','../sim/','aes_shiftrows')