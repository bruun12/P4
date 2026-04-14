from lexer.lexer import Lexer


string = "int x = 20 /* initializing */ x\ny = x * 5"
lex = Lexer(string)

# 1. Run the lexing process
lex.lexer() 

# 2. Print each token object in the list
for token in lex.tokens:
    print(token)