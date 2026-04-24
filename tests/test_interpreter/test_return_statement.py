from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import ReturnStatement

def test_return_statement():
    lex = Lexer("""return 0;""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ReturnStatement)
    assert node.to_c() == "return 0;"

def test_return_statement():
    lex = Lexer("""return 
                         true 
        AND 
                                     false;""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ReturnStatement)
    assert node.to_c() == "return true && false;"

