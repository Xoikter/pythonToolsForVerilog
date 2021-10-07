import os
import re
import uvm_gen as ug
# path = "../verilog_python"
keyword = ['always', 'and', 'assign', 'begin', 'buf', 'bufif0', 'bufif1', 'case', 'casex', 'casez', 'cmos', 'deassign',
           'default',
           'defparam', 'disable', 'edge', 'else', 'end', 'endcase', 'endmodule', 'endfunction', 'endprimitive',
           'endspecify',
           'endtable', 'endtask', 'event', 'for', 'force', 'forever', 'fork', 'function', 'highz0', 'highz1', 'if',
           'initial',
           'inout', 'input', 'integer', 'join', 'large', 'macromodule', 'medium', 'module', 'nand', 'negedge', 'nmos',
           'nor', 'not', 'notif0',
           'notifl', 'or', 'output', 'parameter', 'pmos', 'posedge', 'primitive', 'pull0', 'pull1', 'pullup',
           'pulldown', 'rcmos',
           'reg', 'releses', 'repeat', 'mmos', 'rpmos', 'rtran', 'rtranif0', 'rtranif1', 'scalared', 'small', 'specify',
           'specparam',
           'strength', 'strong0', 'strong1', 'supply0', 'supply1', 'table', 'task', 'time', 'tran', 'tranif0',
           'tranif1', 'tri',
           'tri0', 'tri1', 'triand', 'trior', 'trireg', 'vectored', 'wait', 'wand', 'weak0', 'weak1', 'while', 'wire',
           'wor', 'xnor', 'xor','extends','uvm_report_server','int','void','virtual','new','uvm_analysis_port','super'
           ,'extern0',"uvm_component_utils","type_id",'bit','byte','unsiged','shortint','longint','timer','real','interface','class',
           'logic','genvar','uvm_tlm_analysis_fifo','uvm_blocking_get_port','constraint','import','uvm_active_passive_enum','define','undef'
           ,'ifdef','elsif','endif']
# path = "/home/IC/xsc"
filename = "fifo_ctr"

filemap = {}
definemap = {}
except_module = ['assert_never_unknown']





def find_port(filename,name):
    ports = []
    parameters = []
    fd = open(filename, errors='ignore')
    # result = 
    str = fd.read()
    str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
    # str_temp = re.sub(r'//.*',"",str_temp)
    str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
    str_temp = re.sub("\\bfunction\\b[\s\S]*?\\bendfunction\\b", "", str_temp)
    str_temp = re.search("\\bmodule\\b\s*\\b" + name + "\\b.*?endmodule", str_temp, flags=re.S).group()
    str_temp = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", str_temp)
    str_temp = re.sub("\\binterface\\b.*?;", "", str_temp, flags=re.S)
    str_port = re.search("\\bmodule.*?;",str_temp,flags=re.S).group()
    result = re.findall('\\b(input|output)\\b\s*\\b(wire|reg)?\\b\s*(\[.*?\])?\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)', str_port, flags=re.S)
    res_para = re.findall('\\bparameter\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)(\s*=)',str_port,flags=re.S)
    for res in res_para:
        para_temp = res[0]
        parameters.append(para_temp)
    for res in result:
        portTemp = [res[0], res[1], res[2], res[3]]
        ports.append(portTemp)
    str_temp = re.sub("\\bmodule.*?;","",str_temp,flags=re.S)
    result = re.findall('\\b(input|output)\\b\s*\\b(wire|reg)?\\b\s*(\[.*?\])?\s*(.*?)\s*;', str_temp, flags=re.S)
    res_para = re.findall('\\bparameter\\b\s*(.*?)\s*;',str_temp,flags=re.S)
    for res in res_para:
        res_temp1 = re.split("\s*,\s*",res)
        for item in res_temp1:
            res_temp2 = re.split('\s*=\s*',item)
            parameters.append(res_temp2[0])

    # parameters_temp = re.findall("\\bparameters")
    for res in result:
        # print(res)
        res_temp = re.split("\s*,\s*", res[3])
        for item in res_temp:
            portTemp = [res[0], res[1], res[2], item]
            ports.append(portTemp)
        # portTemp = [res[0], res[1], res[2], res[3]]
        # ports.append(portTemp)
    # for line in fd.readlines():
    #     result = re.findall('(input|output)\s+(wire|reg)?\s*(\[.*?\])?\s+(\w+)',line,re.M)
    #     if(len(result) != 0):
    #         portTemp = [result[0][0],result[0][1],result[0][2],result[0][3]]
    #         ports.append(portTemp)
    # print(ports)
    return [ports, parameters]


def find_define(path):
    fp = open(path, "r", errors="ignore")
    string = fp.read()
    str_temp = re.sub("\/\*.*?\*\/", "", string, flags=re.S)
    # str_temp = re.sub(r'//.*',"",str_temp)
    str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
    defines = []
    result = re.findall("`(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)", str_temp)
    for item in result:
        if item not in keyword:
            defines.append(item)
    return defines


def find_define_file(path, define_word):
    out_path = ""
    if define_word in definemap:
        return definemap[define_word]
 
    for start in path:
        for relpath, dirs, files in os.walk(start):
            for File in files:
                if re.match('.+\.s?v$', File) is not None:
                    fp = open(os.path.join(relpath, File), "r", errors="ignore")
                    str = fp.read()
                    str_temp = re.sub("\/\*[\s\S]*?\*\/", "", str)
                    # str_temp = re.sub(r'//.*$',"",str_temp)
                    str_temp = re.sub('//[\s\S]*?\n', "", str_temp)
                    # print(File)

                    full_path = os.path.join(relpath, File)
                    # if(re.match(name + '.s?v$',File) != None):
                    res_temp = re.findall("`define\s*([\S]*)\s*",str_temp)
                    for item in res_temp:
                        if item  not in definemap:
                            definemap[item] = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                        
                


                    if re.search('`define\s*(\\b'+define_word+'\\b)', str_temp) is not None:
                    # for 
                        if out_path == "":
                            out_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                        else:
                            print("find mutidefine\n")
                            print(os.path.normpath(os.path.abspath(full_path)).replace("\\", "/") + "Y")
                            print(out_path + "N")
                            sel = input("select:")
                            if sel == "Y":
                                out_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                        # return out_path
                        # print(full_path)
                        # return os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
    return out_path


def find_module(path,flag):
    # print(path)
    # print(flag)
    fp = open(path, "r", errors="ignore")
    str = fp.read()
    str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
    # str_temp = re.sub(r'//.*',"",str_temp)
    str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
    str_temp = re.sub('\\bif\s*\(.*?\)', " ; ", str_temp, flags=re.S)
    str_temp = re.sub('\\bcase\s*\(.*?\)', " ; ", str_temp, flags=re.S)
    str_temp = re.sub('\\bextern.*?;', " ; ", str_temp, flags=re.S)
    str_temp = re.sub('\\bfunction.*?\\bendfunction', " ; ", str_temp, flags=re.S)
    str_temp = re.sub('\\bdefine.*', " ; ", str_temp)
    # str_temp = re.sub('\\bgenerate.*?\\bendgenerate', " ; ", str_temp, flags=re.S)
    str_temp = re.sub('\\btask.*?\\bendtask', " ; ", str_temp, flags=re.S)

    modules = []
    if flag == 0 or flag == 5:
        result = re.findall("#\(\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*\)",str_temp,flags=re.S)
        for item in result:
            if(item not in keyword):
                modules.append(item)

    # str_re1 = ""
    # str1 = "\((?:\s*\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\((?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\),)*\s*(?:\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\((?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\))\s*\)"
    # str1 = "\((?:\s*\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\(.*?\)\s*,)*\s*(?:\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\(.*?\)\s*)\s*\)"
    # str2 = "\((?:.*?\s*,)*.*?\)"
    # # str2 = "\((?:(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*),)*(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\)"
    # str3 = "(?:\s*#\s*(?:"+str1 +"|" + str2 + "))?\s*"
    # str4 = "\s*(?:"+str1 +"|" + str2 + ")\s*;"
    # str5 = "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str3 + "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str4
    # result = re.findall(str5, str,flags=re.S)
#     str1 = "\((?:\s*\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\([^\(\)]*?\)\s*,)*\s*(?:\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\([^\(\)]*?\)\s*)\s*\)"
#     str2 = "\((?:[^\(\)]*?\s*,)*[^\(\)]*?\)\s*"
# # str2 = "\((?:(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*),)*(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\)"
#     str3 = "(?:\s*#\s*(?:"+str1 +"|" + str2 + "))?\s*"
#     str4 = "\s*(?:"+str1 +"|" + str2 + ")\s*;"
#     str5 = "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str3 + "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str4
#     result = re.findall(str5, str,flags=re.S)
    # str2 = "\s*\((?:(?:.*?)(?=,)\s*)*?(?:(?:.*?))(?=\)\s*)\s*\)\s*"
    # str1 = "\s*\((?:\s*\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\(.*?(?=\)\s*,)\)\s*,)*\s*(?:\s*\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\(.*?(?=\)\s*\))\)\s*\))\s*\s*"


    # str1 = "\s*\((?:\s*\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\([^\(\)]*?\)\s*,)*\s*(?:\.(?:\s*\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b\s*)\s*\([^\(\)]*?\)\s*)\s*\)\s*"
    # str2 = "\s*\((?:[^\(\)]*?\s*,)*[^\(\)]*?\)\s*"
    # str3 = "\s*(?:\s*#\s*(?:"+str1 +"|" + str2 + "))?\s*"
    # str4 = "\s*(?:"+str1 +"|" + str2 + ")\s*;"
    # str5 = "\s*(?:"+str1 +"|" + str2 + ")?\s*;"
    # str6 = "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str3 + "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str4
    # str7 = "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str3 + "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*" + str5


    str7 = "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(?:\(.*?\))?;"
    str6 = "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(?:#\s*\(.*?\))?\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*\(.*?\)\s*;"
    
    if flag == 0 or flag == 5:
        result = re.findall(str7, str_temp,flags=re.S)
    else:
        result = re.findall(str6, str_temp,flags=re.S)
    
    # result = re.findall('(?:;|end|endfunction|endtask|endclass|endinterface|endmodule)\s*(?:)(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(\(.*?\))?\s*;', str_temp,flags=re.S)
    for item in result:
        if (item[0] not in keyword) and (item[1] not in keyword) and (item[0] not in except_module):
            # print(item)
            modules.append(item[0])

    return modules
    # for line in fp.readlines():
    #     result = re.findall('(\w+)\s+(\w+)\s*\(',line)
    # print(result)


def find_file(starts, name):
    # print(start)
    out_path = ""
    # for item in filemap:
    #     if name == item[0]:
    #         return item[1]
    if name in filemap:
        return filemap[name]
    for start in starts:
        for relpath, dirs, files in os.walk(start):
            for File in files:
                if re.match('.+\.s?v$', File) is not None:
                    fp = open(os.path.join(relpath, File), "r", errors="ignore")
                    str = fp.read()
                    str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
                    # str_temp = re.sub(r'//.*',"",str_temp)
                    str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)

                    full_path = os.path.join(relpath, File)
                    res_temp =  re.findall('\\b(module|interface|class|program)\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\\b', str_temp)
                    for item in res_temp:
                        # flag_file = 0
                        if item[1] not in filemap:
                            # if mod[0] == item[1]:
                                # flag_file = 1
                        # if flag_file == 0:
                            # filemap.append([item[1],os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")])
                            filemap[item[1]] = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                    # for item in res_temp:
                    #     if name == item[1]:
                    # print(File)
                    # if(re.match(name + '.s?v$',File) != None):
                    if re.search('\\b(module|interface|class|program)\\b\s*' + name + '\\b', str_temp) is not None:
                            # full_path = os.path.join(relpath, File)
                            if out_path == "":
                                out_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                            else:
                                print("find mutidefine\n")
                                print(os.path.normpath(os.path.abspath(full_path)).replace("\\", "/") + "Y")
                                print(out_path + "N")
                                sel = input("select:")
                                if sel == "Y":
                                    out_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")

                        # print(full_path)
                        # return os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
    # filemap.append([name,out_path])
    return out_path


def filelist_gen(source_path, target_path, name, flags,flag1):
    os.chdir(os.path.dirname(__file__))
    path = find_file(source_path, name)
    if flags == 1 or flags == 3:
        defines = find_define(path)
        lists_root = []
        for item in defines:
            define_files = find_define_file(source_path, item)
            if define_files not in lists_root:
                lists_root.append(define_files)

    # print(path)
    # print(name)
    lists = find_module(path,flags)
    # print(lists)
    flag = 1
    list_pass = []
    while flag == 1:
        list_temp = []
        flag = 0
        # print(flag)
        for list in lists:
            # print(list)
            modules = []
            if list not in list_temp:
                dic = find_file(source_path,list)
                modules = find_module(dic,flags)            
                # if len(modules) != 0:
                #     flag = 1
                for module in modules:
                    if module not in list_temp:
                        list_temp.append(module)
                    if module not in lists:
                        flag = 1
                list_temp.append(list)
        lists = list_temp
    if flags == 1 or flags == 3:
        for list in lists:
            defines_temp = find_define(find_file(source_path,list))
            for define in defines_temp:
                define_file = find_define_file(source_path, define)
                if define_file not in lists_root:
                    lists_root.append(define_file)











        #     if list not in list_pass:
        #         dic = find_file(source_path, list)
        #         defines_temp = find_define(path)
        #         for item in defines:
        #             define_files = find_define_file(source_path, item)
        #             if define_files not in lists_root:
        #                 lists_root.append(define_files)
        #         # print(dic)
        #         modules = find_module(dic)
        #         # print(modules)
        #         if len(modules) != 0:
        #             flag = 1
        #             # print(flag)
        #             for module in modules:
        #                 if module not in lists:
        #                     list_temp.append(module)

        #         # if(len(modules) != 0):
        #         #     flag = 1
        #         #     list_temp.extend(modules)
        #     if list not in list_temp:
        #         list_temp.append(list)
        #     if list not in list_pass:
        #         list_pass.append(list)
        # lists = list_temp


    os.chdir(target_path)
    if flags == 0 or flags == 5:
        fo = open("filelist_uvm_base.f","w")
        os.chdir(os.path.dirname(__file__))
        file_path_temp = []
        for item in lists:
            temp_path = find_file(source_path,item)
            if temp_path not in file_path_temp:
                file_path_temp.append(temp_path)
        for item in file_path_temp:
            fo.write(item + "\n")
        fo.write(path + "\n")
        fo.close()
    if flags == 5:
        os.chdir(target_path)
        fl = open("filelist_uvm_case.f","w")
        os.chdir(os.path.dirname(__file__))
        fl.write(find_file(source_path,"case0")+"\n")
        fl.close()
        os.chdir(target_path)
        fl = open("filelist_uvm.f","w")
        fl.write("-f "+os.path.abspath(os.path.dirname("filelist_uvm_base.f")).replace("\\", "/") + '/filelist_uvm_base.f' + "\n")
        fl.write("-f "+os.path.abspath(os.path.dirname("filelist_uvm_case.f")).replace("\\", "/") + '/filelist_uvm_case.f' + "\n")
        fl.close()



    if flags == 1 or flags == 3:
        os.chdir(target_path)
        fq = open("filelist_defines.f", "w")
        os.chdir(os.path.dirname(__file__))
        for item in lists_root:
            fq.write(item + "\n")
        if flag1== 1 and flags != 3:
            fq.write(path + "\n")
        fq.close()
        # lists = lists_root + lists
    if flags == 2 or flags == 3:
        os.chdir(target_path)
        fp = open("filelist_modules.f", "w")
        os.chdir(os.path.dirname(__file__))
        # for list in lists:
        #     fp.write(find_file(source_path, list) + "\n")
        # if flag1 == 1:
        #     fp.write(path + "\n")
        file_path_temp = []
        for item in lists:
            temp_path = find_file(source_path,item)
            if temp_path not in file_path_temp:
                file_path_temp.append(temp_path)
        for item in file_path_temp:
            fp.write(item + "\n")
        if flag1 == 1:
            fp.write(path + "\n")
        fp.close()
    if flags == 3:
        os.chdir(target_path)
        fj = open("filelist.f", "w")
        fj.write("-f "+ os.path.abspath(os.path.dirname("filelist_defines.f")).replace("\\", "/") +"/filelist_defines.f"+ "\n")
        fj.write("-f "+ os.path.abspath(os.path.dirname("filelist_modules.f")).replace("\\", "/") + '/filelist_modules.f' + "\n")
        fj.write("-f "+ os.path.abspath(os.path.dirname("filelist_uvm.f")).replace("\\", "/") + '/filelist_uvm.f' + "\n")
        fj.close()


def makefile_src_gen(target_path, name):
    path = make_sim_dic(target_path,name)
    os.chdir(path)
    # str = "vcs +v2k -timescale=1ns/1ps -debug_all -rdynamic\n"
    fp = open("makefile", "w")
    fp.write("OUTPUT = " + name + "TB\n")
    fp.write("export name = ${OUTPUT}\n")
    fp.write("VCS:\n")
    # fp.write("\tvcs -full64 +v2k -timescale=1ns/1ps -debug_all -LDFLAGS -rdynamic  ")
    fp.write("\tvcs  +acc +vpi  -full64 +v2k -sverilog +incdir+"+r"${UVM_HOME}/src  ${UVM_HOME}/src/uvm_pkg.sv ${UVM_HOME}/src/dpi/uvm_dpi.cc -CFLAGS -DVCS -lca -kdb -timescale=1ns/1ps -debug_all -LDFLAGS -rdynamic  ")
    fp.write(r"-P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ")
    fp.write(r"${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a ")
    fp.write(r" -f filelist.f  -l sim.log" + " ./" + name + "TB.sv\n")
    str = "VERDI:\n\tverdi -f file_list.f " + r"-ssf ${OUTPUT}.fsdb -nologo  -l v.log " + "\n"
    fp.write(str)
    # str = "SIM:\n\t"+r"./${OUTPUT}  -ucli -i" +  " ./run.scr  + fsdb + autoflush  -l sim.log" + "\n"
    str = "SIM:\n\t" + r"./simv  +UVM_TESTNAME=case0 -gui=verdi -i  "+ " ./run.scr  +fsdbfile+" + r"${OUTPUT}.fsdb" " + autoflush  -l sim.log" + "\n"
    fp.write(str)
    str = "SIM_NO_GUI:\n\t" + r"./simv  +UVM_TESTNAME=case0  -l sim.log" + "\n"
    fp.write(str)
    str = "CLEAN:\n\t" + "rm -rf  ./verdiLog  ./dff ./csrc *.daidir *log *.vpd *.vdb simv* *.key *race.out* *.rc *.fsdb *.vpd *.log *.conf *.dat *.conf\n"
    fp.write(str)
    str = "TEST: VCS SIM\n"
    fp.write(str)
    str = "CASE: VCS SIM_NO_GUI"
    fp.write(str)
    fp.close()
    fp = open("run.scr", "w")
    str = "global env\n#fsdbDumpfile " + '"$env(name).fsdb"\n' + 'fsdbDumpvars 0 "$env(name)" \nrun'
    fp.write(str)
    fp.close()


def file_inst(dic, name):
    os.chdir(os.path.dirname(__file__))
    path = find_file(dic, name)
    fp = open(path, "r+", errors='ignore')
    lines = fp.readlines()
    fp.close()
    fp = open(path + '.bak', 'w', errors='ignore')
    fp.writelines(lines)
    fp.close()
    fp = open(path, "w+")
    for lineT in lines:
        resTemp = re.search('(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s+(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s*\(/\*inst\*/\)', lineT)
        if resTemp is not None:
            # fp.write(resTemp.group(1) + " " + resTemp.group(2) + " " + r"(" + "\n")
            ports = find_port(find_file(dic, resTemp.group(1)),resTemp.group(1))
            lenStr = 0
            for port in ports[0]:
                if len(port[3]) > lenStr:
                    lenStr = len(port[3])
            for para in ports[1]:
                if len(para) > lenStr:
                    lenStr = len(para)
            if len(ports[1]) != 0:
                fp.write(resTemp.group(1) + " #(\n")
                for para in ports[1]:
                    if para == ports[1][len(ports[1]) - 1]:
                        fp.write(" " * 8 + r"." + para+ " " * (lenStr + 2 - len(para)) + r"())" + "\n")
                    else:
                        fp.write(" " * 8 + r"." + para+ " " * (lenStr + 2 - len(para)) + r"()," + "\n")
                fp.write(" " * len(resTemp.group(1)) + " " + resTemp.group(2) + " " + r"(" + "\n")
            else:
                fp.write(resTemp.group(1) + " " + resTemp.group(2) + " " + r"(" + "\n")

                    # print(lenStr)

            for port in ports[0]:
                if port == ports[0][len(ports[0]) - 1]:
                    fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"());" + r"//" + port[
                        0] + " " * (8 - len(port[0])) + port[2] + "\n")
                else:
                    fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"() ," + r"//" + port[
                        0] + " " * (8 - len(port[0])) + port[2] + "\n")
        else:
            fp.write(lineT)
    fp.close()


def tb_inst(SourceDic, TargetDic, name):
    os.chdir(os.path.dirname(__file__))
    path = find_file(SourceDic, name)
    # print(path)
    ports = find_port(path,name) #注意此处ports是一个二维的列表
    os.chdir(TargetDic)
    if not os.path.isfile(name + r"TB.sv"):
        fp = open(name + r"TB.sv", "w+")
        fp.write("`include \"uvm_macros.svh\"\n")
        fp.write("import uvm_pkg::*;\n")
        fp.write("module " + name + "TB;\n")
        fp.write(name+"_interface "+name+"_if();\n")
        fp.write("logic clk;\n")
        fp.write("logic rst_n;\n")
        # fp.write(name + " " + name + "Inst(\n")
        
        lenStr = 0
        for port in ports[0]:
            if len(port[3]) > lenStr:
                lenStr = len(port[3])
        for para in ports[1]:
            if len(para) > lenStr:
                lenStr = len(para)
        if len(ports[1]) != 0:
            fp.write(name + " #(\n")
            for para in ports[1]:
                if para == ports[1][len(ports[1]) - 1]:
                    fp.write(" " * 8 + r"." + para+ " " * (lenStr + 2 - len(para)) + r"())" + "\n")
                else:
                    fp.write(" " * 8 + r"." + para+ " " * (lenStr + 2 - len(para)) + r"()," + "\n")
            fp.write(" " * len(name) + " " + name+"_inst" + " " + r"(" + "\n")
        else:
            fp.write(name + " " + name+"_inst" + " " + r"(" + "\n")

                # print(lenStr)

        for port in ports[0]:
            if port == ports[0][len(ports[0]) - 1]:
                fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"("+name+"_if.ifo." + port[3] + " " * (
                        lenStr - len(port[3])) + "));" + r"//" + port[
                    0] + " " * (8 - len(port[0])) + port[2] + "\n")
            else:
                fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"("+name+"_if.ifo." + port[3] + " " * (
                        lenStr - len(port[3])) + ") ," + r"//" + port[
                    0] + " " * (8 - len(port[0])) + port[2] + "\n")




        # for port in ports:
        #     if len(port[3]) > lenStr:
        #         lenStr = len(port[3])
        #         # print(lenStr)
        # for port in ports:
        #     if port == ports[len(ports) - 1]:
        #         fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(if.ifo." + port[3] + " " * (
        #                 lenStr - len(port[3])) + "));" + r"//" + port[0] + " " * (8 - len(port[0])) + port[
        #                      2] + "\n")
        #     else:
        #         fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(if.ifo." + port[3] + " " * (
        #                 lenStr - len(port[3])) + ") ," + r"//" + port[0] + " " * (8 - len(port[0])) + port[
        #                      2] + "\n")

        fp.write("initial begin\n")
        fp.write("clk = 0;\n")
        fp.write("rst_n = 0;\n")
        fp.write("#8 rst_n = 0;\n")
        fp.write("\n")
        fp.write("end\n\n\n")

        fp.write("always #5 clk = ~clk;\n\n")


        fp.write("always@ * begin\n")
        fp.write("\n\n\nend\n\n")

        fp.write("initial begin\n")
        fp.write("   run_test();\n")
        fp.write("end\n")


        fp.write("initial begin\n")
        fp.write("   uvm_config_db#(virtual "+name+"_interface)::set(null, \"uvm_test_top.env.i_agt.drv\", \"vif\", "+name+"_if);\n")
        fp.write("   uvm_config_db#(virtual "+name+"_interface)::set(null, \"uvm_test_top.env.i_agt.mon\", \"vif\", "+name+"_if);\n")
        fp.write("   uvm_config_db#(virtual "+name+"_interface)::set(null, \"uvm_test_top.env.o_agt.mon\", \"vif\", "+name+"_if);\n")
        fp.write("end\n")
        fp.write("\n\n\n\n\nendmodule\n")
        fp.close()
    else:
        print("file exists")
    return name + r"TB"


def make_sim_dic(targetPath, name):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    # str = "../sim/"
    str = targetPath
    if not os.path.isdir(str):
        print("creat "+targetPath + "/path")
        os.makedirs(str)
    if not os.path.isdir(str + name + "Test"):
        print("creat "+targetPath +name+"Test path")
        os.makedirs(str + name + "Test")
    return os.path.normpath(os.path.abspath(str + name + r"Test/")).replace("\\", "/")



def interface_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    file_path = find_file(Source_path,name)
    ports = find_port(file_path,name)
    interface_path = make_sim_dic(TargetPath,name) 
    os.chdir(interface_path)
    fj = open(name+"_interface_port.sv","w")
    fj.write("interface "+name+"_interface_port;\n" )
    if flag==1:
        fq = open(name+"_interface_inner.sv","w")
        fp = open(name+"_interface.sv","w")
        fp.write("interface "+name+"_interface;\n" )
        fp.write(name+"_interface_port ifo();\n")
        fp.write(name+"_interface_inner ifi();\n")
        fp.write("\n\n\n\nendinterface")
        fq.write("interface "+name+"_interface_inner;\n" )
        fq.write("\n\n\n\nendinterface")
        fq.close()
    for port in ports[0]:
        fj.write("logic " + port[2] + (0 if len(port[2]) == 0 else 1) * " " + port[3] + ";\n")
    fj.write("\n\n\n\nendinterface")
    fj.close()

def transaction_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_transaction.sv","w")
    fp.write("import uvm_pkg::*;\n")
    fp.write("class "+name+"_transaction extends uvm_sequence_item;\n")
    fp.write("\n\n\nconstraint con{\n\n\n}\n")
    fp.write("`uvm_object_utils("+name+"_transaction)\n")
    fp.write("function new(string name = \""+name+"_transaction\");\nsuper.new();\nendfunction\n")
    fp.write("endclass\n")
    fp.close()


def sequencer_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_sequencer.sv","w")
    fp.write("class "+name+"_sequencer extends uvm_sequencer #("+ name +"_transaction);\n")
    fp.write("    function new(string name, uvm_component parent);\n        super.new(name, parent);\n    endfunction \n")
    fp.write("    `uvm_component_utils("+name+"_sequencer)\n")
    fp.write("endclass\n")
    fp.close()

def scoreboard_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    write_str = re.sub("my",name,open("./uvm/my_scoreboard.sv","r").read())
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_scoreboard.sv","w")
    fp.write(write_str)
    fp.close()

def monitor_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    write_str = re.sub("my",name,open("./uvm/my_monitor.sv","r").read())
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_monitor.sv","w")
    fp.write(write_str)
    fp.close()

def model_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    write_str = re.sub("my",name,open("./uvm/my_model.sv","r").read())
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_model.sv","w")
    fp.write(write_str)
    fp.close()

def env_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    write_str = re.sub("my",name,open("./uvm/my_env.sv","r").read())
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_env.sv","w")
    fp.write(write_str)
    fp.close()

def drive_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    write_str = re.sub("my",name,open("./uvm/my_driver.sv","r").read())
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_driver.sv","w")
    fp.write(write_str)
    fp.close()

def case_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    write_str = re.sub("my",name,open("./uvm/my_case0.sv","r").read())
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_case0.sv","w")
    fp.write(write_str)
    fp.close()

def agent_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    write_str = re.sub("my",name,open("./uvm/my_agent.sv","r").read())
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_agent.sv","w")
    fp.write(write_str)
    fp.close()

def base_test_gen(Source_path,TargetPath,name,flag):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    write_str = re.sub("my",name,open("./uvm/base_test.sv","r").read())
    path = make_sim_dic(TargetPath,name)
    os.chdir(path)
    fp = open(name+"_base_test.sv","w")
    fp.write(write_str)
    fp.close()


def sim_gen(dic, name):
    TargetPath = make_sim_dic(name)
    tb_inst(dic, TargetPath, name)

#   flag_tb指示是否为sim文件，flag_tb1:1-重新生成base_test filelist; 5-重新生成三个uvmfilelist flag_dicmake为是否创造路径，flags指示：1,3写define_filelist;2,3写module_filelist;3写filelist； 
#   flag1指示是否写入本文件路径 


def filelist_regen(flag_tb,flag_tb1,flag_dicmake,flags,flag1,sourcePath,targetPath,name):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    search_path = sourcePath
    path = find_file(search_path,name)
    if flag_dicmake==1:
        real_targetPath = make_sim_dic(targetPath, name)
    else:
        real_targetPath = os.path.dirname(path)
    if flag_tb == 1:
        filelist_gen([targetPath],real_targetPath,name+"_base_test",flag_tb1,1)
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    filelist_gen(search_path,real_targetPath,name,flags,flag1)


def simflow(sourcePath, targetPath, name):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    # SourcePath = "../code/"
    targetpath = make_sim_dic(targetPath, name)
    TB = tb_inst(sourcePath, targetpath, name)
    # makefile_src_gen(targetpath, name)
    # # tb_inst(path,targetpath,"uart_byte_tx")
    # filelist_gen(sourcePath, targetpath, TB)
    flag = 1
    makefile_src_gen(targetPath,name)
    base_test_gen(sourcePath,targetPath,name,flag)
    agent_gen(sourcePath,targetPath,name,flag)
    case_gen(sourcePath,targetPath,name,flag)
    drive_gen(sourcePath,targetPath,name,flag)
    env_gen(sourcePath,targetPath,name,flag)
    interface_gen(sourcePath,targetPath,name,flag)
    model_gen(sourcePath,targetPath,name,flag)
    monitor_gen(sourcePath,targetPath,name,flag)
    scoreboard_gen(sourcePath,targetPath,name,flag)
    sequencer_gen(sourcePath,targetPath,name,flag)
    transaction_gen(sourcePath,targetPath,name,flag)
    filelist_regen(1,5,1,3,1,sourcePath,targetPath,name)







if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    SourcePath = ["../rtl/"]
    TargetPath = "../sim/"
    name = "gmec_core"
    # TargetPath = make_sim_dic(TargetPath, name)

    simflow(SourcePath,TargetPath,name)
    # filelist_gen([SourcePath], TargetPath, "top", 3)
    # filelist_gen(SourcePath,TargetPath, name,3, 0)
    # file_inst(SourcePath, 'test')
    # targetpath = make_sim_dic("Top")
    # makefile_src_gen(targetpath,"Top")
    # filelist_gen(path,targetpath,"uart_byte_txTB")
