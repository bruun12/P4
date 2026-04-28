from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import WhileStatement
from tests.test_interpreter.test_line_trim import lineTrim

def test_if_statement():
    lex = Lexer("""
                while(true)
                {x = 4;}""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, WhileStatement)
    correctLines = lineTrim(node.to_c())

    assert correctLines[0] == "while (true)"
    assert correctLines[1] == "{x = 4;}"


