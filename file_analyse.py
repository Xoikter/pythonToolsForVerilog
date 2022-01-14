import re
import os
from sys import flags
from typing import Pattern
class File_analyse:
	def __init__(self,strRow) -> None:
		self.keyword = ['always', 'and', 'assign', 'begin', 'buf', 'bufif0', 'bufif1', 'case', 'casex', 'casez', 'cmos', 'deassign',
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
	   'specparam','timescale'
	   'strength', 'strong0', 'strong1', 'supply0', 'supply1', 'table', 'task', 'time', 'tran', 'tranif0',
	   'tranif1', 'tri',
	   'tri0', 'tri1', 'triand', 'trior', 'trireg', 'vectored', 'wait', 'wand', 'weak0', 'weak1', 'while', 'wire',
	   'wor', 'xnor', 'xor','extends','uvm_report_server','int','void','virtual','new','uvm_analysis_port','super'
	   ,'extern0',"uvm_component_utils","type_id",'bit','byte','unsiged','shortint','longint','timer','real','interface','class',
	   'logic','genvar','uvm_tlm_analysis_fifo','uvm_blocking_get_port','constraint','import','uvm_active_passive_enum','define','undef'
	   ,'ifdef','elsif','endif',"uvm_object_utils_begin","uvm_object_utils_end","`define","`"]
		self.res={}
		self.strRow = strRow
		self.macro = []
	#     self.module_name = []
	#     self.module_inst = []
	#     self.defvar = []
	#     self.usedvar = []
	#     self.
	def def_tools(self,stringIn:str):
		string_out = stringIn
		str_temp = re.findall("((?:`ifdef|`ifndef|`else|`elsif).*?)(?=`else|`elsif|`endif)",stringIn,flags=re.S)
		for item in str_temp:
			res_temp =re.search("(`ifdef)\s*(\S*)\s*",item,flags=re.S) 
			if res_temp is not None and res_temp.group(2)  in self.macro:

				return(item.replace(res_temp.group()," "))
			elif res_temp is not None:
				string_out = string_out.replace(item," ")
			res_temp =re.search("(`ifndef)\s*(\S*)\s*",item,flags=re.S) 
			if res_temp is not None and res_temp.group(2) not   in self.macro:
				return(item.replace(res_temp.group()," "))
				string_out =  string_out.replace(item," ")
			elif res_temp is not None:
				string_out = string_out.replace(item," ")
		string_out = string_out.replace(r'`endif'," ")
		string_out = string_out.replace(r'`else'," ")
		return string_out


				



	def define_op(self,stringIn:str):
		# string = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		# string = re.sub('//.*?\n', "", string, flags=re.S)
		string = stringIn
		pattern = re.compile("`endif\\b",flags=re.S)
		match = re.search("`(?:ifdef|ifndef)\\b",stringIn,flags=re.S)
		if(match == None):
			return stringIn
		i_s = re.finditer("`(?:ifdef|ifndef)\\b",stringIn,flags=re.S)
		i_sp = 0
		for item in i_s:
			i_sp = item.start()
		i_e = pattern.search(string,i_sp)
		if i_e != None:
			string_temp = string[i_sp:i_e.end()]
			string_rep = self.def_tools(string_temp)
			string = string.replace(string_temp,string_rep)
			return self.define_op(string)
		return None
		

		for i in reversed(i_s):
			i_e = pattern.search(string,i.end())
			if i_e != None:
				string_temp = string[i.start():i_e.end()]
				string_rep = self.def_tools(string_temp)
				string = string.replace(string[i.start():i_e.end()],string_rep)
				return self.define_op(string)
		

















	##  find pair pattern
	## if pattern lenth == 1,regard it as symbol like {} (),else regard it as var
	## return list :
	## 		pair string list, string witch delete pair string 
	def find_pair(self,stringIn:str,string_begin:str,string_end:str,replace_str:str):
		string = re.sub("\\bif\\b\s*\(.*?\)",";",stringIn,flags=re.S)
		string = re.sub("\\bcase(z|x)?\\b\s*\(.*?\)",";",string,flags=re.S)
		return [[],string]
		res = []
		string = stringIn
		lenth = len(string_end)
		
		if lenth == 1:
			ll = ""
		else:
			ll = "\\b"
		pattern_end = re.compile(ll+string_end+ll)
		pattern_begin = re.compile(ll+string_begin+ll)
		while(1):
			# string_temp= re.search("\\b"+string_begin+"\\b.*?\\b"+string_end+"\\b",string,flags=re.S).group()
			# if(string_temp == None):
			# 	break
			# ptr_s = string.find(string_temp)
			match = pattern_begin.search(string)
			if( match == None):
				break
			ptr_s = match.start()
			ptr_e = ptr_s
			while(1):
				# ptr_e = string.find(string_end,ptr_e + lenth)
				match = pattern_end.search(string,ptr_e)
				if match == None:
					string = re.sub("\\bif\\b\s*\(.*?\)",";",stringIn,flags=re.S)
					string = re.sub("\\bcase(z|x)?\\b\s*\(.*?\)",";",string,flags=re.S)
					return [[],string]
				ptr_e = pattern_end.search(string,ptr_e).end()
				count_begin = len(re.findall("\\b"+string_begin+"\\b",string[ptr_s:ptr_e],flags=re.S))
				count_end = len(re.findall("\\b"+string_end+"\\b",string[ptr_s:ptr_e],flags=re.S))
				if(count_begin == count_end):
					# print(string[ptr_s:ptr_e])
					# print(len(string))
					res.append(string[ptr_s:ptr_e])
					# string = re.sub(string[ptr_s:ptr_e+lenth],"",string)
					string = string.replace(string[ptr_s:ptr_e],replace_str)
					# print(len(string))
					break
		return [res,string]
	# def gene_tool(self,stringIn:str):
	# 	string = stringIn
	# 	pattern_for = re.compile("\\bgenerate\\b\s*for\\b",flags=re.S)
	# 	pattern_if = re.compile("\\bgenerate\\b\s*if\\b",flags=re.S)
	# 	pattern_case = re.compile("\\bgenerate\\b\s*case\\b",flags=re.S)
	# 	pattern_begin = re.compile("\\begin\\",flags=re.S)
	# 	string_out = ""
	# 	p_s = 0
	# 	if pattern_for(stringIn[p_s:]) != None:
	# 		match = pattern_begin.search(string,p_s)
	# 		if match != None:
	# 			res = self.find_pair(string[p_s:],"begin","end","")[0]
				




	# def gene_op(self,stringIn:str):
	# 	string = stringIn
	# 	# string_temp = self.find_pair(string,"generate","endgenerate"," ")[0]
	# 	match = re.search("\\bgenerate\\b",string,flags = re.S)
	# 	if match == None:
	# 		return stringIn
	# 	ine = re.finditer("\\bgenerate\\b",string,flags=re.S)
	# 	s_p = 0
	# 	for item in ine:
	# 		s_p = item.start()
	# 	s_e = s_p
	# 	pattern = re.compile("\\bendgenerate\\b",flags=re.S)
	# 	match = pattern.search(string,s_p)
	# 	if match == None:
	# 		print("error")
	# 		return None
	# 	s_e = match.end()
	# 	string_rep = self.gene_tool(string[s_p:s_e])
	# 	string = string.replace(string[s_p:s_e],string_rep)
	# 	return self.gene_op(string)

		
	# 	for item in string_temp:
			
	def varDefineTool(self,stringIn:str):
		stringTemp = stringIn
		string = re.sub("\[.*?\]","",stringIn,flags=re.S)
		string = re.sub("=.*?[,;]",",",string,flags=re.S)
		string = re.sub(" ","",string)
		string = re.sub(";",",",string)
		res = string.split(",")
		res.pop()
		return res
	def find_varDefine(self,stringIn:str):
		out = {}
		stringTemp = stringIn
		string = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		string = re.sub('//.*?\n', "", string, flags=re.S)
		string = re.sub("\\bfunction\\b[\s\S]*?\\bendfunction\\b", "", string)
		string = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", string)
		string = re.sub("\\binterface\\b.*?;", "", string, flags=re.S)
		string = re.sub("\\bmodule\\b.*?;", "", string, flags=re.S)
		pattern = re.compile("\\b(wire|reg|intergred)\\b\s*\\b(signed|unsigned)?\s*(\[.*?\])?\s*(.*?;)")
		pattern_temp = re.compile("\\b(?:wire|reg|intergred)\\b\s*\\b(?:signed|unsigned)?\\b\s*(?:\[.*?\])?\s*(?:.*?;)\s*?\n")
		res = pattern.findall(string)
		for item in res:
			# varAttr.update({{"type":item[0]},{"width":}}
			varAttr = {"type":"wire","width":0,"has_load":False,"has_drive":False,"signed":"","only_inst_port_connect_width":0,"reWrite":True}
			varAttr["type"] = item[0] 
			varAttr["signed"] = item[1]
			varAttr["width"] = item[2] 
			if "=" in item[3]:
				varAttr["reWrite"] = False
			if "[" in item[3]:
				varAttr["reWrite"] = False
			var_local = self.varDefineTool(item[3])
			for item in var_local:
				out.update({item:varAttr})
		# print(out)
		ret_temp =pattern_temp.findall(string)
		for item in ret_temp:
			if "=" not in item:
				stringTemp = stringTemp.replace(item,"")
		return [out,stringTemp]
	def find_port_parameter(self,stringIn:str):
		ports = []
		parameters = []
		parameters_all = []
		str_temp = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
		str_temp = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", str_temp)
		str_temp = re.sub("\\bfunction\\b[\s\S]*?\\bendfunction\\b", "", str_temp)
		str_temp = re.sub("\\binterface\\b.*?;", "", str_temp, flags=re.S)
		str_port = re.search("\\bmodule.*?;",str_temp,flags=re.S).group()
		# result = re.findall('\\b(input|output)\\b\s*\\b(wire|reg)?\\b\s*(\[.*?\])?\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)', str_port, flags=re.S)
		result = re.findall('\\b(input|output)\\b\s*\\b(wire|reg)?\s*\\b(?:signed)?\\b\s*(\[.*?\])?\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)', str_port, flags=re.S)
		# res_para = re.findall('\\bparameter\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)(\s*=)',str_port,flags=re.S)
		res_para_temp = re.finditer('#\s*\(',str_port,flags=re.S)
		stack_para = []
		para_str_port = []
		if res_para_temp is not None:
			stack_para.append("(")
		for res_pare_temp_item in res_para_temp:
			for index in range(res_pare_temp_item.end(),len(str_port)):
				if(str_port[index] == r"("):
					stack_para.append(r"(")
				if(str_port[index] == r")"):
					stack_para.pop()
				if len(stack_para) == 0:
					para_str_port.append(str_port[res_pare_temp_item.end():index])
					break
		for item in para_str_port:
			str_temp_local = re.sub("\\bparameter\\b"," ",item,flags=re.S)
			res_split = re.split("\s*,\s*",str_temp_local)
			for res_sp in res_split:
				res_sp = re.sub("^\s*","",res_sp,flags=re.S)
				res_sp = re.sub("\s*$","",res_sp,flags=re.S)
				parameters_all.append("parameter " + res_sp + ";")
				res_sp_temp = re.sub("=.*","",res_sp,flags=re.S)
				res_sp_temp = re.sub("\s","",res_sp_temp,flags=re.S)
				parameters.append(res_sp_temp)




		# for res in res_para:
		#     para_temp = res[0]
		#     parameters.append(para_temp)
		for res in result:
			portTemp = [res[0], res[1], res[2], res[3]]
			ports.append(portTemp)
		str_temp = re.sub("\\bmodule.*?;","",str_temp,flags=re.S)
		result = re.findall('\\b(input|output)\\b\s*\\b(wire|reg)?\\b\s*\\b(?:signed)?\\b\s*(\[.*?\])?\s*(.*?)\s*;', str_temp, flags=re.S)
		res_para = re.findall('\\bparameter\\b\s*(.*?)\s*;',str_temp,flags=re.S)
		if len(parameters) != 0:
			res_para = []
		for res in res_para:
			res_temp1 = re.split("\s*,\s*",res)
			parameters_all.append(res)
			for item in res_temp1:
				res_temp2 = re.split('\s*=\s*',item)
				parameters.append(res_temp2[0])		
		for res in result:
			res_temp = re.split("\s*,\s*", res[3])
			for item in res_temp:
				portTemp = [res[0], res[1], res[2], item]
				ports.append(portTemp)
		return [ports, parameters,parameters_all]		
	def connect_tool(self,stringIn:str):
		# string = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		# string = re.sub('//.*?\n', "", string, flags=re.S)
		pattern = re.compile("\.\s*([a-zA-Z0-9_`]*)\s*\(\s*(.*?)\s*\)",flags=re.S)
		# pattern_all = re.compile("\.\s*[a-zA-Z_`]*\s*\(.*?\)",flags=re.S)
		# string_temp = pattern_all.sub("",string)
		# string_temp = re.sub("\.\s*(?:[a-zA-Z0-9_`]*)\s*\(\s*(?:.*?)\s*\)","",string,flags=re.S)
		# string_temp = re.sub("[,;\(\)\s]","",string_temp)
		res = pattern.findall(stringIn)
		con = {}
		for item in res:
			con.update({item[1]:{"type":item[0],"width":0}})
		return con
	# def find_module_inst(self,stringIn:str):
	# 	out = {}
	# 	string = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
	# 	string = re.sub('//.*?\n', "", string, flags=re.S)
	# 	string = re.sub("\$.*?;",";",string,flags=re.S)
	# 	string = re.sub("\".*?\"",";",string,flags=re.S)
	# 	string = re.sub("\\bfunction\\b[\s\S]*?\\bendfunction\\b", "", string)
	# 	string = re.sub("\\bmodule\\b[\s\S]*?;", "", string)
	# 	string = re.sub('\\bdefine.*', "", string)
	# 	string = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", string)
	# 	string = re.sub("\\bcase\\b[\s\S]*?\\bendcase\\b", ";", string)
	# 	string = re.sub("\\binterface\\b.*?;", "", string, flags=re.S)
	# 	string = self.find_pair(string,"begin","end",";")[1]		
	# 	string = re.sub('`else\\b', " ", string)
	# 	string = re.sub('`ifdef\\b', " ", string)
	# 	string = re.sub('`endif\\b', " ", string)
	# 	string = re.sub('`elif\\b', " ", string)
	# 	string = re.sub("\\belse\\b.*?;","",string,flags=re.S)
	# 	string = re.sub("\\bif\\b.*?;",";",string,flags=re.S)
	# 	string = re.sub("\\balways\\b.*?;","",string,flags=re.S)
	# 	string = re.sub("\\binitial\\b.*?;","",string,flags=re.S)
	# 	string = re.sub("\\bassign\\b.*?;","",string,flags=re.S)
	# 	string = re.sub("\\bwire\\b.*?;","",string,flags=re.S)
	# 	pattern = re.compile("(\\b[a-zA-Z_`][a-zA-Z0-9_$]*\\b)\s*(#\s*\([^;]*?\))?\s*(\\b[a-zA-Z_`][a-zA-Z0-9_$]*\\b)\s*(\([^;]*?\))\s*;",flags=re.S)
	# 	res = pattern.findall(string)
	# 	module = []
	# 	for item in res:
	# 		if item[1] not in self.keyword and item[0] not in self.keyword:
	# 			con = self.connect_tool(item[3])
	# 			out.update({item[2]:{"type":item[0],"con":con}})
	# 			module.append([item[0],item[2]])
	# 	# print(res)
	# 	return [out,module]
	def find_module_inst(self,stringIn:str):
		string = stringIn
		symbol = " \n\t"
		string = re.sub("\/\*.*?\*\/", "", string, flags=re.S)
		string = re.sub('//.*?\n', "", string, flags=re.S)
		res = re.finditer("\s*([`_a-zA-Z][_a-zA-Z0-9]*)\\b\s*(?=#|[`_a-zA-Z][_a-zA-Z0-9]*\\b)",string,flags=re.S)
		pattern_1 = re.compile("\s*#",flags=re.S)
		pattern_3 = re.compile("\s*([`_a-zA-Z][_a-zA-Z0-9]*\\b)",flags=re.S)
		pattern_2 = re.compile("\s*\(",flags=re.S)
		out = {}
		module = []
		except_words = ["function","`define","task"]

		for item in res:
			module_name = ""
			module_type = ""
			module_connect = ""
			word = ""
			# for i in range(0,item.start()):
			# 	if string[item.start() - i - 1] not in symbol:
			# 		word = string[item.start() - i - 1] + word
			# 	elif len(word) != 0:
			# 		break
			# if(word  in except_words):
			# 	continue
	


			if item.group(1) not in self.keyword:
				for i in range(0,item.start()):
					if string[item.start() - i - 1] not in symbol:
						word = string[item.start() - i - 1] + word
					elif len(word) != 0:
						break
				if(word  in except_words):
					continue
				match_p = pattern_1.match(string,item.end())
				if match_p!= None:
					match = pattern_2.match(string,match_p.end())
					if match == None:
						continue
				# if item.group(2) == "#":
					stack = []
					index = 0
					# match = pattern_2.match(string,match.end())
					# if match == None:
					# 	continue
					for i in range(match.end() - 1 ,len(string)):
						if string[i] == "(":
							stack.append("(")	
						if string[i] == ")":
							stack.pop()
						if len(stack) == 0:
							index = i + 1
							break
					match = pattern_3.match(string,index)
					if  match == None or match.group(1)  in self.keyword:
						continue
					if  match != None and match.group(1) not in self.keyword:
						index = match.end()
					match_connect = pattern_2.match(string,index)
					if match_connect ==  None:
						continue
					for i in range(match_connect.end() - 1, len(string)):
						if string[i] == "(":
							stack.append("(")	
						if string[i] == ")":
							stack.pop()
						if len(stack) == 0:
							index = i + 1
							break
					con = self.connect_tool(string[match_connect.end() - 1:index])
					out.update({match.group(1):{"type":item.group(1),"con":con}})
					if item.group(1) not in module:
						module.append(item.group(1))
				else:
					stack = []
					index = 0
					match = pattern_3.match(string,item.end())
					if  match == None or match.group(1)  in self.keyword:
					# if   item.group(2)  in self.keyword:
						continue
					# if   item.group(1) not in self.keyword:
						index = match.end()
					match_connect = pattern_2.match(string,match.end())
					if match_connect ==  None:
						continue
					for i in range(match_connect.end() - 1, len(string)):
						if string[i] == "(":
							stack.append("(")	
						if string[i] == ")":
							stack.pop()
						if len(stack) == 0:
							index = i + 1
							break
					con = self.connect_tool(string[match_connect.end() - 1:index])
					out.update({match.group(1):{"type":item.group(1),"con":con}})
					if item.group(1) not in module:
						module.append(item.group(1))
					
					
						

		return [out, module]
	def find_module_uvm(self,stringIn:str) :
		string = stringIn
		modules = []
		except_words = ["function","`define","task"]
		symbol = " \n\t"
		out = {}
		string = re.sub("\/\*.*?\*\/", "", string, flags=re.S)
		string = re.sub('//.*?\n', "", string, flags=re.S)
		res_transtion = re.findall("#\s*\(\s*([_a-zA-Z][_a-zA-Z0-9]*)\s*\)",string,flags=re.S)
		pattern_3 = re.compile("\s*(\\b[_a-zA-Z][_a-zA-Z0-9]*\\b)",flags=re.S)
		pattern_2 = re.compile("\s*\(",flags=re.S)
		pattern_end = re.compile("\s*;",flags=re.S)
		for item in res_transtion:
			if item not in modules and item not in self.keyword:
				modules.append(item)
		res = re.finditer("\\b[_a-zA-Z][_a-zA-Z0-9]*\\b",string,flags=re.S)
		for item in res:
			module_name = ""
			module_type = ""
			module_connect = ""
			word = ""
			for i in range(0,item.start()):
				if string[item.start() - i - 1] not in symbol:
					word = string[item.start() - i - 1] + word
				elif len(word) != 0:
					break
			if(word  in except_words):
				continue

			if item.group() not in self.keyword:
				stack = []
				index = 0
				match = pattern_3.match(string,item.end())
				if  match == None or match.group(1)  in self.keyword:
					continue
				if  match != None and match.group(1) not in self.keyword:
					index = match.end()
				match_end = pattern_end.match(string,index)
				if match_end != None:
					if match.group() not in self.keyword:
						modules.append(item.group())
					continue
				match_connect = pattern_2.match(string,index)
				if match_connect ==  None:
					continue
				for i in range(match_connect.start(), len(string)):
					if string[i] == "(":
						stack.append("(")	
					if string[i] == ")":
						stack.pop()
					if len(stack) == 0:
						index = i + 1
						break
				# con = self.connect_tool(string[match_connect.start():index])
				match_end = pattern_end.match(string,index)
				if match_end !=  None:
					if item.group() not in modules:
						modules.append(item.group())
				# out.update({match.group(1):{"type":item.group(),"con":con}})
				# if item.group() not in module:
				# 	module.append(item.group())
				
				
					

		return modules



					

	# def find_module_uvm(self,stringIn:str):
	# 	out = []
	# 	string = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
	# 	string = re.sub('//.*?\n', "", string, flags=re.S)
	# 	string = re.sub("\$.*?;",";",string,flags=re.S)
	# 	string = re.sub("\".*?\"",";",string,flags=re.S)
	# 	string = re.sub('\\bextern.*?;', "", string, flags=re.S)
	# 	string = re.sub('\\bdefine.*', "", string)
	# 	string = re.sub("\\bfunction\\b[\s\S]*?\\bendfunction\\b", "", string)
	# 	string = re.sub("\\bmodule\\b[\s\S]*?;", "", string)
	# 	string = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", string)
	# 	string = re.sub("\\bcase\\b[\s\S]*?\\bendcase\\b", ";", string)
	# 	string = re.sub("\\binterface\\b.*?;", "", string, flags=re.S)
	# 	string = self.find_pair(string,"begin","end",";")[1]		
	# 	string = re.sub('`else\\b', " ", string)
	# 	string = re.sub('`ifdef\\b', " ", string)
	# 	string = re.sub('`endif\\b', " ", string)
	# 	string = re.sub('`elif\\b', " ", string)
	# 	string = re.sub("\\belse\\b.*?;","",string,flags=re.S)
	# 	string = re.sub("\\bif\\b.*?;",";",string,flags=re.S)
	# 	string = re.sub("\\balways\\b.*?;","",string,flags=re.S)
	# 	string = re.sub("\\binitial\\b.*?;","",string,flags=re.S)
	# 	string = re.sub("\\bassign\\b.*?;","",string,flags=re.S)
	# 	string = re.sub("\\bwire\\b.*?;","",string,flags=re.S)
	# 	transtion_tmp = re.findall("#\(\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*\)",string,flags=re.S)

	# 	for item in transtion_tmp:
	# 		if(item not in self.keyword):
	# 			out.append([item,"----"])
	# 	module_result = re.findall( "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(?:\(.*?\))?;", string,flags=re.S)
	# 	for item in module_result:
        #     	    if(item[0] not in self.keyword and item[1] not in self.keyword):
        #     	        out.append(item)
	# 	return out




	def text_used(self,stringIn:str):
		stringOut = ""
		string = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		string = re.sub('//.*?\n', "", string, flags=re.S)
		# string = re.sub("\\bfunction\\b[\s\S]*?\\bendfunction\\b", "", string)
		string = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", string)
		string = re.sub("\\binterface\\b.*?;", "", string, flags=re.S)
		string = re.sub("\[.*?\]", "", string, flags=re.S)
		string = re.sub("`[a-zA-Z0-9_]*?\\b"," ",string,flags=re.S)
		#find  = right
		string = string.replace("==="," ")
		string = string.replace("=="," ")

		func = re.findall("\\bfunction\\b\s*(.*)?\s*(?:;\()",string,flags=re.S)
		string = re.sub("\\bfunction\\b[\s\S]*?\\bendfunction\\b", "", string)
		res_left = re.finditer("<?=",string,flags=re.S)
		for item in res_left:
			stack = []
			word = ""
			flag = 0
			index = 0
			word_blank = " \n\t"
			for i in range(0,item.start()):
				if string[item.start() - 1 - i] == "}":
					flag = 1
					index = item.start() - 1 - i
					break
				elif string[item.start() - 1 - i] == ")":
					flag = 2
					index = item.start() - 1 - i
					break
				elif string[item.start() - 1 - i] not in word_blank:
					flag = 3
					index = item.start() - 1 - i
					break
			for i in range(0,index):
				if flag == 1 :
					if string[index - i] == "}":
						stack.append("}")
					if string[index - i] == "{":
						stack.pop()
					if len(stack) == 0:
						stringOut = stringOut + " " + string[index - i:index+1]
						break
				if flag == 2 :
					if string[index - i] == ")":
						stack.append(")")
					if string[index - i] == "(":
						stack.pop()
					if len(stack) == 0:
						stringOut = stringOut + " " + string[index - i:index+1]
						break
				if flag == 3:
					if string[index - i] in word_blank:
						stringOut = stringOut + " " + string[index - i:index+1]
						break

				
		res_right = re.findall("=.*?;",string,flags=re.S)
		for item in res_right:
			stringOut = stringOut + " " + item.replace("="," ")
		res_if = re.findall("\\bif\\b\s*\((.*?)\)",string,flags=re.S)
		for item in res_if:
			stringOut = stringOut + " " + item

		res_case = re.findall("\\bcase(?:z|x)?\\b\s*\((.*?)\)",string,flags=re.S)
		for item in res_case:
			stringOut = stringOut + " " + item
		res_func = []
		for item in func:
			res_func.append(re.findall("\\b"+item+ "\\b\s*\((.*?)\)"))
		for item in res_func:
			stringOut = stringOut + " " + item
		res_always = re.findall("\\balways@?\((.*?)\)",string,flags=re.S)
		for item in res_always:
			string_local = re.sub("(posedge|negedge|or)"," ",item,flags=re.S)
			stringOut = stringOut + " " +string_local 
		return stringOut


	def find_define(self,stringIn:str):
		str_temp = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
		res = re.findall("`([_a-zA-Z][_a-zA-Z0-9]*)\\b",str_temp,flags=re.S)
		out = []
		for item in res:
			if item not in self.keyword:
				out.append(item)
		return 	out
	def find_define_word(self,stringIn:str):
		# str_temp = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		# str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
		return re.findall("`define\s*([\S]+)\s*",stringIn,flags=re.S)
