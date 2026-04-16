from parser.parser import Parser
from lexer.lexer import TokenType, Token

def test_advance_success():
    tokens = [Token(TokenType.TYPE, "string", 1, 1),
              Token(TokenType.IDENTIFIER, "x", 2, 1)]



    parser = Parser(tokens)
    assert parser.current().type == TokenType.TYPE
    parser.advance()
    assert parser.current().type == TokenType.IDENTIFIER

