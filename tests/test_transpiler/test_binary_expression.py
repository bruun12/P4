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

def test_binary_expression3():
    lex = Lexer("true OR (a<3+8 AND 4>=7) AND false")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()

    assert node.to_c() == "(true || (((a < (3 + 8)) && (4 >= 7)) && false))"

def test_binary_expression4():
    lex = Lexer("8 + f(9+3) * 5")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()

    assert node.to_c() == "(8 + (f((9 + 3)) * 5))"

def test_binary_expression5():
    lex = Lexer("a+b < c < 100")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()

    assert node.to_c() == "(((a + b) < c) && (c < 100))"

def test_binary_expression6():
    lex = Lexer("99 < comp >= b")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()

    assert node.to_c() == "((99 < comp) && (comp >= b))"

def test_binary_expression7():
    lex = Lexer("10 > 9 > 8 > 7 > 6 > 5")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()

    assert node.to_c() == "(((((10 > 9) && (9 > 8)) && (8 > 7)) && (7 > 6)) && (6 > 5))"