import re
import os
# import ply.yyac as yyac
import ply.lex as lex

keyword = ['always', 'and', 'assign', 'begin', 'buf', 'bufif0', 'bufif1', 'case', 'casex', 'casez', 'cmos',
                        'deassign',
                        'default',
                        'defparam', 'disable', 'edge', 'else', 'end', 'endcase', 'endmodule', 'endfunction',
                        'endprimitive','include',
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
                        'specparam', 'timescale'
                                     'strength', 'strong0', 'strong1', 'supply0', 'supply1', 'table', 'task', 'time',
                        'tran', 'tranif0',
                        'tranif1', 'tri',
                        'tri0', 'tri1', 'triand', 'trior', 'trireg', 'vectored', 'wait', 'wand', 'weak0', 'weak1',
                        'while', 'wire',
                        'wor', 'xnor', 'xor', 'extends', 'uvm_report_server', 'int', 'void', 'virtual', 'new',
                        'uvm_analysis_port', 'super'
            , 'extern0', "uvm_component_utils", "type_id", 'bit', 'byte', 'unsiged', 'shortint', 'longint', 'timer',
                        'real', 'interface', 'class',
                        'logic', 'genvar', 'uvm_tlm_analysis_fifo', 'uvm_blocking_get_port', 'constraint', 'import',
                        'uvm_active_passive_enum', 'define', 'undef'
            , 'ifdef', 'elsif', 'endif', "uvm_object_utils_begin", "uvm_object_utils_end", "`define", "`"]
tokens = (
    "MIRCO",
    "OPERATE",
    "OTHERS",
    "SYMBOL",
    "NUMBER",
    "UNINUMBER",
    "SEMI",
    # "OTHERS",
    "MODULE",
    "LPAREN",
    "NAME",
    "RPAREN"
)
t_OTHERS = r'.'
# t_MODULE = r"\\bmodule\\b"
t_UNINUMBER = r'\d+[a-z][a-f0-9]+'
t_NUMBER = r'\d+'
# t_NAME = r'\\b[_A-Za-z]+\\b'
t_MIRCO = r'`[_A-Za-z]+'
t_OPERATE = r'[\+\-\*\/\&\|\~\!\\<\>\+\^\=]'
t_SEMI = r';'
# t_SYMBOL = r"[\[\]\(\)\:\#\,]"
t_SYMBOL = r"[\#]"
t_LPAREN = r"\("
t_RPAREN = r"\)"
def t_MODULE(t):
    r"\bmodule\b"
    return t
def t_NAME(t):
    r'[_A-Za-z][_A-Za-z0-9\[\]\.]*'
    return t
def t_error(t):
    raise Exception('Lex error {} at line {}, illegal character {}'
                    .format(t.value[0], t.lineno, t.value[0]))
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'


fp = open("./code/test.sv", "r")
string = fp.read()

string = re.sub("\/\*.*?\*\/", "", string, flags=re.S)
string = re.sub('//.*?\n', "", string, flags=re.S)

lexer = lex.lex()
lexer.input(string)

# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     if tok.type == "MODULE":
#         lexer.token()
#         lexer.token()
#     temp = tok.value
#     if tok.type == "NAME" and tok.value not in keyword:
#         tok_temp = lexer.token()
#         if not tok_temp:
#             break
#         if tok_temp.value == r"#":
#             stack_par = []
#             tok_temp = lexer.token()
#             if not tok_temp:
#                 break
#             if tok_temp.value == "(":
#                 stack_par.append(r"(")
#                 while(True):
#                     tok_temp = lexer.token()
#                     if not tok_temp:
#                         break
                    
#                     if tok_temp.value == "(":
#                         stack_par.append(r"(")
#                     if tok_temp.value == ")":
#                         stack_par.pop()
#                     if len(stack_par) == 0:
#                         break
#                 tok_temp = lexer.token()
#                 if not tok_temp:
#                     break
#                 if tok_temp.type != "NAME":
#                     print("[WARNING] there is a waring!!!")
#                 elif tok_temp.value not in keyword :
#                     print("[INFO] find module inst name is " + temp)
#             else:
#                 print("[WARNING] there is a waring!!! no (")
#         elif tok_temp.type ==  "NAME" and tok_temp.value not in keyword:
#                     print("[INFO] find module inst name 22 is " + temp)



        
    # print(tok)
module_lex = []
while True:
            tok = lexer.token()
            if not tok:
                break
            if tok.type == "MODULE":
                print("module name " + lexer.token().value)
                lexer.token()
            temp = tok.value
            if tok.type == "NAME" and tok.value not in keyword:
                tok_temp = lexer.token()
                if not tok_temp:
                    break
                if tok_temp.value == r"#":
                    stack_par = []
                    tok_temp = lexer.token()
                    if not tok_temp:
                        break
                    if tok_temp.value == "(":
                        stack_par.append(r"(")
                        while(True):
                            tok_temp = lexer.token()
                            if not tok_temp:
                                break
                            
                            if tok_temp.value == "(":
                                stack_par.append(r"(")
                            if tok_temp.value == ")":
                                stack_par.pop()
                            if len(stack_par) == 0:
                                break
                        tok_temp = lexer.token()
                        if not tok_temp:
                            break
                        # if tok_temp.type != "NAME":
                            # print("[WARNING] there is a waring!!!")
                        if tok_temp.type == "NAME" and tok_temp.value not in keyword :
                            temp2 = tok_temp.value
                            tok_temp = lexer.token()
                            if not tok_temp:
                                break
                            if(tok_temp.value == "("):
                                # print("[INFO] find module inst name is " + temp)
                                module_lex.append(temp)
                            elif tok_temp.type == "NAME" and tok_temp.value not in keyword:
                                tok_temp = lexer.token()
                                if not tok_temp:
                                    break
                                if(tok_temp.value == "("):
                                    print("[INFO] find module inst name is " + temp2)
                                    module_lex.append(temp2)


                    else:
                        print("[WARNING] there is a waring!!! no (")
                elif tok_temp.type ==  "NAME" and tok_temp.value not in keyword:
                            temp2 = tok_temp.value
                            tok_temp = lexer.token()
                            if not tok_temp:
                                break
                            if(tok_temp.value == "("):
                                print("[INFO] find module inst name is 22 " + temp)
                                module_lex.append(temp)
                            elif tok_temp.type == "NAME" and tok_temp.value not in keyword:
                                tok_temp = lexer.token()
                                if not tok_temp:
                                    break
                                if(tok_temp.value == "("):
                                    print("[INFO] find module inst name is " + temp2)
                                    module_lex.append(temp2)