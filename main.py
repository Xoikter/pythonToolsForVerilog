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
    
    os.chdir(os.path.dirname(__file__)) #路径是以此python文件路径为参考 
    if not os.path.isfile("config.txt"):
        print("config file create")
        fd = open("./config.txt","w+")
        fd.write("SourcePath = [];\n")
        fd.write("TargetPath = \"\";\n")
        fd.write("except module = [];\n")
        fd.close
    else:
        with open("./config.txt","r+",errors="ignore") as fd:
            text = fd.read()
            config = re.findall("\\b(SourcePath|TargetPath|except module)\s*=\s*(.*?)\s*;",text,flags=re.S)
            for item in config:
                if(item[0] == "SourcePath"):
                    SourcePath = ast.literal_eval(item[1])
                elif(item[0] == "TargetPath"):
                    TargetPath = ast.literal_eval(item[1])
                elif(item[0] == "except module"):
                    except_module = ast.literal_eval(item[1])
            fd.close()
        fc.SourcePath = SourcePath
        fc.TargetPath = TargetPath
    
    
    
        # SourcePath = "../code/"
        # targetpath = fc.make_sim_dic("uart_byte_tx")
        # TB = fc.tb_inst(SourcePath,targetpath,'aes_unit')
        # fc.makefile_src_gen(targetpath,TB)
        #     # tb_inst(path,targetpath,"uart_byte_tx")
        # fc.filelist_gen(SourcePath,TB)
    
        # fc.simflow('../','../sim/','Mix_Columns_Enc')
        # fc.except_module.append('assert_never_unknown')
        fc.except_module = except_module
    # SourcePath = SourcePath
    # TargetPath = TargetPath
        full_path_temp = os.path.join(sys.argv[3],sys.argv[2])
        full_path = os.path.normpath(os.path.abspath(full_path_temp)).replace("\\", "/")
        # print(os.path.normpath(os.path.abspath(full_path)).replace("\\", "/"))

        argue = input("cmd:")


        if (argue == "i"):
            # print(sys.argv[1])
            fc.file_inst(SourcePath, full_path,2)
        elif(argue == "i_o"):
            fc.file_inst(SourcePath, full_path,1)
        elif(argue == "vd"):
            fc.autodefine(full_path)
        elif (argue == "t"):
            fc.tb_inst(SourcePath, TargetPath, sys.argv[1])
        elif (argue == 'ssf'):
            fc.simflow_seq(SourcePath, TargetPath, sys.argv[1])
        elif (argue == 'csf'):
            fc.simflow_comb(SourcePath, TargetPath, sys.argv[1])
        elif (argue == 'f'):
            fc.filelist_regen(1,0,1,2,1,SourcePath,TargetPath,sys.argv[1])
            fc.interface_gen(SourcePath,TargetPath,sys.argv[1],0)
            fc.tb_inst(SourcePath,TargetPath,sys.argv[1],1)

