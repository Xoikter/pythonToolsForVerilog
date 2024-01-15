#verilog analyse
- 分析出文本所含有的模块
	- 数据结构 `{module_name:{module_var:{var_name:var_struct},module_inst:{inst_name:inst_struct}}`
		- `var_stuct = {isdefine:bool,define_width:0,has_load:,has_drive,only_inst_port_connect_width:0}`
- 分析出所有的begin块
- 分析出所有的{}块，用来进行连接关系的声明
- 分析出所有的if case后的判断块
- 分析出所含的module例化块
