from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import Literal

def test_literal_expression_integer():
    lex = Lexer("1")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    
    assert isinstance(node, Literal)
    assert node.to_c() == "1" 
    
def test_literal_expression_double():
    lex = Lexer("1.3")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    
    assert isinstance(node, Literal)
    assert node.to_c() == "1.3" 
    
def test_literal_expression_bool_true():
    lex = Lexer("true")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    
    assert isinstance(node, Literal)
    assert node.to_c() == "true" 
    
def test_literal_expression_bool_false():
    lex = Lexer("false")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    
    assert isinstance(node, Literal)
    assert node.to_c() == "false"     

def test_literal_expression_string():
    lex = Lexer('"Hej"')
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    
    assert isinstance(node, Literal)
    assert node.to_c() == '"Hej"' 