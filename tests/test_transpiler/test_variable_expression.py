from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import Variable

def test_variable_expression_x():
    lex = Lexer("x")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    
    assert isinstance(node, Variable)
    assert node.to_c() == "x" 

def test_variable_expression_xyz():
    lex = Lexer("xyz")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    
    assert isinstance(node, Variable)
    assert node.to_c() == "xyz" 

def test_variable_expression_xyz12():
    lex = Lexer("xyz12")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    
    assert isinstance(node, Variable)
    assert node.to_c() == "xyz12" 
 
