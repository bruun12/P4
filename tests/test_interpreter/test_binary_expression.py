from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import Binary

def test_binary_expression():
    lex = Lexer("2 + 3 + 2")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    assert isinstance(node, Binary)
    assert node.to_c() == "((2 + 3) + 2)"

def test_binary_expression2():
    lex = Lexer("x(1 ,   2                               ,                        3      )")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()

    assert node.to_c() == "x(1,2,3)"
