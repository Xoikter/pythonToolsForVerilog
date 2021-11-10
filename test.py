from file_analyse import File_analyse
import re
if __name__=="__main__":
	# fp = open("/home/IC/xsc/gmec/rtl/aes/aes_misc_unit.v","r")
	fp = open("./test1.v","r")
	string_test = fp.read()
	fp.close()
	test_s = "begin end"
	pattern = re.compile("begin")
	stri = pattern.search(test_s).start()
	fa = File_analyse(string_test)
	fa.macro = ["xx"]
	fa.def_tools(string_test)
	# fa.(string_test)


	fp = open("./out.v","w+")
	fp.write(fa.find_varDefine(string_test)[1])
	fp.close()