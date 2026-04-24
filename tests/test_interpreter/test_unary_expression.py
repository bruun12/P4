from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import Unary

def test_unary_expression():
    lex = Lexer("!true")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    assert isinstance(node, Unary)
    assert node.to_c() == "!true"

def test_unary_expression2():
    lex = Lexer("-               (5)       ")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    assert isinstance(node, Unary)
    assert node.to_c() == "-5"
