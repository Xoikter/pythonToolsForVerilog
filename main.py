from verilog_tools import Verilog_tools as vt
import os
import re
import sys
import ast
import getopt
import argparse
# parser = argparse.ArgumentParser(description='Test for argparse')
# parser.add_argument('--source', '-s', help='非必要参数')
# parser.add_argument('--target', '-d', help='非必要参数，但是有默认值')
# parser.add_argument('--command', '-c', help='必要参数')
# parser.add_argument('--top', '-t', help='必要参数')
# parser.add_argument('--name', '-n', help='必要参数')
# parser.add_argument('--exclude', '-e', help='必要参数')
# args = parser.parse_args()
if __name__ == '__main__':
    SourcePath = [""]
    TargetPath = ""
    except_module = [""]
    config_flag = False
    del_pass = False
    # print(sys.argv[1:])
    agent_in_num = 1
    agent_out_num = 1
    name = "test"
    uvm_verbosity = "UVM_MEDIUM"

    opts, argv = getopt.getopt(sys.argv[1:],"c:t:n:x:s:r:e",["agent_in_num=","agent_out_num=","del_pass=","uvm_verbosity=","sp=","tp="])
    # print(args.exclude)
    for opt, arg in opts:
        if(opt == '-e'):
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
                    config_flag = True
        elif(opt == '-c'):
            cmd = arg
        elif(opt == '-t'):
            top = arg
            name = top
        elif(opt == '-n'):
            name = arg
        elif(opt == '-x'):
            testcase = arg
            # print(testcase)
        elif(opt == '-s'):
            # print(arg)
            if arg == "":
                seed = None
            else:
                seed = int(arg)
        elif(opt == '-r'):
            if arg == "":
                repeat_num = None
            else:
                repeat_num = int(arg)
        elif(opt == '--uvm_verbosity'):
            uvm_verbosity = arg
        elif(opt == '--sp'):
            sourceFile = arg
        elif(opt == '--tp'):
            TargetFile = arg
        elif(opt == '-agent_in_num'):
            agent_in_num = int(arg)
        elif(opt == '-agent_out_num'):
            agent_out_num = int(arg)
        elif(opt == '--del_pass'):
            if(arg == "True"):
                del_pass = True
            else:
                del_pass = False

    fc = vt(name,agent_in_num,agent_out_num)
    fc.SourcePath = SourcePath
    fc.TargetPath = TargetPath
    fc.except_module = except_module
    fc.uvm_verbosity = uvm_verbosity
    # print(del_pass)
    fc.del_pass = del_pass
    fc.read_py()
    # if len(sys.argv) > 2:
        # fc.SourcePath = sys.argv[2]
    # if len(sys.argv) > 3:
    #     fc.TargetPath = sys.argv[3]

    # if len(sys.argv) > 5:
        # print(sys.argv[5])
        # print(type(sys.argv[5]))
        # fc.except_module= eval(sys.argv[5]) 
        # fc.except_module= ast.literal_eval(sys.argv[5]) 
    
    
    # full_path_temp = os.path.join(sys.argv[3],sys.argv[2])
    # full_path = os.path.normpath(os.path.abspath(full_path_temp)).replace("\\", "/")
    
    # if len(sys.argv) > 4:
    #     name = sys.argv[4]
    
    
    if len(sys.argv) > 1:
        # argue = sys.argv[1]
        print("[INFO] command: " + cmd)
        if (cmd == "inst"):
            if config_flag:
                fc.file_inst(fc.SourcePath, name ,2)
            else: 
                print("need config file")
        elif(cmd == "inst_o"):
            if config_flag:
                fc.file_inst(fc.SourcePath, name,1)
            else: 
                print("need config file")
        elif(cmd == "vd"):
            fc.autodefine(full_path)
        elif (cmd == "t"):
            fc.tb_inst(fc.SourcePath, fc.TargetPath, sys.argv[1])
        elif (cmd == 'ssf'):
            # print("entry")
            if config_flag:
                fc.simflow_seq(fc.SourcePath, fc.TargetPath, top)
            else: 
                print("need config file")
        elif (cmd == 'csf'):
            fc.simflow_comb(fc.SourcePath, fc.TargetPath, sys.argv[1])
        elif (cmd == 'f'):
            fc.filelist_regen(1,1,fc.SourcePath,fc.TargetPath,sys.argv[1])
            fc.interface_gen(SourcePath,TargetPath,sys.argv[1],0)
            fc.tb_inst(SourcePath,TargetPath,sys.argv[1],1)
        elif (cmd == "ctree"):
            fc.env_initial(1)
        elif (cmd == "ctree_lite"):
            fc.env_initial(0)
        elif (cmd == "comp"):
            fc.comp()
        elif (cmd == "lint"):
            fc.lint()
        elif (cmd == "dc"):
            fc.dc()
        elif (cmd == "lint_gui"):
            fc.lint_gui()
        elif (cmd == "sim"):
            fc.sim(testcase,seed,repeat_num,0)
        elif (cmd == "all"):
            fc.all(testcase,seed,repeat_num)
        elif (cmd == "regress"):
            # fc.sim(testcase,seed,repeat_num,1)
            fc.regress(repeat_num)
        elif (cmd == "sanity"):
            fc.sanity()
        elif (cmd == "gen_top"):
            fc.gen_top(sourceFile,TargetFile,fc.SourcePath,2)
        elif (cmd == "gen_filelist"):
            fc.gen_filelist(name,TargetFile)
    else:
        print ("need cmd")


