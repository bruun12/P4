from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import IfStatement
from test_line_trim import lineTrim

def test_if_statement():
    correctLines = lineTrim("if(true){}")

    assert correctLines[0] == "if (true)"
    assert correctLines[1] == "{"
    assert correctLines[2] == "}"