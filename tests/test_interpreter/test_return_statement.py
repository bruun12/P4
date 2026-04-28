from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import ReturnStatement

def test_return_statement_int():
    lex = Lexer("""return 0;""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ReturnStatement)
    assert node.to_c() == "return 0;"

def test_return_statement_bool():
    lex = Lexer("""return true;""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ReturnStatement)
    assert node.to_c() == "return true;"

def test_return_statement_double():
    lex = Lexer("""return 5.2;""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ReturnStatement)
    assert node.to_c() == "return 5.2;"

def test_return_statement_string():
    lex = Lexer("""return "Hej";""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ReturnStatement)
    assert node.to_c() == """return "Hej";"""

def test_return_statement_expression():
    lex = Lexer("""return 
                         true 
        AND 
                                     false;""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ReturnStatement)
    assert node.to_c() == "return (true && false);"


