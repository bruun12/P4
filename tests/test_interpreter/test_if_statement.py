from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import IfStatement
from tests.test_interpreter.test_line_trim import lineTrim

def test_if_statement():
    lex = Lexer("""if(true){}""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    correctLines = lineTrim(node.to_c())

    assert correctLines[0] == "if (true)"
    assert correctLines[1] == "{}"