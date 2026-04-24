from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import ExpressionStatement

def test_expression_statement():
    lex = Lexer("""5+7;""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ExpressionStatement)
    assert node.to_c() == "5 + 7;"

def test_expression_statement():
    lex = Lexer("""true 
                
                AND 
                
                false ;""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ExpressionStatement)
    assert node.to_c() == "true && false;"

