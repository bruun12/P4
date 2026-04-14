from parser.parser import Parser
from lexer.lexer import Lexer, TokenType

def test_advance():
    string = "int x = 20 // initilizing x\ny = x * 5"
    lex = Lexer(string)

    lex.lexer()

    parser = Parser(lex.tokens)
    assert parser.current().type == TokenType.IDENTIFIER

    while parser.current().type != TokenType.EOF:
        parser.advance()
    
    assert parser.current().type == TokenType.EOF
