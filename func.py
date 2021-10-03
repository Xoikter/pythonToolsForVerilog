import os
import re

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
           'wor', 'xnor', 'xor']
# path = "/home/IC/xsc"
filename = "fifo_ctr"


def find_port(filename,name):
    ports = []
    parameters = []
    fd = open(filename, errors='ignore')
    # result = 
    str = fd.read()
    str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
    # str_temp = re.sub(r'//.*',"",str_temp)
    str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
    str_temp = re.sub("\\bfunction\\b[\s\S]*?\bendfunction\\b", "", str_temp)
    str_temp = re.search("\\bmodule\\b\s*\\b" + name + "\\b.*?endmodule", str_temp, flags=re.S).group()
    str_temp = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", str_temp)
    str_temp = re.sub("\\binterface\\b.*?;", "", str_temp, flags=re.S)
    str_port = re.search("\\bmodule.*?;",str_temp,flags=re.S).group()
    result = re.findall('\\b(input|output)\\b\s*\\b(wire|reg)?\\b\s*(\[.*?\])?\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)', str_port, flags=re.S)
    res_para = re.findall('\\bparameter\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)(\s*=)',str_port,flags=re.S)
    for res in res_para:
        para_temp = res[0]
        parameters.append(para_temp)
    for res in result:
        portTemp = [res[0], res[1], res[2], res[3]]
        ports.append(portTemp)
    str_temp = re.sub("\\bmodule.*?;","",str_temp,flags=re.S)
    result = re.findall('\\b(input|output)\\b\s*\\b(wire|reg)?\\b\s*(\[.*?\])?\s*(.*?)\s*;', str_temp, flags=re.S)
    res_para = re.findall('\\bparameter\\b\s*(.*?)\s*;',str_temp,flags=re.S);
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
    result = re.findall("`(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)", str_temp)
    for item in result:
        if item not in keyword:
            defines.append(item)
    return defines


def find_define_file(path, define_word):
    out_path = ""
    for start in path:
        for relpath, dirs, files in os.walk(start):
            for File in files:
                if re.match('.+\.s?v', File) is not None:
                    fp = open(os.path.join(relpath, File), "r", errors="ignore")
                    str = fp.read()
                    str_temp = re.sub("\/\*[\s\S]*?\*\/", "", str)
                    # str_temp = re.sub(r'//.*$',"",str_temp)
                    str_temp = re.sub('//[\s\S]*?\n', "", str_temp)
                    # print(File)
                    # if(re.match(name + '.s?v$',File) != None):
                    if re.search('`define\s*(\\b'+define_word+'\\b)', str_temp) is not None:
                        full_path = os.path.join(relpath, File)
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
    return out_path


def find_module(path):
    # print(path)
    fp = open(path, "r", errors="ignore")
    str = fp.read()
    str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
    # str_temp = re.sub(r'//.*',"",str_temp)
    str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)

    modules = []
    result = re.findall('(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s+(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s*\(', str_temp)
    for item in result:
        if (item[0] not in keyword) and (item[1] not in keyword):
            # print(item)
            modules.append(item[0])

    return modules
    # for line in fp.readlines():
    #     result = re.findall('(\w+)\s+(\w+)\s*\(',line)
    # print(result)


def find_file(starts, name):
    # print(start)
    out_path = ""
    for start in starts:
        for relpath, dirs, files in os.walk(start):
            for File in files:
                if re.match('.+\.s?v$', File) is not None:
                    fp = open(os.path.join(relpath, File), "r", errors="ignore")
                    str = fp.read()
                    str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
                    # str_temp = re.sub(r'//.*',"",str_temp)
                    str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)

                    # print(File)
                    # if(re.match(name + '.s?v$',File) != None):
                    if re.search('\\b(module|interface|class|program)\\b\s*' + name + '\\b', str_temp) is not None:
                        full_path = os.path.join(relpath, File)
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
    return out_path


def filelist_gen(source_path, target_path, name, flags,flag1):
    os.chdir(os.path.dirname(__file__))
    path = find_file(source_path, name)
    defines = find_define(path)
    lists_root = []
    for item in defines:
        define_files = find_define_file(source_path, item)
        if define_files not in lists_root:
            lists_root.append(define_files)

    # print(path)
    # print(name)
    lists = find_module(path)
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
            if list not in list_pass:
                dic = find_file(source_path, list)
                defines_temp = find_define(path)
                for item in defines:
                    define_files = find_define_file(source_path, item)
                    if define_files not in lists_root:
                        lists_root.append(define_files)
                # print(dic)
                modules = find_module(dic)
                # print(modules)
                if len(modules) != 0:
                    flag = 1
                    # print(flag)
                    for module in modules:
                        if module not in lists:
                            list_temp.append(module)

                # if(len(modules) != 0):
                #     flag = 1
                #     list_temp.extend(modules)
            if list not in list_temp:
                list_temp.append(list)
            if list not in list_pass:
                list_pass.append(list)
        lists = list_temp


    os.chdir(target_path)
    if flags == 1 or flags == 3:
        os.chdir(target_path)
        fq = open("filelist_defines.f", "w")
        for item in lists_root:
            fq.write(item + "\n")
        if flag1== 1:
            fq.write(path + "\n")
        fq.close()
        # lists = lists_root + lists
    if flags == 2 or flags == 3:
        fp = open("filelist_modules.f", "w")
        os.chdir(os.path.dirname(__file__))
        for list in lists:
            fp.write(find_file(source_path, list) + "\n")
        if flag1 == 1:
            fp.write(path + "\n")
        fp.close()
    if flags == 3:
        os.chdir(target_path)
        fj = open("filelist.f", "w")
        fj.write(os.path.abspath(os.path.dirname("filelist_defines")).replace("\\", "/") +"/filelist_defines"+ "\n")
        fj.write(os.path.abspath(os.path.dirname("filelist_modules")).replace("\\", "/") + '/filelist_modules' + "\n")
        fj.close()


def makefile_src_gen(target_path, name):
    os.chdir(target_path)
    # str = "vcs +v2k -timescale=1ns/1ps -debug_all -rdynamic\n"
    fp = open("makefile", "w")
    fp.write("OUTPUT = " + name + "TB\n")
    fp.write("export name = ${OUTPUT}\n")
    fp.write("VCS:\n")
    # fp.write("\tvcs -full64 +v2k -timescale=1ns/1ps -debug_all -LDFLAGS -rdynamic  ")
    fp.write("\tvcs -full64 +v2k -sverilog -lca -kdb -timescale=1ns/1ps -debug_all -LDFLAGS -rdynamic  ")
    fp.write(r"-P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ")
    fp.write(r"${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a ")
    fp.write(r" -f filelist.f  -l sim.log" + " ./" + name + "TB.sv\n")
    str = "VERDI:\n\tverdi -f file_list.f " + r"-ssf ${OUTPUT}.fsdb -nologo  -l v.log " + "\n"
    fp.write(str)
    # str = "SIM:\n\t"+r"./${OUTPUT}  -ucli -i" +  " ./run.scr  + fsdb + autoflush  -l sim.log" + "\n"
    str = "SIM:\n\t" + r"./simv  -gui=verdi -i" + " ./run.scr  +fsdbfile+" + r"${OUTPUT}.fsdb" " + autoflush  -l sim.log" + "\n"
    fp.write(str)
    str = "CLEAN:\n\t" + "rm -rf  ./verdiLog  ./dff ./csrc *.daidir *log *.vpd *.vdb simv* *.key *race.out* *.rc *.fsdb *.vpd *.log *.conf *.dat *.conf\n"
    fp.write(str)
    str = "TEST: VCS SIM"
    fp.write(str)
    fp.close()
    fp = open("run.scr", "w")
    str = "global env\n#fsdbDumpfile " + '"$env(name).fsdb"\n' + 'fsdbDumpvars 0 "$env(name)" \nrun 10000ns'
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
    ports = find_port(path) #注意此处ports是一个二维的列表
    os.chdir(TargetDic)
    if not os.path.isfile(name + r"TB.sv"):
        fp = open(name + r"TB.sv", "w+")
        fp.write("module " + name + "TB;\n")
        for port in ports:
            fp.write("logic " + port[2] + (0 if len(port[2]) == 0 else 1) * " " + port[3] + ";\n")
        fp.write(name + " " + name + "Inst(\n")
        lenStr = 0
        for port in ports:
            if len(port[3]) > lenStr:
                lenStr = len(port[3])
                # print(lenStr)
        for port in ports:
            if port == ports[len(ports) - 1]:
                fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + port[3] + " " * (
                        lenStr - len(port[3])) + "));" + r"//" + port[0] + " " * (8 - len(port[0])) + port[
                             2] + "\n")
            else:
                fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + port[3] + " " * (
                        lenStr - len(port[3])) + ") ," + r"//" + port[0] + " " * (8 - len(port[0])) + port[
                             2] + "\n")

        fp.write("initial begin\n")
        fp.write("\n")
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
        os.makedirs(str)
    if not os.path.isdir(str + name + "Test"):
        os.makedirs(str + name + "Test")
    return os.path.normpath(os.path.abspath(str + name + r"Test/")).replace("\\", "/")


def sim_gen(dic, name):
    TargetPath = make_sim_dic(name)
    tb_inst(dic, TargetPath, name)


def simflow(sourcePath, targetPath, name):
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    # SourcePath = "../code/"
    targetpath = make_sim_dic(targetPath, name)
    TB = tb_inst(sourcePath, targetpath, name)
    makefile_src_gen(targetpath, name)
    # tb_inst(path,targetpath,"uart_byte_tx")
    filelist_gen(sourcePath, targetpath, TB)


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    SourcePath = "./code/"
    TargetPath = "./sim/"
    TargetPath = make_sim_dic(TargetPath, "VFU_Int_top")
    # filelist_gen([SourcePath], TargetPath, "top", 3)
    filelist_gen(['E:/xsc/pro/git_pro/pythonToolsForVerilog/code/'],TargetPath, "VFU_Int_top",3, 0)
    # file_inst(SourcePath, 'test')
    # targetpath = make_sim_dic("Top")
    # makefile_src_gen(targetpath,"Top")
    # filelist_gen(path,targetpath,"uart_byte_txTB")
