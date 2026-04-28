from lexer.lexer import Lexer
from parser.parser import Parser
from parser.ASTNodes import IfStatement

def lineTrim(lines:str):

    lines = lines.split("\n")
    correctLines = []
    for line in lines:
        if line.strip() != "":
            correctLines.append(line.strip())

    return correctLines