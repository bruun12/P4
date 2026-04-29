from lexer.lexer import Lexer
from parser.parser import Parser
from parser.ASTNodes import Parameter

def test_parameter():
    lex = Lexer("integer foobar(integer x, integer y) { return x; }")
    lex.lexer()
    node = Parser(lex.tokens).parse()
    params = node.functions[0].parameters

    assert params[0].to_c() == "int x"
    assert params[1].to_c() == "int y"

