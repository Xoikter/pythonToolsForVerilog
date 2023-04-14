import os
import re
import threading
import random
from queue import Queue

# import uvm_gen as ug
from file_analyse import File_analyse as fa


# path = "../verilog_python"
class Verilog_tools:
    def __init__(self,name,agent_in_num,agent_out_num):
        self.keyword = ['always', 'and', 'assign', 'begin', 'buf', 'bufif0', 'bufif1', 'case', 'casex', 'casez', 'cmos',
                        'deassign',
                        'default',
                        'defparam', 'disable', 'edge', 'else', 'end', 'endcase', 'endmodule', 'endfunction',
                        'endprimitive',
                        'endspecify',
                        'endtable', 'endtask', 'event', 'for', 'force', 'forever', 'fork', 'function', 'highz0',
                        'highz1', 'if',
                        'initial',
                        'inout', 'input', 'integer', 'join', 'large', 'macromodule', 'medium', 'module', 'nand',
                        'negedge', 'nmos',
                        'nor', 'not', 'notif0',
                        'notifl', 'or', 'output', 'parameter', 'pmos', 'posedge', 'primitive', 'pull0', 'pull1',
                        'pullup',
                        'pulldown', 'rcmos',
                        'reg', 'releses', 'repeat', 'mmos', 'rpmos', 'rtran', 'rtranif0', 'rtranif1', 'scalared',
                        'small', 'specify',
                        'specparam',
                        'strength', 'strong0', 'strong1', 'supply0', 'supply1', 'table', 'task', 'time', 'tran',
                        'tranif0',
                        'tranif1', 'tri',
                        'tri0', 'tri1', 'triand', 'trior', 'trireg', 'vectored', 'wait', 'wand', 'weak0', 'weak1',
                        'while', 'wire',
                        'wor', 'xnor', 'xor', 'extends', 'uvm_report_server', 'int', 'void', 'virtual', 'new',
                        'uvm_analysis_port', 'super'
            , 'extern0', "uvm_component_utils", "type_id", 'bit', 'byte', 'unsiged', 'shortint', 'longint', 'timer',
                        'real', 'interface', 'class',
                        'logic', 'genvar', 'uvm_tlm_analysis_fifo', 'uvm_blocking_get_port', 'constraint', 'import',
                        'uvm_active_passive_enum', 'define', 'undef'
            , 'ifdef', 'elsif', 'endif', "uvm_object_utils_begin", "uvm_object_utils_end"]
        # path = "/home/IC/xsc"
        self.filename = name
        self.rtl_filemap = {}
        self.rtl_definemap = {}
        self.test_filemap = {}
        self.test_definemap = {}
        # except_module = ['assert_never_unknown']
        self.except_module = []
        self.mapGenFlag = False
        self.SourcePath = []
        self.TargetPath = ""
        self.moduleFound = []
        self.build_list={}
        self.test_list={}
        self.regress_list={}
        self.sanity_list={}
        self.fa = fa("")
        self.agent_in_num = agent_in_num
        self.agent_out_num = agent_out_num
        self.del_pass = False
        self.max_thread = 150
        self.sem = threading.Semaphore(self.max_thread)
        self.uvm_verbosity="UVM_MEDIUM"


        self.ctree = ["de",
                      "de/filelist",
                      "de/common_ip",
                      "de/rtl",
                      "dv",
                      "dv/simctrl",
                      "dv/vc",
                      "dv/tg",
                      "impl",
                      "fpga",
                      "ip",
                      "doc"
                      ]

        self.makefile = {"de/filelist": open(os.path.dirname(__file__) + "/makefile/makefile_de_filelist", "r",
                                             errors="ignore").read(),
                         "de/rtl": open(os.path.dirname(__file__) + "/makefile/makefile_de_rtl", "r",
                                        errors="ignore").read(),
                         "dv/filelist": open(os.path.dirname(__file__) + "/makefile/makefile_dv_filelist", "r",
                                             errors="ignore").read(),
                         "dv/tg": open(os.path.dirname(__file__) + "/makefile/makefile_dv_uvc", "r",
                                       errors="ignore").read(),
                         "dv/sim": open(os.path.dirname(__file__) + "/makefile/makefile_dv_sim", "r",
                                        errors="ignore").read(),
                         "sim": open(os.path.dirname(__file__) + "/makefile/makefile_sim", "r",
                                        errors="ignore").read()}
        self.config = {
            "dv/tg": open(os.path.dirname(__file__) + "/config/config_dv_tg.txt", "r", errors="ignore").read(),
            "de/rtl": open(os.path.dirname(__file__) + "/config/config_de_rtl.txt", "r", errors="ignore").read()
        }
        self.uvc = {
            # "scoreboard_comb": open(os.path.dirname(__file__) + "/uvm/my_scoreboard_comb.sv", "r", errors="ignore").read(),
            "transaction": open(os.path.dirname(__file__) + "/uvm/my_transaction.sv", "r", errors="ignore").read(),
            "sequencer": open(os.path.dirname(__file__) + "/uvm/my_sequencer.sv", "r", errors="ignore").read(),
            "vsqr": open(os.path.dirname(__file__) + "/uvm/my_vsqr.sv", "r", errors="ignore").read(),
            "driver": open(os.path.dirname(__file__) + "/uvm/my_driver.sv", "r", errors="ignore").read(),
            "monitor": open(os.path.dirname(__file__) + "/uvm/my_monitor.sv", "r", errors="ignore").read(),
            "agent": open(os.path.dirname(__file__) + "/uvm/my_agent.sv", "r", errors="ignore").read(),
            "model": open(os.path.dirname(__file__) + "/uvm/my_model.sv", "r", errors="ignore").read(),
            "scoreboard": open(os.path.dirname(__file__) + "/uvm/my_scoreboard_seq.sv", "r", errors="ignore").read(),
            "env": open(os.path.dirname(__file__) + "/uvm/my_env.sv", "r", errors="ignore").read(),
            "base_test": open(os.path.dirname(__file__) + "/uvm/my_base_test.sv", "r", errors="ignore").read()}
        # "if": open(os.path.dirname(__file__) + "/uvm/my_if.sv", "r", errors="ignore").read(),
        self.tc = {
            "case0": open(os.path.dirname(__file__) + "/uvm/my_case0.sv", "r", errors="ignore").read()
        }
        self.seq_lib = {
            "case0_sequence": open(os.path.dirname(__file__) + "/uvm/my_case0_sequence.sv", "r", errors="ignore").read(),
            "case0_vseq": open(os.path.dirname(__file__) + "/uvm/my_case0_vseq.sv", "r", errors="ignore").read()
        }
        self.build_py = open(os.path.dirname(__file__) + "/build/build.py", "r", errors="ignore").read()
        self.test_list_py = open(os.path.dirname(__file__) + "/test_list/test_list.py", "r", errors="ignore").read()

    def test_map_initial(self):
        for relpath, dirs, files in os.walk(self.TargetPath):
            for File in files:
                if re.match('.+\.s?v$', File) is not None:
                    fp = open(os.path.join(relpath, File), "r", errors="ignore")
                    str = fp.read()
                    str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
                    # str_temp = re.sub(r'//.*',"",str_temp)
                    str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
                    str_temp = re.sub("\$.*?;", "", str_temp, flags=re.S)
                    str_temp = re.sub("\".*?\"", "", str_temp, flags=re.S)
                    full_path = os.path.join(relpath, File)
                    real_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                    module_temp = re.findall(
                        '\\b(module|interface|class|program)\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\\b', str_temp)
                    define_temp = self.fa.find_define_word(str_temp)
                    for item in module_temp:
                        # flag_file = 0
                        if ((item[1] in self.test_filemap) and (
                                real_path.strip() != self.test_filemap[item[1]].strip())):
                            print("find mutidefine module\n" + item[1])
                            print(os.path.normpath(os.path.abspath(full_path)).replace("\\", "/") + " Y ")
                            print(self.test_filemap[item[1]] + " N ")
                            # sel = input("select:")
                            # if sel == "Y":
                            #     self.test_filemap.update({item[1]:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                        elif item[1] not in self.test_filemap:
                            self.test_filemap.update(
                                {item[1]: os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                    for item in define_temp:
                        if ((item[0] in self.test_definemap) and (
                                real_path.strip() != self.test_definemap[item[0]][0].strip())):
                            print("find mutidefine define_word\n" + item[0])
                            print(os.path.normpath(os.path.abspath(full_path)).replace("\\", "/") + " Y ")
                            print(self.test_definemap[item[0]] + " N ")
                            # sel = input("select:")
                            # if sel == "Y":
                            #     self.test_definemap.update({item:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                        elif item[0] not in self.test_definemap:
                            self.test_definemap.update(
                                {item[0]: [os.path.normpath(os.path.abspath(full_path)).replace("\\", "/"), item[1]]})

    def rtl_map_initial(self):
        for start in self.SourcePath:
            # print(start)
            # for relpath, dirs, files in os.walk(self.SourcePath):
            for relpath, dirs, files in os.walk(start):
                for File in files:
                    if re.match('.+\.s?v$', File) is not None:
                        fp = open(os.path.join(relpath, File), "r", errors="ignore")
                        str = fp.read()

                        str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
                        # str_temp = re.sub(r'//.*',"",str_temp)
                        str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
                        str_temp = re.sub("\$.*?;", "", str_temp, flags=re.S)
                        # str_temp = re.sub("\".*?\"","",str_temp,flags=re.S)

                        full_path = os.path.join(relpath, File)
                        real_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                        module_temp = re.findall(
                            '\\b(module|interface|class|program)\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\\b', str_temp)
                        define_temp = self.fa.find_define_word(str_temp)
                        for item in module_temp:
                            # flag_file = 0
                            # if ((item[1]  in self.rtl_filemap) and (real_path.strip() is not self.rtl_filemap[item[1]].strip())):
                            if ((item[1] in self.rtl_filemap) and (real_path != self.rtl_filemap[item[1]])):
                                print("find mutidefine module  " + item[1])
                                print(real_path + " Y ")
                                print(self.rtl_filemap[item[1]] + " N ")
                                # sel = input("select:")
                                # if sel == "Y":
                                #     self.rtl_filemap.update({item[1]:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                            elif item[1] not in self.rtl_filemap:
                                self.rtl_filemap.update(
                                    {item[1]: os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})

                        for item in define_temp:
                            if ((item[0] in self.rtl_definemap) and (
                                    real_path.strip() != self.rtl_definemap[item[0]][0].strip())):
                                print("find mutidefine define_word  " + item[0])
                                # print(real_path + " Y ")
                                # print(self.rtl_definemap[item] + " N ")
                                # sel = input("select:")
                                # if sel == "Y":
                                #     self.rtl_definemap.update({item:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                            elif item[0] not in self.rtl_definemap:
                                self.rtl_definemap.update({item[0]: [
                                    os.path.normpath(os.path.abspath(full_path)).replace("\\", "/"), item[1]]})
                                # self.filemap[item[1]] = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
        # return out_path

    def map_initial(self):
        self.rtl_map_initial()
        self.test_map_initial()
        self.mapGenFlag = True

    def find_port(self, filename, modulename):
        # ports = []
        # parameters = []
        # parameters_all = []
        fd = open(filename, errors='ignore')
        str_for_ports = fd.read()
        string = re.sub("\/\*.*?\*\/", "", str_for_ports, flags=re.S)
        string = re.sub('//.*?\n', "", string, flags=re.S)
        match = re.search("\\bmodule\s*" + modulename + "\s*.*?\\bendmodule\\b", string, flags=re.S)
        if match is None:
            print("can't find module " + modulename + "in this file : " + filename)
            return [[], [], []]
        result = self.fa.find_port_parameter(match.group())
        if result is None:
            print("can't find ports or parameters in module " + modulename + " in " + filename)

        return result

    def find_define(self, path):
        fp = open(path, "r", errors="ignore")
        string = fp.read()
        result = self.fa.find_define(string)
        if result is None:
            print("can't find define in file: " + path)

        return result

    def find_rtl_define_file(self, path, define_word):
        out_path = ""
        if self.mapGenFlag is not True:
            self.map_initial()
        if define_word not in self.rtl_definemap:
            print("waring: define " + define_word + " not find ")
            return ""
        return self.rtl_definemap.get(define_word)[0]

    def find_test_define_file(self, path, define_word):
        out_path = ""
        if self.mapGenFlag is not True:
            self.map_initial()
        if define_word not in self.test_definemap:
            print("waring: define " + define_word + " not find ")
        return self.test_definemap.get(define_word)[0]

    def find_module(self, path, flag):
        fp = open(path, "r", errors="ignore")
        if self.mapGenFlag is not True:
            self.map_initial()
        string_for_find_module = fp.read()

        modules = []

        if flag != 1:
            result = self.fa.find_module_uvm(string_for_find_module)
        else:
            result = self.fa.find_module_inst(string_for_find_module)[1]

        for item in result:
            if item not in self.except_module:
                modules.append(item)

        return modules

    def find_test_file(self, starts, modulenane):
        if self.mapGenFlag is not True:
            self.map_initial()
        out_path = ""
        if modulenane not in self.test_filemap:
            self.test_map_initial()
            if modulenane not in self.test_filemap:
                print("warning module " + modulenane + " not find")

        return self.test_filemap.get(modulenane)

    def find_rtl_file(self, starts, modulename):
        if self.mapGenFlag is not True:
            self.map_initial()
        out_path = ""
        if modulename not in self.rtl_filemap:
            self.rtl_map_initial()
            if modulename not in self.rtl_filemap:
                print("warning module " + modulename + " not find")

        return self.rtl_filemap.get(modulename)

    def dfs(self, lists: list, index: int, flags=1) -> list:
        for i in range(index, len(lists)):
            if lists[i] in self.moduleFound:
                return lists[index:i] + (self.dfs(lists, i + 1, flags))
            if flags == 1:
                path = self.find_rtl_file(self.SourcePath, lists[i])
            else:
                path = self.find_test_file(self.TargetPath, lists[i])
            if path is None:
                self.moduleFound.append(lists[i])
                return lists[index:i] + (self.dfs(lists, i + 1, flags))
            list_temp = self.find_module(path, flags)
            self.moduleFound.append(lists[i])
            if len(list_temp) != 0:
                list1 = lists[index:i] + (self.dfs(list_temp, 0, flags))
                list1.append(lists[i])
                list3 = list1 + (self.dfs(lists, i + 1, flags))
                return list3

        return lists[index:len(lists)]

    def filelist_gen(self, source_path, target_path, top_module_name, fp, fq, flags):
        if self.mapGenFlag is not True:
            self.map_initial()
        if flags == 1:
            path = self.find_rtl_file(source_path, top_module_name)
            if path is None:
                print("can't find top module " + top_module_name + " in path" + source_path)
                return
            defines = self.find_define(path)
            lists_root = []
            define_words = []
            for item in defines:
                if item not in define_words:
                    define_words.append(item)
                define_files = self.find_rtl_define_file(source_path, item)
                if define_files not in lists_root:
                    lists_root.append(define_files)
        else:
            path = self.find_test_file(source_path, top_module_name)
            if path is None:
                print("can't find top module " + top_module_name + " in path" + source_path)
                return
            defines = self.find_define(path)
            lists_root = []
        lists = self.find_module(path, flags)
        lists = self.dfs(lists, 0, flags)
        for item in lists:
            if flags == 1:
                path_local = self.find_rtl_file(self.SourcePath, item)
                string = open(path_local, "r", errors="ignore").read()
                define_temp = self.find_define(path_local)
                for define in define_temp:
                    if define not in define_words:
                        define_file = self.find_rtl_define_file(source_path, define)
                        if define_file not in lists_root and define_file != "":
                            lists_root.append(define_file)
                        define_words.append(define)

        file_path_temp = []
        for item in lists:
            temp_path = self.find_rtl_file(source_path, item)
            if temp_path not in file_path_temp:
                file_path_temp.append(temp_path)
        for item in file_path_temp:
            if item is not None:
                fp.write(os.path.relpath(item, target_path).replace("\\", "/") + "\n")
        fp.write(os.path.relpath(path, target_path).replace("\\", "/") + "\n")
        for item in lists_root:
            if item not in file_path_temp and item is not None:
                fq.write(os.path.relpath(item, target_path).replace("\\", "/") + "\n")


    def file_inst(self, dic, name, flags=1):
        # os.chdir(os.path.dirname(__file__))
        path = self.find_rtl_file(dic, name)
        fp = open(path, "r+", errors='ignore')
        lines = fp.readlines()
        fp.close()
        fp = open(path + 'bak', 'w', errors='ignore')
        fp.writelines(lines)
        fp.close()
        fp = open(path, "w+")
        para_dictionary = {}
        port_dictionary = {}
        variables_dictionary = {}
        for lineT in lines:
            resTemp2 = re.search('(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s+(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s*\(/\*inst\*/\)',
                                lineT)
            resTemp1 = re.search('(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s+(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s*\(/\*inst_i\*/\)',
                                lineT)
            if (resTemp2 is not None) or (resTemp1 is not None):
                # fp.write(resTemp.group(1) + " " + resTemp.group(2) + " " + r"(" + "\n")
                if resTemp2 is not None:
                    resTemp = resTemp2
                else:
                    resTemp = resTemp1
                ports = self.find_port(self.find_rtl_file(dic, resTemp.group(1)), resTemp.group(1))
                lenStr = 0
                len_width = 0
                for port in ports[0]:
                    if len(port[3]) > lenStr:
                        lenStr = len(port[3])
                for para in ports[1]:
                    if len(para) > lenStr:
                        lenStr = len(para)
                for port in ports[1]:
                    if len(port[2]) > len_width:
                        len_width = len(ports[2])
                if resTemp1 is not None:
                    for index in range(len(ports[0])):
                        port = ports[0][index]
                        fp.write("logic " + port[2] + " " * (len_width - len(port[2])) + " " + port[3] + ";\n")
                if len(ports[1]) != 0:
                    fp.write(resTemp.group(1) + " #(\n")
                    for index in range(len(ports[1])):
                        para = ports[1][index]
                        if para not in para_dictionary:
                            para_dictionary[para] = ports[2][index]
                        if flags == 1:
                            if index == len(ports[1]) - 1:
                                fp.write(" " * 8 + r"." + para + " " * (lenStr + 2 - len(para)) + r"())" + "\n")
                            else:
                                fp.write(" " * 8 + r"." + para + " " * (lenStr + 2 - len(para)) + r"()," + "\n")
                        else:
                            if index == len(ports[1]) - 1:
                                fp.write(" " * 8 + r"." + para + " " * (lenStr + 2 - len(para)) + r"(" + para + " " * (
                                        lenStr + 2 - len(para)) + r"))" + "\n")
                            else:
                                fp.write(" " * 8 + r"." + para + " " * (lenStr + 2 - len(para)) + r"(" + para + " " * (
                                        lenStr + 2 - len(para)) + r")," + "\n")

                    fp.write(" " * len(resTemp.group(1)) + " " + resTemp.group(2) + " " + r"(" + "\n")
                else:
                    fp.write(resTemp.group(1) + " " + resTemp.group(2) + " " + r"(" + "\n")

                    # print(lenStr)

                for index in range(len(ports[0])):
                    port = ports[0][index]
                    if port[3] not in port_dictionary:
                        if port[3] not in variables_dictionary:
                            port_dictionary[port[3]] = [port[0],port[1],port[2]]
                    elif port[0] != port_dictionary[port[3]][0]:
                        del port_dictionary[port[3]]
                        if port[3] not in variables_dictionary:
                            variables_dictionary[port[3]] = port[2]

                    
                    if flags == 1:
                        if index == len(ports[0]) - 1:
                            fp.write(
                                " " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"());" + r"//" + port[
                                    0] + " " * (8 - len(port[0])) + port[2] + "\n")
                        else:
                            fp.write(
                                " " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"() ," + r"//" + port[
                                    0] + " " * (8 - len(port[0])) + port[2] + "\n")
                    else:
                        if index == len(ports[0]) - 1:
                            fp.write(
                                " " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + port[3] + " " * (
                                        lenStr + 2 - len(port[3])) + r"));" + r"//" + port[0] + " " * (
                                        8 - len(port[0])) + port[2] + "\n")
                        else:
                            fp.write(
                                " " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + port[3] + " " * (
                                        lenStr + 2 - len(port[3])) + r") ," + r"//" + port[0] + " " * (
                                        8 - len(port[0])) + port[2] + "\n")

            else:
                fp.write(lineT)
        fp.close()
        fp = open(path, "r+", errors='ignore')
        lines = fp.readlines()
        fp.close()
        fp = open(path, "w+")
        # print(para_dictionary)
        # print(port_dictionary)
        for lineT in lines:
            resTemp = re.search('(\\bmodule+\\b)\s+(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s*\(/\*ports\*/\)',
                                lineT)
            if resTemp is not None:
                if len(para_dictionary) != 0:
                    fp.write("module " + resTemp.group(1) + " #(\n")
                    cnt = 0
                    for para in para_dictionary:
                         if cnt == len(para_dictionary) - 1:
                             fp.write(para_dictionary[para] + ")\n")
                         else:
                             fp.write(para_dictionary[para] + ",\n")
                         cnt = cnt + 1
                    
                    fp.write(" " * 10 + "(\n")
                else:
                    fp.write("module " + resTemp.group(2) + " (\n")
                cnt = 0
                port0_len = 0
                port1_len = 0
                port2_len = 0
                for port in port_dictionary:
                    if len(port_dictionary[port][0]) > port0_len:
                        port0_len = len(port_dictionary[port][0])
                    if len(port_dictionary[port][1]) > port1_len:
                        port1_len = len(port_dictionary[port][1])
                    if len(port_dictionary[port][2]) > port2_len:
                        port2_len = len(port_dictionary[port][2])
                    
                for port in port_dictionary:
                    if cnt == len(port_dictionary) - 1:
                        fp.write(" " * 4 + port_dictionary[port][0] + " "*(port0_len -  len(port_dictionary[port][0]))  + " " + "logic" + " " * 0 + " " + port_dictionary[port][2] +" " * (port2_len -  len(port_dictionary[port][2])) + " " + port + ");\n")
                    else:
                        fp.write(" " * 4 + port_dictionary[port][0] + " "*(port0_len -  len(port_dictionary[port][0]))  + " " + "logic" + " " * 0 + " " + port_dictionary[port][2] +" " * (port2_len -  len(port_dictionary[port][2])) + " " + port + ",\n")
                    cnt = cnt + 1
            else:
                fp.write(lineT)

        fp.close()
        fp = open(path, "r+", errors='ignore')
        lines = fp.readlines()
        fp.close()
        fp = open(path, "w+")
        for lineT in lines:
            resTemp = re.search('\s*/\*vars\*/',
                                lineT)
            if resTemp is not None :
                name_len = 0
                width_len = 0
                for var in variables_dictionary:
                    if(len(var) > name_len):
                        name_len = len(var)
                    if(len(variables_dictionary[var]) > width_len):
                        width_len = len(variables_dictionary[var])
                for var in variables_dictionary:
                    fp.write("logic " + variables_dictionary[var] + " " * (width_len - len(variables_dictionary[var])) + " " + var + " " * (name_len - len(var)) + " ;\n")
            else:
                fp.write(lineT)


        fp.close()

# autodefine is deprecated
    def autodefine(self, fullpath):
        os.chdir(os.path.dirname(__file__))
        fp = open(fullpath, "r")
        string = fp.read()
        fs = open(fullpath + "bak", "w+")
        fs.write(string)
        fs.close()
        fp.close()
        res = re.findall("\\bmodule.*?\\bendmodule\\b", string, flags=re.S)
        for item in res:
            string_rep = ""
            [vardefine, string_out] = self.fa.find_varDefine(item)
            [ports, paras, para_all] = self.fa.find_port_parameter(item)
            for i in para_all:
                string_out = string_out.replace(i, "")
            for port in ports:
                var_name = port[3]
                varAttr = {"type": "reg" if port[1] == "reg" else "wire", "width": port[2], "has_load": False,
                           "has_drive": False, "signed": "", "only_inst_port_connect_width": 0, "reWrite": False}
                vardefine.update({var_name: varAttr})
            [detail_module, modules] = self.fa.find_module_inst(string)
            text_used = self.fa.text_used(item)
            port_use = {}
            for module in modules:
                path = self.find_rtl_file(self.SourcePath, module)
                [ports_local, para_local, para_all_local] = self.find_port(path, module)
                portAttr = {}
                for item1 in ports_local:
                    port_name = item1[3]
                    port_width = item1[2]
                    portAttr.update({port_name: port_width})
                port_use.update({module: portAttr})
            for module in detail_module.keys():
                value = detail_module[module]
                port_con = port_use[value["type"]]
                for item2 in value["con"]:
                    pattern = re.compile("[`a-z_A-Z][a-zA-Z0-9_]*", flags=re.S)
                    text_used = text_used + " " + item2

                    if pattern.match(item2) != None:
                        varAttr = {"type": "wire", "width": 0, "has_load": False, "has_drive": False, "signed": "",
                                   "only_inst_port_connect_width": 4, "reWrite": True}
                        if item2 not in vardefine:
                            varAttr["width"] = port_con[value["con"][item2]["type"]]
                            vardefine.update({item2: varAttr})
            for item0 in vardefine:
                if item0 not in text_used:
                    attr = vardefine[item0]
                    attr["reWrite"] = False
                    vardefine[item0] = attr

            pattern = re.compile("\\bmodule.*?;", flags=re.S)
            match = pattern.match(string_out)
            # fp.write(match.group())
            string_rep = match.group() + "\n"

            for item0 in para_all:
                # fp.write(para_all+"\n")
                string_rep = string_rep + "parameter " + item0 + ";\n"
            for item0 in vardefine:
                value = vardefine[item0]
                if value["reWrite"]:
                    # fp.write(value["type"] + " " + value["width"] + " " + item + ";\n")
                    len_space = 1 if value["signed"] != "" else 0
                    string_rep = string_rep + value["type"] + " " + value["signed"] + value[
                        "width"] + len_space * " " + item0 + ";\n"
            string_tmp = string_out[match.end():]
            string_sp = " \n\t"
            index_r = 0
            for index in range(0, len(string_tmp)):
                if string_tmp[index] in string_sp:
                    index_r = index_r + 1
                else:
                    break
            string_rep = string_rep + "\n\n" + string_tmp[index_r:]
            string = string.replace(item, string_rep)
            if len(string) == 0:
                return False

            # fk = open(fullpath+"test","w+")
            # fk.write(string_rep)
            # fk.close()
        if len(string) == 0:
            return False
        fp = open(fullpath, "w")
        fp.write(string)
        fp.close()
        return True
        # fp.write(string_out[match.out])

    # TODO: need to update for multi agent
    def tb_inst(self, SourceDic, fp, name, flag=0, flags=0):
        if self.mapGenFlag is not True:
            self.map_initial()
        path = self.find_rtl_file(SourceDic, name)
        if path is None:
            print(" can't find module : " + name + " in path " + SourceDic)
            return
        # print(path)
        ports = self.find_port(path, name)  # 注意此处ports是一个二维的列表
        if ports is None:
            print(" can't find ports in module " + name + " in path " + path)
            return
        if not os.path.isfile(name + r"_tb.sv"):
            lenStr = 0
            for para in ports[1]:
                if len(para) > lenStr:
                    lenStr = len(para)
            lenPara = lenStr
            for port in ports[0]:
                if len(port[3]) > lenStr:
                    lenStr = len(port[3])
            # fp = open(name + r"TB.sv", "w+")
            fp.write("`include \"uvm_macros.svh\"\n")
            # fp.write("import uvm_pkg::*;\n")
            fp.write("module " + name + "_tb;\n")
            for para_all in ports[2]:
                fp.write("parameter " + para_all + ";\n")
            if len(ports[1]) != 0:
                fp.write(name + "_interface_port #(\n")
                for para in ports[1]:
                    if para == ports[1][len(ports[1]) - 1]:
                        fp.write(" " * 8 + r"." + para + " " * (lenPara + 2 - len(para)) + r"(" + para + " " * (
                                lenPara + 2 - len(para)) + r"))" + "\n")
                    else:
                        fp.write(" " * 8 + r"." + para + " " * (lenPara + 2 - len(para)) + r"(" + para + " " * (
                                lenPara + 2 - len(para)) + r")," + "\n")
                # fp.write(" " * len(name + "_interface_port") + " " + name+"_if" + " " + r"();" + "\n")
                fp.write(" " * len(name + "_interface_port") + " " + "ifo" + " " + r"();" + "\n")
            else:
                fp.write(name + "_interface_port" + " " + "ifo" + " " + r"();" + "\n")
                # fp.write(name+"_interface_port "+name+"_if();\n")

            fp.write(name + "_interface_inner " + "ifi ();\n")
            fp.write("logic clk;\n")
            fp.write("logic rst_n;\n")
            fp.write("logic rst_p;\n")
            # fp.write(name + " " + name + "Inst(\n")

            if len(ports[1]) != 0:
                fp.write(name + " #(\n")
                for para in ports[1]:
                    if para == ports[1][len(ports[1]) - 1]:
                        fp.write(" " * 8 + r"." + para + " " * (lenPara + 2 - len(para)) + r"(" + para + " " * (
                                lenPara + 2 - len(para)) + r"))" + "\n")
                    else:
                        fp.write(" " * 8 + r"." + para + " " * (lenPara + 2 - len(para)) + r"(" + para + " " * (
                                lenPara + 2 - len(para)) + r")," + "\n")
                fp.write(" " * len(name) + " " + name + "_inst" + " " + r"(" + "\n")
            else:
                fp.write(name + " " + name + "_inst" + " " + r"(" + "\n")

                # print(lenStr)

            for port in ports[0]:
                if port == ports[0][len(ports[0]) - 1]:
                    fp.write(
                        " " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + "ifo." + port[3] + " " * (
                                lenStr - len(port[3])) + "));" + r"//" + port[
                            0] + " " * (8 - len(port[0])) + port[2] + "\n")
                else:
                    fp.write(
                        " " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + "ifo." + port[3] + " " * (
                                lenStr - len(port[3])) + ") ," + r"//" + port[
                            0] + " " * (8 - len(port[0])) + port[2] + "\n")

            fp.write("always #5 clk = ~clk;\n\n")

            fp.write("initial begin\n")
            fp.write("clk = 0;\n")
            fp.write("rst_n = 0;\n")
            fp.write("rst_p = 1;\n")
            fp.write("#2 rst_n = 1;\n")
            fp.write("#1 rst_p = 0;\n")

            fp.write("\n")
            fp.write("end\n\n")

            fp.write("always_comb begin\n")
            if (flags == 0):
                fp.write("ifo.clk = clk;\n")
                fp.write("ifo.rst_n = rst_n;\n")
            elif (flags == 1):
                fp.write("ifo.clk = clk;\n")
                fp.write("ifo.rst = rst_p;\n")
            fp.write("\nend\n\n")

            fp.write("initial begin\n")
            fp.write("   run_test();\n")
            fp.write("end\n\n")

            fp.write("initial begin\n")
            fp.write(
                "   uvm_config_db#(virtual " + name + "_interface_port)::set(null, \"uvm_test_top.env.mst_agt.drv\", \"vif\", " + "ifo);\n")
            fp.write(
                "   uvm_config_db#(virtual " + name + "_interface_port)::set(null, \"uvm_test_top.env.mst_agt.mon\", \"vif\", " + "ifo);\n")
            fp.write(
                "   uvm_config_db#(virtual " + name + "_interface_port)::set(null, \"uvm_test_top.env.slv_agt.mon\", \"vif\", " + "ifo);\n")
            fp.write(
                "   uvm_config_db#(virtual " + name + "_interface_inner)::set(null, \"uvm_test_top.env.mst_agt.drv\", \"vif_i\", " + "ifi);\n")
            fp.write(
                "   uvm_config_db#(virtual " + name + "_interface_inner)::set(null, \"uvm_test_top.env.mst_agt.mon\", \"vif_i\", " + "ifi);\n")
            fp.write(
                "   uvm_config_db#(virtual " + name + "_interface_inner)::set(null, \"uvm_test_top.env.slv_agt.mon\", \"vif_i\", " + "ifi);\n")
            fp.write("end\n")
            fp.write("initial begin\n")
            fp.write("   $fsdbDumpvars();\n")
            fp.write("end\n")
            fp.write("\n\n\n\n\nendmodule\n")
            fp.close()
        elif flag == 1:
            print("file exists file refresh\n")
            # os.chdir(TargetPath)
            fo = open(name + r"TB.sv", "r")
            fi = open(name + r"TB.sv.bak", "w+")
            string_temp = fo.read()
            fi.write(string_temp)
            fi.close()
            fo.close()
            fo = open(name + r"TB.sv", "w+")
            # print(string_temp)
            res_para = re.findall("\\blogic\\b.*?;", string_temp, flags=re.S)
            res = re.findall("(?:\\binitial\\b|\\balways\\b\s*\@\s*\*)\s*\\bbegin\\b\s*.*?end\\b", string_temp,
                             flags=re.S)
            # print(res)
            lenStr = 0
            for para in ports[1]:
                if len(para) > lenStr:
                    lenStr = len(para)
            lenPara = lenStr
            for port in ports[0]:
                if len(port[3]) > lenStr:
                    lenStr = len(port[3])
            fo = open(name + r"TB.sv", "w+")
            fo.write("`include \"uvm_macros.svh\"\n")
            # fo.write("import uvm_pkg::*;\n")
            fo.write("module " + name + "TB;\n")
            for para_all in ports[2]:
                fo.write("parameter " + para_all + ";\n")
            if len(ports[1]) != 0:
                fo.write(name + "_interface_port #(\n")
                for para in ports[1]:
                    if para == ports[1][len(ports[1]) - 1]:
                        fo.write(" " * 8 + r"." + para + " " * (lenPara + 2 - len(para)) + r"(" + para + " " * (
                                lenPara + 2 - len(para)) + r"))" + "\n")
                    else:
                        fo.write(" " * 8 + r"." + para + " " * (lenPara + 2 - len(para)) + r"(" + para + " " * (
                                lenPara + 2 - len(para)) + r")," + "\n")
                # fo.write(" " * len(name + "_interface_port") + " " + name+"_if" + " " + r"();" + "\n")
                fo.write(" " * len(name + "_interface_port") + " " + "ifo" + " " + r"();" + "\n")
            else:
                fo.write(name + "_interface_port" + " " + "ifo" + " " + r"();" + "\n")
                # fo.write(name+"_interface_port "+name+"_if();\n")

            fo.write(name + "_interface_inner " + "ifi ();\n")
            # fo.write("logic clk;\n")
            # fo.write("logic rst_n;\n")
            # fo.write("logic rst_p;\n")
            for res_para_temp in res_para:
                fo.write(res_para_temp + "\n")
            # fo.write(name + " " + name + "Inst(\n")

            if len(ports[1]) != 0:
                fo.write(name + " #(\n")
                for para in ports[1]:
                    if para == ports[1][len(ports[1]) - 1]:
                        fo.write(" " * 8 + r"." + para + " " * (lenPara + 2 - len(para)) + r"(" + para + " " * (
                                lenPara + 2 - len(para)) + r"))" + "\n")
                    else:
                        fo.write(" " * 8 + r"." + para + " " * (lenPara + 2 - len(para)) + r"(" + para + " " * (
                                lenPara + 2 - len(para)) + r")," + "\n")
                fo.write(" " * len(name) + " " + name + "_inst" + " " + r"(" + "\n")
            else:
                fo.write(name + " " + name + "_inst" + " " + r"(" + "\n")

            for port in ports[0]:
                if port == ports[0][len(ports[0]) - 1]:
                    fo.write(
                        " " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + "ifo." + port[3] + " " * (
                                lenStr - len(port[3])) + "));" + r"//" + port[
                            0] + " " * (8 - len(port[0])) + port[2] + "\n")
                else:
                    fo.write(
                        " " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + "ifo." + port[3] + " " * (
                                lenStr - len(port[3])) + ") ," + r"//" + port[
                            0] + " " * (8 - len(port[0])) + port[2] + "\n")

            fo.write("always #5 clk = ~clk;\n\n")
            for res_temp in res:
                fo.write(res_temp + "\n\n")

            fo.write("initial begin\n")
            fo.write("   $fsdbDumpvars();\n")
            fo.write("end\n")
            fo.write("\n\n\n\nendmodule\n")
            fo.close()
        else:
            print("file exist, gen stop")

        return name + r"TB"

    def make_sim_dic(self, targetPath, name):
        os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
        # str = "../sim/"
        str = targetPath
        if not os.path.isdir(str):
            print("creat " + targetPath + "/path")
            os.makedirs(str)
        if not os.path.isdir(str + name + "Test"):
            print("creat " + targetPath + name + "Test path")
            os.makedirs(str + name + "Test")
        return os.path.normpath(os.path.abspath(str + name + r"Test/")).replace("\\", "/")

    def interface_gen(self, Source_path, fp, fq, name, flag):
        # os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
        file_path = self.find_rtl_file(Source_path, name)
        ports = self.find_port(file_path, name)
        # interface_path = self.make_sim_dic(TargetPath,name) 
        # os.chdir(interface_path)
        # fp = open(name+"_interface_port.sv","w")
        fp.write("interface " + name + "_interface_port;\n")
        if flag == 1:
            # fq = open(name+"_interface_inner.sv","w")
            # fp = open(name+"_interface.sv","w")
            # fp.write("interface "+name+"_interface;\n" )
            # fp.write(name+"_interface_port ifo();\n")
            # fp.write(name+"_interface_inner ifi();\n")
            # fp.write("\n\n\n\nendinterface")
            fq.write("interface " + name + "_interface_inner;\n")
            fq.write("\n\n\n\nendinterface")
        for para in ports[2]:
            fp.write("parameter " + para + ";\n")
        for port in ports[0]:
            fp.write("logic " + port[2] + (0 if len(port[2]) == 0 else 1) * " " + port[3] + ";\n")
        fp.write("\n\n\n\nendinterface")

    def transation_gen(self, Source_path, TargetPath, name, flag):
        os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
        path = self.make_sim_dic(TargetPath, name)
        os.chdir(path)
        fp = open(name + "_transation.sv", "w")
        # fp.write("import uvm_pkg::*;\n")
        fp.write("class " + name + "_transation extends uvm_sequence_item;\n")
        fp.write("rand bit variable_for_test;\n")
        fp.write("\n\n\nconstraint con{\nvariable_for_test == 0;\n\n}\n")
        fp.write("`uvm_object_utils_begin(" + name + "_transation)\n")
        fp.write("\n\n`uvm_object_utils_end\n")
        fp.write("function new(string name = \"" + name + "_transation\");\nsuper.new();\nendfunction\n")
        fp.write("endclass\n")
        fp.close()

    def sequencer_gen(self, Source_path, TargetPath, name, flag):
        os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
        path = self.make_sim_dic(TargetPath, name)
        os.chdir(path)
        fp = open(name + "_sequencer.sv", "w")
        fp.write("class " + name + "_sequencer extends uvm_sequencer #(" + name + "_transation);\n")
        fp.write(
            "    function new(string name, uvm_component parent);\n        super.new(name, parent);\n    endfunction \n")
        fp.write("    `uvm_component_utils(" + name + "_sequencer)\n")
        fp.write("endclass\n")
        fp.close()

    def scoreboard_gen(self):
        str_temp = "class "+self.filename+"_scoreboard extends uvm_scoreboard;\n\n"
        for index in range(self.agent_out_num):
            str_temp = str_temp + "    " + self.filename + "_transaction expect_queue" + str(index) + "[$];\n"
            str_temp = str_temp + "    uvm_blocking_get_port #(" + self.filename + "_transaction) exp_port" + str(index) +";\n"
            str_temp = str_temp + "    uvm_blocking_get_port #(" + self.filename + "_transaction) act_port" + str(index) +";\n"
            str_temp = str_temp + "\n\n"
        str_temp = str_temp + "    `uvm_component_utils(" + self.filename + "_scoreboard)\n"

        str_temp = str_temp + "function " + self.filename + "_scoreboard::new(string name, uvm_component parent = null);\n"
        str_temp = str_temp + "   super.new(name, parent);\n"
        str_temp = str_temp + "endfunction\n"

        str_temp = str_temp + "function void " + self.filename + "_scoreboard::build_phase(uvm_phase phase);\n"
        str_temp = str_temp + "   super.build_phase(phase);\n"

        for index in range(self.agent_out_num):
            str_temp = str_temp + "    exp_port" + str(index) + " = new(\"exp_port" + str(index) + "\", this);\n"
            str_temp = str_temp + "    act_port" + str(index) + " = new(\"act_port" + str(index) + "\", this);\n"
        str_temp = str_temp + "endfunction\n"

        str_temp = str_temp + "task " + self.filename + "_scoreboard::main_phase(uvm_phase phase);\n"
        for index in range(self.agent_out_num):
            str_temp = str_temp + "    " + self.filename + "_transaction get_expect" + str(index) + ", get_actual" + str(index) + ", tmp_tran" + str(index) + ";\n"
            str_temp = str_temp + "    bit result" + str(index) + ";\n"
        str_temp = str_temp + "   super.main_phase(phase);\n"
        str_temp = str_temp + "    fork\n"
        for index in range(self.agent_out_num):
            str_temp = str_temp + "      while(1) begin\n"
            str_temp = str_temp + "        exp_port" + str(index) + ".get(get_expect" + str(index) + ");\n"
            str_temp = str_temp + "      end\n"
            str_temp = str_temp + "      while(1) begin\n"
            str_temp = str_temp + "        act_port" + str(index) + ".get(act_expect" + str(index) + ");\n"
            str_temp = str_temp + "        if(expect_queue" + str(index) + ".size() > 0) begin\n"
            str_temp = str_temp + "          tmp_tran" + str(index) + " = expect_queue" + str(index) + ".pop_front();\n"
            str_temp = str_temp + "          result" + str(index) + " = get_actual" + str(index) + ".compare(tmp_tran" + str(index) + ");\n"
            str_temp = str_temp + "          if(result" + str(index) + ") begin\n"
            str_temp = str_temp + "          `uvm_info(\"my_scoreboard\", \"" + "Checker" + str(index) +  " compare SUCCESSFULLY\", UVM_LOW);\n"
            str_temp = str_temp + "          end\n"
            str_temp = str_temp + "          else begin\n"
            str_temp = str_temp + "            `uvm_error(\"my_scoreboard\", \"" + "Checker" + str(index) +  " compare FAILED\");\n"
            str_temp = str_temp + "          end\n"
            str_temp = str_temp + "        end\n"
            str_temp = str_temp + "        else begin\n"
            str_temp = str_temp + "          `uvm_error(\"my_scoreboard\", \"" + "Checker" + str(index) +  " received from DUT, while Expect Queue is empty\");\n"
            str_temp = str_temp + "        end\n"
            str_temp = str_temp + "      end\n"
        str_temp = str_temp + "    join\n"
        str_temp = str_temp + "endtask\n"
        return str_temp
               



    def monitor_gen(self,componetn_id):
        str_temp = re.sub("my", self.filename, open("./uvm/my_monitor.sv", "r").read())
        str_temp = re.sub(self.filename+ "_monitor", self.filename+ "_monitor"+str(componetn_id),str_temp)
        # str_temp = re.sub(self.filename+ "_transaction", self.filename+ "_transaction"+str(componetn_id),str_temp)
        return str_temp


    def model_gen(self):
        str_temp = "class "+self.filename+"_model extends uvm_component;\n\n"
        for index in range(self.agent_out_num):
            str_temp = str_temp + "    " + self.filename + "_transaction expect_queue" + str(index) + "[$]\n"
        
        # generate port
        for index in range(self.agent_in_num):
            str_temp = str_temp + "    uvm_blocking_get_port #(" + self.filename + "transaction) port" + str(index) +";\n"
        
        str_temp = str_temp + "\n\n"
        
        #generate ap
        for index in range(self.agent_out_num):
            str_temp = str_temp + "    uvm_analysis_port #(" + self.filename + "transaction) ap" + str(index) +";\n"

        str_temp = str_temp + "\n\n"

        str_temp = str_temp + "    extern function new(string name, uvm_component parent);\n"
        str_temp = str_temp + "    extern function void build_phase(uvm_phase phase);\n"
        str_temp = str_temp + "    extern virtual  task main_phase(uvm_phase phase);\n"

        str_temp = str_temp + "\n\n"

        str_temp = str_temp + "    `uvm_component_utils(" + self.filename + "_model)\n"
        str_temp = str_temp + "endclass\n"

        str_temp = str_temp + "\n\n"


        str_temp = str_temp + "function void " + self.filename + "_model::new(string name, uvm_component parent);\n"
        str_temp = str_temp + "    super.new(name, parent);\n"
        str_temp = str_temp + "endfunction\n"

        str_temp = str_temp + "\n\n"


        str_temp = str_temp + "function void " + self.filename + "_model::build_phase(string name, uvm_component parent);\n"
        str_temp = str_temp + "    super.build_phase(name, parent);\n"
        for index in range(self.agent_in_num):
            str_temp = "    port"+str(index)+" = (\"port" + str(index) + "\", this);\n"
        for index in range(self.agent_out_num):
            str_temp = "    ap"+str(index)+" = (\"ap" + str(index) + "\", this);\n"
        str_temp = str_temp + "endfunction\n"

        str_temp = str_temp + "\n\n"
    
        str_temp = str_temp + "function void " + self.filename + "_model::main_phase(string name, uvm_component parent);\n"
        str_temp = str_temp + "    super.main_phase(phase);\n"
        str_temp = str_temp + "\n\n"
        str_temp = str_temp + "\n\n"
        str_temp = str_temp + "endtask\n"
        return str_temp

    def env_gen(self, Source_path, TargetPath, name, flag):
        str_temp = "class "+self.filename+"_env extends uvm_env;\n\n"
        str_temp = str_temp + "    " + self.filename + "_model mdl;\n"
        str_temp = str_temp + "    " + self.filename + "_scoreboard scb;\n"
        for index in self.agent_in_num:
            str_temp = str_temp + "    " + self.filename + "agent_master" + str(index) + ";\n"
            str_temp = str_temp + "    uvm_tlm_analysis_fifo #(" + self.filename + "_transaction) " + "agent_master" + str(index) +"_mdl_fifo;\n"
        str_temp = str_temp + "\n\n"
        for index in self.agent_out_num:
            str_temp = str_temp + "    " + self.filename + "agent_slave" + str(index) + ";\n"
            str_temp = str_temp + "    uvm_tlm_analysis_fifo #(" + self.filename + "_transaction) " + "agent_slave" + str(index) +"_scb_fifo;\n"
        for index in self.agent_out_num:
            str_temp = str_temp + "    uvm_tlm_analysis_fifo #(" + self.filename + "_transaction) " + "mdl_scb_fifo" + str(index) + ";\n"
        str_temp = str_temp + "    function new(string name = \"" + self.filename + "_env\", uvm_component parent);\n"
        str_temp = str_temp + "        super.new(name, parent);\n"
        str_temp = str_temp + "    endfunction\n"

        str_temp = str_temp + "    virtual function void build_phase(uvm_phase phase);\n"
        str_temp = str_temp + "        super.build_phase(phase);\n"
        for index in range(self.agent_in_num):
            str_temp = str_temp + "      agent_master" + str(index) + " = " + self.filename + "_agent_master" + str(index) + "::type_id::create(\"agent_master" + str(index) + "\", this);\n"
        str_temp = str_temp + "\n\n"
        for index in range(self.agent_in_num):
            str_temp = str_temp + "      agent_slave" + str(index) + " = " + self.filename + "_agent_slave" + str(index) + "::type_id::create(\"agent_master" + str(index) + "\", this);\n"

    def drive_gen(self,componetn_id):
        str_temp = re.sub("my", self.filename, open("./uvm/my_driver.sv", "r").read())
        str_temp = re.sub(self.filename+ "_driver", self.filename+ "_driver"+str(componetn_id),str_temp)
        # str_temp = re.sub(self.filename+ "_transaction", self.filename+ "_transaction"+str(componetn_id),str_temp)
        return str_temp

    def case_gen(self, Source_path, TargetPath, name, flag):
        os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
        write_str = re.sub("my", name, open("./uvm/my_case0.sv", "r").read())
        path = self.make_sim_dic(TargetPath, name)
        os.chdir(path)
        fp = open(name + "_case0.sv", "w")
        fp.write(write_str)
        fp.close()

    def agent_gen(self, Source_path, TargetPath, name, flag):
        os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
        write_str = re.sub("my", name, open("./uvm/my_agent.sv", "r").read())
        path = self.make_sim_dic(TargetPath, name)
        os.chdir(path)
        fp = open(name + "_agent.sv", "w")
        fp.write(write_str)
        fp.close()

    def base_test_gen(self, Source_path, TargetPath, name, flag):
        os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
        write_str = re.sub("my", name, open("./uvm/base_test.sv", "r").read())
        path = self.make_sim_dic(TargetPath, name)
        os.chdir(path)
        fp = open(name + "_base_test.sv", "w")
        fp.write(write_str)
        fp.close()
    

    ##
    ##
    def comp(self):
        for relpath, dirs, files in os.walk("./build"):
            for file in files:
                if(re.match(".+\.py",file) is not None):
                    with open(os.path.join(relpath, file), "r", errors="ignore") as fp:
                        exec(fp.read())
        os.system("cd ../build && echo start build > build.log")
        for key in self.build_list.keys():
            print("[INFO] run build " + key)
            print("[INFO] build command: " + self.build_list[key]["build_opts"])
            os.system("cd ../build/ && "+ self.build_list[key]["build_opts"] + ">> build.log")
        with open("../build/build.log","r") as fq:
            if (re.search("(Error-|ERROR)",fq.read()) is not None):
                print("\033[0;31m[ERROR]  " + self.filename + " build fail\033[0m")
                fq.seek(0)
                lines = fq.readlines()
                flag = False
                mask_cnt = 2
                for line in lines:
                    if(flag ==True and ((re.match("\s+",line) is not None) or (mask_cnt != 0))):
                        print("\033[0;31m" + line + "\033[0m")
                        mask_cnt = mask_cnt - 1
                    else:
                        flag = False
                    if(flag == False and re.search("(Error-|ERROR-)",line) is not None):
                        print("\033[0;31m" + line + "\033[0m")
                        flag = True
                return False
            else:
                print("[INFO]  " + self.filename + " build pass")
                return True
    
    def all(self,test_case,seed,repeat_num):
        build_result = self.comp()
        if build_result:
            self.sim(test_case,seed,repeat_num)
        else:
            print("\033[0;33m[ERROR] skip all test case\033[0m")

    def sim_single(self,test_case,seed,q):
        if not os.path.isdir( "../work"):
            print("[INFO] no work directory, create it")
            os.makedirs("../work")
        if not os.path.isdir( "../work/"+ test_case + "_" + str(seed)):
            print("[INFO] no test directory, create it")
            os.makedirs( "../work/"+ test_case + "_" + str(seed))
        print("[INFO] run test case: ",test_case,", seed=",seed)
        print("[INFO] command: ",self.test_list[test_case]["sim_opts"] + " +ntb_random_seed="+str(seed) + " +UVM_VERBOSITY=" + self.uvm_verbosity)
        os.system("cd " + "../work/"+ test_case + "_" + str(seed) + " && " + self.test_list[test_case]["sim_opts"] + " +ntb_random_seed=" +str(seed) + " +UVM_VERBOSITY=" + self.uvm_verbosity + "> tools.log")
        
        if self.del_pass is False:
            fp = open("../work/"+ test_case + "_" + str(seed) + "/makefile","w")
            str_temp = re.sub("my",self.filename,self.makefile["sim"])
            str_temp = re.sub("TC_TEMP",test_case,str_temp)
            str_temp = re.sub("SEED_TEMP",str(seed),str_temp)
            fp.write(str_temp)
            fp.close()
            # fp = open("../work/"+ test_case + "_" + str(seed) + "/run.tcl","w")
            # fp.write("global env \n")
            # fp.write("#fsdbDumpfile \"hw.fsdb\"\n")
            # fp.write("fsdbDumpvars 0 \"$env(name)_tb\"\n")
            # fp.write("run")
            # fp.close()
        if not os.path.exists("../work/"+ test_case + "_" + str(seed) + "/tools.log"):
            print("[ERROR] can not find log !!!")
            q.put([False,[]," sim path :" + os.path.abspath("../work/"+ test_case + "_" + str(seed))])
            print("[ERROR] running test case number:",threading.activeCount() ,"  can not find log !!!")
        else:
            with open ("../work/"+ test_case + "_" + str(seed) + "/tools.log") as fi:
                if re.search("TEST\s*CASE\s*PASSED",fi.read()) is not None:
                    print("[INFO] " + test_case + "_" + str(seed) + " pass")
                    q.put([True,[]," sim path :" + os.path.abspath("../work/"+ test_case + "_" + str(seed))])
                    print("[INFO] running test case number:",threading.activeCount() - 1,"  "+test_case + "_" + str(seed) + " pass")
                    print("[INFO] " + test_case + "_" + str(seed), " sim path :", os.path.abspath("../work/"+ test_case + "_" + str(seed)))
                    if self.del_pass:
                        print("[INFO] delete sim path : ", os.path.abspath("../work/"+ test_case + "_" + str(seed)))
                        os.system("rm -rf " + os.path.abspath("../work/"+ test_case + "_" + str(seed)))
                else:
                    temp_result = []
                    fi.seek(0)
                    lines = fi.readlines()
                    flag = False
                    mask_cnt = 2
                    for line in lines:
                        # if(flag ==True and  (mask_cnt != 0)):
                        if(flag ==True and ((re.match("\s+",line) is not None) or (mask_cnt != 0))):
                            print("\033[0;31m" + line + "\033[0m")
                            mask_cnt = mask_cnt - 1
                            temp_result.append(line)
                        else:
                            flag = False
                        if(flag == False and re.match("(UVM_ERROR |UVM_FATAL )",line) is not None):
                            print("\033[0;31m" + line + "\033[0m")
                            mask_cnt = 2
                            temp_result.append(line)
                            flag = True
                    q.put([False,temp_result," sim path :" + os.path.abspath("../work/"+ test_case + "_" + str(seed))])
                    print("[INFO] active test case number:",threading.activeCount() - 2,"  "+test_case + "_" + str(seed) + " fail")
                    print("[INFO] " + test_case + "_" + str(seed), " sim path :", os.path.abspath("../work/"+ test_case + "_" + str(seed)))
        self.sem.release()
        


    def sim(self,test_case,seed,repeat_num):
        for relpath, dirs, files in os.walk("./test_list"):
            for file in files:
                if(re.match(".+\.py",file) is not None):
                    # print(file)
                    with open(os.path.join(relpath, file), "r", errors="ignore") as fp:
                        exec(fp.read())
            # print(test_case)
            # print(self.test_list)
        if test_case in self.test_list.keys():
            result = []
            pass_cnt = 0
            pass_case = []
            fail_case = []
            fail_cnt = 0
            q = Queue()
            threads = []
            seed_use = []
            if repeat_num == None:
                repeat_num = self.test_list[test_case]["repeat_num"]
            for index in range(repeat_num):
                if repeat_num != 1:
                    seed_temp = random.randint(0,9999999)
                    while(seed_temp in seed_use):
                        seed_temp = random.randint(0,9999999)
                        # print("retry 00000000000000")
                    seed_use.append(seed_temp)
                    self.sem.acquire()
                    t = threading.Thread(target=self.sim_single,args=(test_case,seed_temp,q))
                else:
                    self.sem.acquire()
                    t = threading.Thread(target=self.sim_single,args=(test_case,seed,q))
                t.start()
                threads.append(t)
            print("[INFO] " , threading.activeCount() - 1 ," test case are running")
            for thread in threads:
                thread.join(300)
            for _ in range(repeat_num):
                result = q.get()
                if result[0]:
                    pass_cnt = pass_cnt + 1
                    pass_case.append(result[2])
                else:
                    fail_cnt = fail_cnt + 1
                    fail_case.append(result[2])
            for item in pass_case:
                print("[INFO] pass case: " + item)
            for item in fail_case:
                print("[ERROR] fail case: " + item)
            print("[INFO] repeat num = ",repeat_num,", pass ",pass_cnt,", fail ",fail_cnt)




    def sim_gen(self, dic, name):
        TargetPath = self.make_sim_dic(name)
        self.tb_inst(dic, TargetPath, name)

    #   flag_tb指示是否为sim文件，flag_tb1:1-重新生成base_test filelist; 5-重新生成三个uvmfilelist flag_dicmake为是否创造路径，flags指示：1,3写define_filelist;2,3写module_filelist;3写filelist； 
    #   flag1指示是否写入本文件路径 

    def filelist_regen(self, flags, flag1, sourcePath, targetPath, name):
        os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
        if self.mapGenFlag is not True:
            self.map_initial()
        search_path = sourcePath
        # path = self.find_rtl_file(search_path,name)
        # if flag_dicmake==1:
        real_targetPath = self.make_sim_dic(targetPath, name)
        # else:
        #     real_targetPath = os.path.dirname(path)
        # if flag_tb == 1:
        self.filelist_gen([targetPath], real_targetPath, name + "_base_test", flags + 1, flag1)
        os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
        self.filelist_gen(search_path, real_targetPath, name, flags, flag1)

    def simflow_cmb(self, sourcePath, targetPath, name):
        if not os.path.isdir(targetPath + "/" + name):
            print("create " + name + " workspace")
            os.makedirs(targetPath + "/" + name)
            os.makedirs(targetPath + "/" + name + "/filelist")
            os.makedirs(targetPath + "/" + name + "/uvc")
            os.makedirs(targetPath + "/" + name + "/tb")
            os.makedirs(targetPath + "/" + name + "/testcase")
            os.makedirs(targetPath + "/" + name + "/work")
            os.makedirs(targetPath + "/" + name + "/sim")
            # os.chdir(targetPath+"/"+name)
            for item in self.uvc:
                fp = open(targetPath + "/" + name + "/uvc/" + name + "_" + item + ".sv", "w")
                fp.write(re.sub("my", name, self.uvc[item]))
                fp.close()
            fp = open(targetPath + "/" + name + "/uvc/" + name + "_""package.sv", "w")
            fp.write("`include " + "uvm_macros.svh" + "\n")
            fp.write("import uvm_pkg::*;\n")
            fp.close()
            fp = open(targetPath + "/" + name + "/uvc/" + name + "_interface_port.sv", "w")
            fq = open(targetPath + "/" + name + "/uvc/" + name + "_interface_inner.sv", "w")
            self.interface_gen(sourcePath, fp, fq, name, 1)
            fp.close()
            fp = open(targetPath + "/" + name + "/tb/" + name + "_tb.sv", "w")
            self.tb_inst(sourcePath, fp, name, 0, 0)
            fp.close()
            fp = open(targetPath + "/" + name + "/filelist/filelist.f", "w")
            print("gen filelist")
            fp.write("-f ../filelist/filelist_def.f\n")
            fp.write("-f ../filelist/filelist_rtl.f\n")
            fp.write("-f ../filelist/filelist_uvc.f\n")
            fp.write("-f ../filelist/filelist_tc.f\n")
            fp.close()
            fp = open(targetPath + "/" + name + "/filelist/makefile", "w")
            fp.write(self.makefile["dv/filelist"])
            fp.close()
            fp = open(targetPath + "/" + name + "/filelist/filelist_rtl.f", "w")
            fq = open(targetPath + "/" + name + "/filelist/filelist_def.f", "w")
            self.filelist_gen(sourcePath, targetPath + "/" + name + "/sim", name, fp, fq, 1)
            fp.close()
            fq.close()
            fp = open(targetPath + "/" + name + "/filelist/filelist_uvc.f", "w")
            fp.write("../uvc/" + name + "_" + "package.sv\n")
            for item in self.uvc:
                fp.write("../uvc/" + name + "_" + item + ".sv\n")
            fp.write("../uvc/" + name + "_interface_port.sv\n")
            fp.write("../uvc/" + name + "_interface_inner.sv\n")
            fp.close()
            fp = open(targetPath + "/" + name + "/filelist/filelist_tc.f", "w")
            for item in self.tc:
                fp.write("../testcase/" + name + "_" + item + ".sv\n")
            fp.close()
            fp = open(targetPath + "/" + name + "/testcase/case0.sv", "w")
            fp.write(re.sub("my", name, self.tc["case0"]))
            fp.close()
            fp = open(targetPath + name + "/sim/makefile", "w")
            fp.write(re.sub("my", name, self.makefile["dv/sim"]))
            fp.close()
        else:
            print("workspace exist")

    def simflow_seq(self, sourcePath, targetPath, name):
        print(sourcePath)
        if not os.path.isdir(targetPath + "/" + name):
            print("create " + name + " workspace")
            os.makedirs(targetPath + "/" + name)
            os.makedirs(targetPath + "/" + name + "/filelist")
            os.makedirs(targetPath + "/" + name + "/uvc")
            os.makedirs(targetPath + "/" + name + "/tb")
            os.makedirs(targetPath + "/" + name + "/testcase")
            os.makedirs(targetPath + "/" + name + "/seq_lib")
            os.makedirs(targetPath + "/" + name + "/work")
            os.makedirs(targetPath + "/" + name + "/build")
            os.makedirs(targetPath + "/" + name + "/sim_ctrl")
            os.makedirs(targetPath + "/" + name + "/sim_ctrl/build")
            os.makedirs(targetPath + "/" + name + "/sim_ctrl/test_list")
            # os.chdir(targetPath+"/"+name)
            for item in self.uvc:
                fp = open(targetPath + "/" + name + "/uvc/" + name + "_" + item + ".sv", "w")
                fp.write(re.sub("my", name, self.uvc[item]))
                fp.close()
            for item in self.seq_lib:
                fp = open(targetPath + "/" + name + "/seq_lib/" + name + "_" + item + ".sv", "w")
                fp.write(re.sub("my", name, self.seq_lib[item]))
                fp.close()
            fp = open(targetPath + "/" + name + "/uvc/" + name + "_""package.sv", "w")
            fp.write("import uvm_pkg::*;\n")
            fp.write("`include " + "\"uvm_macros.svh\"" + "\n")
            fp.close()
            fp = open(targetPath + "/" + name + "/uvc/" + name + "_interface_port.sv", "w")
            fq = open(targetPath + "/" + name + "/uvc/" + name + "_interface_inner.sv", "w")
            self.interface_gen(sourcePath, fp, fq, name, 1)
            fp.close()
            fp = open(targetPath + "/" + name + "/tb/" + name + "_tb.sv", "w")
            self.tb_inst(sourcePath, fp, name, 0, 0)
            fp.close()
            fp = open(targetPath + "/" + name + "/filelist/filelist.f", "w")
            fp.write("-f ../filelist/filelist_def.f\n")
            fp.write("-f ../filelist/filelist_rtl.f\n")
            fp.write("-f ../filelist/filelist_uvc.f\n")
            fp.write("-f ../filelist/filelist_tc.f\n")
            fp.close()
            fp = open(targetPath + "/" + name + "/filelist/makefile", "w")
            fp.write(self.makefile["dv/filelist"])
            fp.close()
            fp = open(targetPath + "/" + name + "/filelist/filelist_rtl.f", "w")
            fq = open(targetPath + "/" + name + "/filelist/filelist_def.f", "w")
            self.filelist_gen(sourcePath, targetPath + "/" + name + "/sim_ctrl", name, fp, fq, 1)
            fp.close()
            fq.close()
            fp = open(targetPath + "/" + name + "/filelist/filelist_uvc.f", "w")
            fp.write("../uvc/" + name + "_" + "package.sv\n")
            fp.write("../uvc/" + name + "_interface_port.sv\n")
            fp.write("../uvc/" + name + "_interface_inner.sv\n")
            for item in self.uvc:
                fp.write("../uvc/" + name + "_" + item + ".sv\n")
            for item in self.seq_lib:
                fp.write("../seq_lib/" + name + "_" + item + ".sv\n")
            fp.close()
            fp = open(targetPath + "/" + name + "/filelist/filelist_tc.f", "w")
            for item in self.tc:
                fp.write("../testcase/" + name + "_" + item + ".sv\n")
            fp.close()
            fp = open(targetPath + "/" + name + "/testcase/" + name + "_case0.sv", "w")
            fp.write(re.sub("my", name, self.tc["case0"]))
            fp.close()
            fp = open(targetPath + name + "/sim_ctrl/makefile", "w")
            fp.write(re.sub("my", name, self.makefile["dv/sim"]))
            fp.close()
            # fp = open(targetPath + name + "/sim_ctrl/run.tcl", "w")
            # fp.write("global env \n")
            # fp.write("#fsdbDumpfile \"hw.fsdb\"\n")
            # fp.write("fsdbDumpvars 0 \"$env(name)_tb \" \"+mda\" \"+struct\"\n")
            # fp.write("run")
            # fp.close()
            fp = open(targetPath + name + "/sim_ctrl/build/build.py", "w")
            fp.write(self.build_py)
            fp.close()
            fp = open(targetPath + name + "/sim_ctrl/test_list/test_list.py", "w")
            fp.write(self.test_list_py)
            fp.close()
            fp = open(targetPath + name + "/build/synopsys_sim.setup", "w")
            fp.write("WORK>DEFAULT\n")
            fp.write("DEFAULT:./work\n")
            fp.write("OTHERS=/opt/vivado_lib/synopsys_sim.setup\n")
            fp.close()
        else:
            print("workspace exist")

    def env_initial(self):
        # os.chdir(os.getcwd())
        for item in self.ctree:
            if not os.path.isdir(item):
                print("generate " + item + " directory")
                os.makedirs(item)
                if item in self.makefile:
                    fp = open(item + "/makefile", "w")
                    fp.write(self.makefile[item])
                    fp.close()
                if item in self.config:
                    fp = open(item + "/config.txt", "w")
                    # print(item)
                    fp.write(self.config[item])
                    fp.close()
            else:
                print(item + " dirdectory exist!!")


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))  # 路径是以此python文件路径为参考
    name = "top"
    # TargetPath = make_sim_dic(TargetPath, name)
    vt = Verilog_tools()
    vt.SourcePath = ["./code/"]
    vt.TargetPath = "./test/"
    name = "top"
    vt.except_module = ['assert_never_unknown', 'ca53dpu_crypto_alu_sha']
    # vt.autodefine("/home/IC/xsc/git_pro/RISCV/code/top.v")

    vt.simflow_seq(vt.SourcePath, vt.TargetPath, name)
    # vt.simflow_seq(vt.SourcePath,vt.TargetPath,name)
    # filelist_gen([SourcePath], TargetPath, "top", 3)
    # filelist_gen(SourcePath,TargetPath, name,3, 0)
    # file_inst(SourcePath, 'test')
    # targetpath = make_sim_dic("Top")
    # makefile_src_gen(targetpath,"Top")
    # filelist_gen(path,targetpath,"uart_byte_txTB")
