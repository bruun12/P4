from lexer.lexer import Lexer

string = "int x = 20 /* initilizing /* x\ny = x * 5"
lex = Lexer(string)


print(lex)