from verilog_tools import Verilog_tools as vt
import os
import re
import sys
import ast

if __name__ == '__main__':
    SourcePath = [""]
    TargetPath = ""
    except_module = [""]
    fc = vt()
    if len(sys.argv) > 2:
        fc.SourcePath = sys.argv[2]
    if len(sys.argv) > 3:
        fc.TargetPath = sys.argv[3]

    if len(sys.argv) > 5:
        fc.except_module= ast.literal_eval(sys.argv[5]) 
    
    
    fc.except_module = except_module
    # full_path_temp = os.path.join(sys.argv[3],sys.argv[2])
    # full_path = os.path.normpath(os.path.abspath(full_path_temp)).replace("\\", "/")
    
    if len(sys.argv) > 4:
        name = sys.argv[4]
    
    
    if len(sys.argv) > 1:
        argue = sys.argv[1]
        print(argue)
        if (argue == "inst"):
            fc.file_inst(fc.SourcePath, name ,2)
        elif(argue == "inst_o"):
            fc.file_inst(fc.SourcePath, name,1)
        elif(argue == "vd"):
            fc.autodefine(full_path)
        elif (argue == "t"):
            fc.tb_inst(fc.SourcePath, fc.TargetPath, sys.argv[1])
        elif (argue == 'ssf'):
            print("entry")
            fc.simflow_seq(fc.SourcePath, fc.TargetPath, name)
        elif (argue == 'csf'):
            fc.simflow_comb(fc.SourcePath, fc.TargetPath, sys.argv[1])
        elif (argue == 'f'):
            fc.filelist_regen(1,1,fc.SourcePath,fc.TargetPath,sys.argv[1])
            fc.interface_gen(SourcePath,TargetPath,sys.argv[1],0)
            fc.tb_inst(SourcePath,TargetPath,sys.argv[1],1)
        elif (argue == "ctree"):
            fc.env_initial()
    else:
        print ("need argue")


