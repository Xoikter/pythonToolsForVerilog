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

# fc.simflow('../','../sim/','Mix_Columns_Enc')


argue = input("cmd:")

if (argue == "i"):
    # print(sys.argv[1])
    fc.file_inst(['E:/xsc/pro/git_pro/pythonToolsForVerilog/code/'], sys.argv[1])
elif (argue == "t"):
    fc.tb_inst('../', '../sim', sys.argv[1])
elif (argue == 's'):
    fc.simflow('../', '../sim/', sys.argv[1])
elif (argue == 'f'):
    targetpath = fc.make_sim_dic('../sim/', sys.argv[1])
    fc.filelist_gen('../', targetpath, sys.argv[1])
