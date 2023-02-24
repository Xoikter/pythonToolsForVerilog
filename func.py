import re
import os
import ply.yyac as yyac
import ply.lex as lex

tokens = (
    "NAME",
    "MIRCO",
    "OPERATE",
    "OTHERS",
    "SYMBOL",
    "NUMBER",
    "UNINUMBER",
    "SEMI",
    "OTHERS"
)
t_UNINUMBER = r'\d+[a-z][a-f0-9]+'
t_NUMBER = r'\d+'
t_NAME = r'[_A-Za-z]+'
t_MIRCO = r'`[_A-Za-z]+'
t_OPERATE = r'[\+\-\*\/\&\|\~\!\\<\>\+\^\=]'
t_SEMI = r';'
t_OTHERS = r'.'

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'
t_SYMBOL = r"[\[\]\(\)\:\#\,]"


fp = open("./code/test.sv", "r")
string = fp.read()

string = re.sub("\/\*.*?\*\/", "", string, flags=re.S)
string = re.sub('//.*?\n', "", string, flags=re.S)

lexer = lex.lex()
lexer.input(string)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
