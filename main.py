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

SourcePath = ["./code/"]
TargetPath = "./sim/"

argue = input("cmd:")

if (argue == "i"):
    # print(sys.argv[1])
    fc.file_inst(SourcePath, sys.argv[1])
elif (argue == "t"):
    fc.tb_inst(SourcePath, TargetPath, sys.argv[1])
elif (argue == 's'):
    fc.simflow(SourcePath, TargetPath, sys.argv[1])
elif (argue == 'f'):
    fc.filelist_regen(1,0,1,3,1,SourcePath,TargetPath,sys.argv[1])

