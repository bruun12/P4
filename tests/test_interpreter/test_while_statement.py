from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import WhileStatement

def test_binary_expression():
    lex = Lexer("""
                while(true)
                {x = 4;}""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, WhileStatement)
    assert node.to_c() == "while (true){x = 4;}"