import os
import re
# path = "../verilog_python"
keyword=['always','and','assign','begin','buf','bufif0','bufif1','case','casex','casez','cmos','deassign','default',
'defparam','disable','edge','else','end','endcase','endmodule','endfunction','endprimitive','endspecify',
'endtable','endtask','event','for','force','forever','fork','function','highz0','highz1','if','initial',
'inout','input','integer','join','large','macromodule','medium','module','nand','negedge','nmos','nor','not','notif0',
'notifl','or','output','parameter','pmos','posedge','primitive','pull0','pull1','pullup','pulldown','rcmos',
'reg','releses','repeat','mmos','rpmos','rtran','rtranif0','rtranif1','scalared','small','specify','specparam',
'strength','strong0','strong1','supply0','supply1','table','task','time','tran','tranif0','tranif1','tri',
'tri0','tri1','triand','trior','trireg','vectored','wait','wand','weak0','weak1','while','wire','wor','xnor','xor']
path = "/home/IC/xsc"
filename = "fifo_ctr"
def find_port(filename):
    ports = []
    fd = open(filename,errors='ignore')
    # result = 
    str = fd.read()
    result = re.findall('(input|output)\s+(wire|reg)?\s*(\[.*?\])?\s*(\w+)',str)
    for res in result:
        # print(res)
        portTemp = [res[0],res[1],res[2],res[3]]
        ports.append(portTemp)
    # for line in fd.readlines():
    #     result = re.findall('(input|output)\s+(wire|reg)?\s*(\[.*?\])?\s+(\w+)',line,re.M)
    #     if(len(result) != 0):
    #         portTemp = [result[0][0],result[0][1],result[0][2],result[0][3]]
    #         ports.append(portTemp)
    # print(ports)
    return ports
def find_module(path):
    # print(path)
    fp = open(path,"r",errors="ignore")
    str = fp.read()
    modules = []
    result = re.findall('(\w+)\s+(\w+)\s*\(',str)
    for item in result:
        if((item[0] not in keyword) and (item[1] not in keyword)):
            # print(item)
            modules.append(item[0])

    return modules
    # for line in fp.readlines():
    #     result = re.findall('(\w+)\s+(\w+)\s*\(',line)
    # print(result)
def find_file(start, name):
    # print(start)
    for relpath, dirs, files in os.walk(start):
        for File in files:
            # print(File)
            if(re.match(name + '.s?v$',File) != None):
                full_path = os.path.join(relpath, File)
                # print(full_path)
                return os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")

def filelist_gen(source_path,target_path,name):
    path = find_file(source_path,name)
    # print(path)
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
                dic = find_file(source_path,list)
                # print(dic)
                modules = find_module(dic)
                # print(modules)
                if(len(modules) != 0):
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
        # print(list_temp)
        # print(lists)
        # print(list_pass)
    os.chdir(target_path)
    fp = open("filelist.f","w")
    for list in lists:
        # print(list)
        fp.write(find_file(source_path,list) + "\n")
    fp.close()

def makefile_src_gen(target_path,name):
    os.chdir(target_path)
    # str = "vcs +v2k -timescale=1ns/1ps -debug_all -rdynamic\n"
    fp = open("makefile","w")
    fp.write("OUTPUT = " + name + "TB\n")
    fp.write("export name = ${OUTPUT}\n")
    fp.write("VCS:\n") 
    # fp.write("\tvcs -full64 +v2k -timescale=1ns/1ps -debug_all -LDFLAGS -rdynamic  ")
    fp.write("\tvcs -full64 +v2k -lca -kdb -timescale=1ns/1ps -debug_all -LDFLAGS -rdynamic  ")
    fp.write(r"-P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ")
    fp.write(r"${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a ")
    fp.write(r" -f filelist.f -o ${OUTPUT} -l sim.log"+" ./"+ name + "TB.sv\n")
    str = "VERDI:\n\tverdi -f file_list.f "+r"-ssf ${OUTPUT}.fsdb -nologo  -l v.log " + "\n"
    fp.write(str)
    # str = "SIM:\n\t"+r"./${OUTPUT}  -ucli -i" +  " ./run.scr  + fsdb + autoflush  -l sim.log" + "\n"
    str = "SIM:\n\t"+r"./${OUTPUT}  -gui=verdi -i" +  " ./run.scr  + fsdb + autoflush  -l sim.log" + "\n"
    fp.write(str)
    str = "CLEAN:\n\t"+ "rm -rf  ./verdiLog  ./dff ./csrc *.daidir *log *.vpd *.vdb simv* *.key *race.out* *.rc *.fsdb *.vpd *.log *.conf *.dat *.conf"
    fp.write(str)
    fp.close()
    fp = open("run.scr","w")
    str = "global env\nfsdbDumpfile "+'"$env(name).fsdb"\n'+'fsdbDumpvars 0 "$env(name)" \nrun 10000ns'
    fp.write(str)
    fp.close()





def file_inst(dic, name):
    os.chdir(os.path.dirname(__file__)) 
    path = find_file(dic, name)
    # print(path)
    fp = open(path,"r+",errors='ignore')
    lines = fp.readlines()
    fp.close()
    fp = open(path,"w+")
    for lineT in lines:
        resTemp = re.search('(\w+)\s+(\w+)\s*\(/\*inst\*/\)',lineT) 
        if(resTemp != None):
            fp.write(resTemp.group(1)+" "+resTemp.group(2) +" "+r"(" + "\n")
            ports = find_port(find_file(dic, resTemp.group(1)))
            lenStr = 0
            for port in ports:
                if(len(port[3]) > lenStr):
                    lenStr = len(port[3])
                    # print(lenStr)
            for port in ports:
                if(port == ports[len(ports) - 1]):
                    fp.write(" " * 8 + r"."+port[3] +" "*(lenStr + 2 - len(port[3])) + r"());" + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")
                else:
                    fp.write(" " * 8 + r"."+port[3] +" "*(lenStr + 2 - len(port[3])) + r"() ," + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")
        else:
            fp.write(lineT)
    fp.close()

def tb_inst(SourceDic,TargetDic, name):
    path = find_file(SourceDic , name)
    # print(path)
    ports = find_port(path)
    os.chdir(TargetDic)
    if not os.path.isfile(name + r"TB.sv"):
        fp = open(name + r"TB.sv","w+")
        fp.write("module " + name + "TB;\n")
        for port in ports:
            fp.write("logic " + port[2] + ( 0 if len(port[2]) == 0 else 1) * " " +  port[3] + ";\n")
        fp.write(name + " " + name + "Inst(\n")
        lenStr = 0
        for port in ports:
            if(len(port[3]) > lenStr):
                lenStr = len(port[3])
                # print(lenStr)
        for port in ports:
            if(port == ports[len(ports) - 1]):
                fp.write(" " * 8 + r"."+port[3] +" "*(lenStr + 2 - len(port[3])) + r"(" +port[3] + " "*(lenStr - len(port[3])) + "));" + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")
            else:
                fp.write(" " * 8 + r"."+port[3] +" "*(lenStr + 2 - len(port[3])) + r"(" +port[3] + " "*(lenStr - len(port[3]))+ ") ," + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")
        
        fp.write("initial begin\n")
        fp.write("\n")
        fp.write("end\n")
        fp.write("\n\n\n\n\nendmodule\n")
        fp.close()
    else:
        print("file exists")

def make_sim_dic(name):
    os.chdir(os.path.dirname(__file__)) 
    # path = findfile(dic , name)
    # print(path)
    # ports = findport(path)
    if not os.path.isdir("./sim"):
        os.makedirs("./sim")
    if not os.path.isdir("./sim/" + name + "Test"):
        os.makedirs("./sim/" + name + "Test")
    # return ("./sim/" + name + "Test")
    return os.path.normpath(os.path.abspath("./sim/" + name + "Test")).replace("\\", "/")
    os.chdir("./sim/" + name + "Test")
    # if not os.path.isfile(name + r"TB.sv"):
    #     fp = open(name + r"TB.sv","w+")
    #     fp.write("module " + name + "TB;\n")
    #     for port in ports:
    #         fp.write("logic " + port[2] + ( 0 if len(port[2]) == 0 else 1) * " " +  port[3] + ";\n")
    #     fp.write(name + " " + name + "Inst(\n")
    #     lenStr = 0
    #     for port in ports:
    #         if(len(port[3]) > lenStr):
    #             lenStr = len(port[3])
    #             # print(lenStr)
    #     for port in ports:
    #         if(port == ports[len(ports) - 1]):
    #             fp.write(" " * 8 + r"."+port[3] +" "*(lenStr + 2 - len(port[3])) + r"(" +port[3] + " "*(lenStr - len(port[3])) + "));" + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")
    #         else:
    #             fp.write(" " * 8 + r"."+port[3] +" "*(lenStr + 2 - len(port[3])) + r"(" +port[3] + " "*(lenStr - len(port[3]))+ ") ," + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")
        
    #     fp.write("initial begin\n")
    #     fp.write("\n")
    #     fp.write("end\n")
    #     fp.write("\n\n\n\n\nendmodule\n")
    #     fp.close()
    # else:
    #     print("file exists")
    
def sim_gen(dic,name):
    TargetPath = make_sim_dic(name)
    tb_inst(dic,TargetPath,name)


if __name__ ==  '__main__':
    # path = findfile(path, filename)
    # print(path)
    # path = path.replace("\\", "/")
    # print(path)
    # ports = findport(path)
    # fileInst(path, "test")
    # sim_gen(path,"fifo_ctr")
    # path = find_file(path,"test")
    targetpath = make_sim_dic("uart_byte_tx")
    makefile_src_gen(targetpath,"uart_byte_tx")
    # print(targetpath)
    # print(targetpath)
    # tb_inst(path,targetpath,"uart_byte_tx")
    filelist_gen(path,targetpath,"uart_byte_txTB")
    # fp = open("/home/IC/xsc/python_pro/verilog_python/code/encryption/crypto_engine_reg.v","r")
    # find_file("/home/IC/xsc","axi_top")
    # print(find_module(path))