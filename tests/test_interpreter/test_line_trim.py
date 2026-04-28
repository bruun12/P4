from lexer.lexer import Lexer
from parser.parser import Parser
from parser.ASTNodes import IfStatement

def lineTrim(lexerString:str):
    lex = Lexer(lexerString)
    lex.lexer()
    node = Parser(lex.tokens).statement()


    lines = node.to_c().split("\n")
    correctLines = []
    for line in lines:
        if line.strip() != "":
            correctLines.append(line.strip())

    return correctLines