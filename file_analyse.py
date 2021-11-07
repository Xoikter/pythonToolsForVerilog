import re
import os
from sys import flags
class File_analyse:
	def __init__(self,strRow) -> None:
	    self.res = {}
	    self.strRow = strRow
	#     self.module_name = []
	#     self.module_inst = []
	#     self.defvar = []
	#     self.usedvar = []
	#     self.




	##  find pair pattern
	## if pattern lenth == 1,regard it as symbol like {} (),else regard it as var
	## return list :
	## 		pair string list, string witch delete pair string 

	def find_pair(self,stringIn:str,string_begin:str,string_end:str,replace_str:str):
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
	def varDefineTool(self,stringIn:str):
		stringTemp = stringIn
		string = re.sub("[.*?]","",stringIn,flags=re.S)
		string = re.sub("=.*?[,;]",",",string,flags=re.S)
		string = re.sub(" ","",string)
		string = re.sub(";",",",string)
		res = string.split(",")
		res.pop()
		return res
	def find_varDefine(self,stringIn:str):
		out = {}
		stringTemp = stringIn
		varAttr = {"type":"wire","width":0,"has_load":False,"has_drive":False,"only_inst_port_connect_width":0,"reWrite":True}
		string = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		string = re.sub('//.*?\n', "", string, flags=re.S)
		string = re.sub("\\bfunction\\b[\s\S]*?\\bendfunction\\b", "", string)
		string = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", string)
		string = re.sub("\\binterface\\b.*?;", "", string, flags=re.S)
		pattern = re.compile("\\b(wire|reg|intergred)\\b\s*(\[.*?\])?\s*(.*?;)")
		pattern_temp = re.compile("\\b(?:wire|reg|intergred)\\b\s*(?:\[.*?\])?\s*(?:.*?;)\s*?\n")
		res = pattern.findall(string)
		for item in res:
			# varAttr.update({{"type":item[0]},{"width":}}
			varAttr["type"] = item[0] 
			varAttr["width"] = item[1] 
			if "=" in item[2]:
				varAttr["reWrite"] = False
			var_local = self.varDefineTool(item[2])
			for item in var_local:
				out.update({item:varAttr})
		# print(out)
		ret_temp =pattern_temp.findall(string)
		for item in ret_temp:
			if "=" not in item:
				stringTemp = stringTemp.replace(item,"")
		return [out,stringTemp]
	def find_port_parameter(self,stringIn:str):
		str_temp = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", stringIn)
		str_temp = re.sub("\\binterface\\b.*?;", "", str_temp, flags=re.S)
		str_port = re.search("\\bmodule.*?;",str_temp,flags=re.S).group()
		result = re.findall('\\b(input|output)\\b\s*\\b(wire|reg)?\\b\s*(\[.*?\])?\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)', str_port, flags=re.S)
		res_para = re.findall('\\bparameter\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)(\s*=)',str_port,flags=re.S)
		ports = []
		parameters = []
		parameters_all = []
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
		string = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		string = re.sub('//.*?\n', "", string, flags=re.S)
		pattern = re.compile("\.\s*([a-zA-Z0-9_`]*)\s*\(\s*(.*?)\s*\)",flags=re.S)
		# pattern_all = re.compile("\.\s*[a-zA-Z_`]*\s*\(.*?\)",flags=re.S)
		# string_temp = pattern_all.sub("",string)
		string_temp = re.sub("\.\s*(?:[a-zA-Z0-9_`]*)\s*\(\s*(?:.*?)\s*\)","",string,flags=re.S)
		string_temp = re.sub("[,;\(\)\s]","",string_temp)
		res = pattern.findall(string)
		con = {}
		for item in res:
			con.update({item[1]:{"type":item[0],"width":0}})
		return con
	def find_module_inst(self,stringIn:str):
		out = {}
		string = re.sub("\/\*.*?\*\/", "", stringIn, flags=re.S)
		string = re.sub('//.*?\n', "", string, flags=re.S)
		string = re.sub("\\bfunction\\b[\s\S]*?\\bendfunction\\b", "", string)
		string = re.sub("\\bmodule\\b[\s\S]*?;", "", string)
		string = re.sub("\\btask\\b[\s\S]*?\\bendtask\\b", "", string)
		string = re.sub("\\bcase[\s\S]*?\\bendcase\\b", ";", string)
		string = re.sub("\\binterface\\b.*?;", "", string, flags=re.S)
		string = self.find_pair(string,"begin","end",";")[1]		
		string = re.sub("\\belse.*?;","",string,flags=re.S)
		string = re.sub("\\bif.*?;",";",string,flags=re.S)
		string = re.sub("\\balways.*?;","",string,flags=re.S)
		string = re.sub("\\bassign.*?;","",string,flags=re.S)
		string = re.sub("\\bwire.*?;","",string,flags=re.S)
		pattern = re.compile("(\\b[a-zA-Z_`][a-zA-Z0-9_$]*\\b)\s*(#\s*\([^;]*?\))?\s*(\\b[a-zA-Z_`][a-zA-Z0-9_$]*\\b)\s*(\([^;]*?\))\s*;",flags=re.S)
		res = pattern.findall(string)
		module = []
		for item in res:
			con = self.connect_tool(item[3])
			out.update({item[2]:{"type":item[0],"con":con}})
			module.append(item[0])
		# print(res)
		return [out,module]


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





		