from file_analyse import File_analyse
import re
if __name__=="__main__":
	fp = open("/home/IC/xsc/gmec/rtl/core/gmec_core.v","r")
	# fp = open("./test.v","r")
	string_test = fp.read()
	fp.close()
	test_s = "begin      end"
	pattern = re.compile("\s*\\b[_a-zA-Z][_a-zA-Z0-9]*\\b",flags=re.S)
	match = pattern.match(test_s,3)
	pattern = re.compile("begin")
	stri = pattern.search(test_s).start()
	fa = File_analyse(string_test)
	fa.macro = ["xx"]
	fa.find_module_inst(string_test)
	
	# fa.(string_test)


	fp = open("./out.v","w+")
	fp.write(fa.find_varDefine(string_test)[1])
	fp.close()